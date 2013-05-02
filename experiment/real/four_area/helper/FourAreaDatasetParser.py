from Stemmer import Stemmer
from collections import defaultdict
import json
import os
import re
import cPickle
from networkx import MultiDiGraph
import operator
from src.importer.error.FourAreaParseError import FourAreaParseError

__author__ = 'jontedesco'

# Regex for stripping non-visible characters
controlChars = ''.join(map(unichr, range(0, 32) + range(127, 160)))
controlCharactersRegex = re.compile('[%s]' % re.escape(controlChars))

# HACK: Get the absolute project root, assuming top-level dir is named 'RicherPathSIM'
projectRoot = str(os.getcwd())
projectRoot = projectRoot[:projectRoot.find('RicherPathSIM') + len('RicherPathSIM')]

# Get the stop words set & stemmer for text analysis
stopWords = None
with open(os.path.join(projectRoot, 'src', 'importer', 'stopWords.json')) as stopWordsFile:
    stopWords = set(json.load(stopWordsFile))
stemmer = Stemmer('english')


def __removeControlCharacters(string):
    string = string.strip('\xef\xbb\xbf')
    return controlCharactersRegex.sub('', string)


def addCitationsToGraph(graph, nodeIndex):

    inputFile = open(os.path.join(projectRoot, 'data', 'DBLP-citation-Feb21.txt'))
    fileStart = inputFile.tell()
    paperTitles = set(nodeIndex['paper'].values())

    # Build an index of int -> paper title (including only papers found in the graph)
    dblpPaperIndex = {}

    lastTitle = None
    for line in inputFile:
        if line.startswith('#*'):
            title = str(line[2:]).strip()
            lastTitle = title if title in paperTitles else None
        elif line.startswith('#index'):
            i = int(__removeControlCharacters(line[len('#index'):]))
            if lastTitle is not None:
                dblpPaperIndex[i] = lastTitle
        elif len(__removeControlCharacters(line)) == 0:
            lastTitle = None

    inputFile.seek(fileStart)

    # Use to perform error checking
    existingNodes = set(graph.nodes())

    # Dictionary of paper titles to their citation counts
    citationCounts = defaultdict(int)

    # Add citations to the papers in the graph
    for line in inputFile:

        # Found new paper block
        if line.startswith('#*'):
            title = __removeControlCharacters(line[2:])
            lastTitle = title if title in paperTitles else None

        # Found new citations
        elif line.startswith('#%'):
            citationIndex = int(__removeControlCharacters(line[2:]))

            # Check that both the citing & cited papers are in our dataset
            citingPaperIsValid = lastTitle is not None and lastTitle in paperTitles
            citedPaperValid = citationIndex in dblpPaperIndex

            if citedPaperValid and citingPaperIsValid:

                # Check that we're not inadvertently adding meaningless edges (since networkx silently adds new nodes
                # if endpoints of edge do not exist...)
                if lastTitle not in existingNodes:
                    raise FourAreaParseError('Citing paper not found in graph: %s' % lastTitle)
                if dblpPaperIndex[citationIndex] not in existingNodes:
                    raise FourAreaParseError('Cited paper not found in graph: %s' % dblpPaperIndex[citationIndex])

                graph.add_edge(lastTitle, dblpPaperIndex[citationIndex])
                citationCounts[dblpPaperIndex[citationIndex]] += 1

        # Reached end of the paper block, reset title if no citation was found (error check)
        elif len(__removeControlCharacters(line)) == 0:
            lastTitle = None

    inputFile.close()

    # Output papers ordered by number of citations
    bestPapers = sorted(citationCounts.iteritems(), key=operator.itemgetter(1))
    bestPapers.reverse()
    paperCitationsFile = open(os.path.join('../data', 'paperCitationCounts'), 'w')
    for i in xrange(0, len(bestPapers)):
        paperCitationsFile.write('%d: %s\n' % (bestPapers[i][1], bestPapers[i][0]))


def parseFourAreaDataset():
    """
      Parse the four area dataset, and use only barebones structures to keep everything efficient
    """

    inputFolderPath = os.path.join('../data', 'four_area')
    nodeIndex = {}
    graph = MultiDiGraph()

    # Add all nodes of some single type to the graph
    def __parseNodeType(lineParser, typeName, fileName, graph, nodeIndex):
        nodeIndex[typeName] = {}
        inputFile = open(os.path.join(projectRoot, inputFolderPath, fileName))
        for line in inputFile:
            objectId, content = lineParser(line)
            if objectId in nodeIndex[typeName]:
                raise FourAreaParseError("Found duplicate node id %d parsing %ss" % (objectId, typeName))
            if content is not None:
                nodeIndex[typeName][objectId] = content
                graph.add_node(content)
        inputFile.close()

    # Parse authors from file
    def authorLineParser(line):
        authorData = line.split()
        authorId = int(__removeControlCharacters(authorData[0]))
        authorName = ' '.join(authorData[1:])
        return authorId, authorName
    __parseNodeType(authorLineParser, 'author', 'author.txt', graph, nodeIndex)

    # Parse conferences from file
    def conferenceLineParser(line):
        conferenceData = line.split()
        conferenceId = int(__removeControlCharacters(conferenceData[0]))
        conferenceName = ' '.join(conferenceData[1:])
        return conferenceId, conferenceName
    __parseNodeType(conferenceLineParser, 'conference', 'conf.txt', graph, nodeIndex)

    # Parse papers
    def paperLineParser(line):
        paperData = line.split()
        paperId = int(__removeControlCharacters(paperData[0]))
        paperTitle = ' '.join(paperData[1:])

        # Filter 'garbage' titles
        garbageTitleSegments = ['Preface.', 'Title, ']
        titleIsGarbage = max([segment in paperTitle for segment in garbageTitleSegments])
        paperTitle = None if titleIsGarbage else paperTitle

        return paperId, paperTitle
    __parseNodeType(paperLineParser, 'paper', 'paper.txt', graph, nodeIndex)

    # Parse terms
    def termLineParser(line):
        topicId, term = line.split()
        topicId = int(__removeControlCharacters(topicId))
        term = stemmer.stemWord(term)
        topic = term if term not in stopWords else None
        return topicId, topic
    __parseNodeType(termLineParser, 'term', 'term.txt', graph, nodeIndex)

    # Add edges to the graph
    def __parseEdgeType(nodeTypeAMap, nodeTypeBMap, graph, fileName):
        inputFile = open(os.path.join(projectRoot, inputFolderPath, fileName))
        for line in inputFile:
            typeAId, typeBId = line.split()
            typeAId = int(__removeControlCharacters(typeAId))
            typeBId = int(__removeControlCharacters(typeBId))
            if typeAId in nodeTypeAMap and typeBId in nodeTypeBMap:
                nodeA = nodeTypeAMap[typeAId]
                nodeB = nodeTypeBMap[typeBId]
                graph.add_edge(nodeA, nodeB)
                graph.add_edge(nodeB, nodeA)
    __parseEdgeType(nodeIndex['paper'], nodeIndex['author'], graph, 'paper_author.txt')
    __parseEdgeType(nodeIndex['paper'], nodeIndex['conference'], graph, 'paper_conf.txt')
    __parseEdgeType(nodeIndex['paper'], nodeIndex['term'], graph, 'paper_term.txt')

    return graph, nodeIndex


def constructGraphAndDumpToFile():

    # Parse 4-area dataset graph & dump it to disk
    graph, nodeIndex = parseFourAreaDataset()
    addCitationsToGraph(graph, nodeIndex)

    cPickle.dump((graph, nodeIndex), open(os.path.join('../data', 'graphWithCitations'), 'w'))


# When run as script, runs through pathsim papers example experiment
if __name__ == '__main__':
    constructGraphAndDumpToFile()
