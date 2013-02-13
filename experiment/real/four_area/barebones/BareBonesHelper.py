from Stemmer import Stemmer
import json
import os
import re
import cPickle
from networkx import MultiDiGraph
import numpy
import operator
import texttable
from src.importer.error.FourAreaParseError import FourAreaParseError

__author__ = 'jontedesco'

# Regex for stripping non-visible characters
controlChars = ''.join(map(unichr, range(0,32) + range(127,160)))
controlCharactersRegex = re.compile('[%s]' % re.escape(controlChars))

# Get the stop words set & stemmer for text analysis
stopWords = None
with open(os.path.join(os.getcwd(), 'src', 'importer', 'stopWords.json')) as stopWordsFile:
    stopWords = set(json.load(stopWordsFile))
stemmer = Stemmer('english')

def __removeControlCharacters(string):
    string = string.strip('\xef\xbb\xbf')
    return controlCharactersRegex.sub('', string)

def parseFourAreaDataset():
    """
      Parse the four area dataset, and use only barebones structures to keep everything efficient
    """

    inputFolderPath = os.path.join('data','four_area')
    nodeIndex = {}
    graph = MultiDiGraph()

    # Add all nodes of some single type to the graph
    def __parseNodeType(lineParser, typeName, fileName, graph, nodeIndex):
        nodeIndex[typeName] = {}
        inputFile = open(os.path.join(inputFolderPath, fileName))
        for line in inputFile:
            id, content = lineParser(line)
            if id in nodeIndex[typeName]:
                raise FourAreaParseError("Found duplicate node id %d parsing %ss" % (id, typeName))
            if content is not None:
                nodeIndex[typeName][id] = content
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
        return paperId, paperTitle
    __parseNodeType(paperLineParser, 'paper', 'paper.txt', graph, nodeIndex)

    # Parse terms
    def termLineParser(line):
        topicId, term = line.split()
        topicId = int(__removeControlCharacters(topicId))
        term = stemmer.stemWord(term)
        topic = term if term not in stopWords else None
        return topicId, topic
    __parseNodeType(termLineParser, 'topic', 'term.txt', graph, nodeIndex)

    # Add edges to the graph
    def __parseEdgeType(nodeTypeAMap, nodeTypeBMap, graph, fileName):
        inputFile = open(os.path.join(inputFolderPath, fileName))
        for line in inputFile:
            typeAId, typeBId = line.split()
            typeAId = int(__removeControlCharacters(typeAId))
            typeBId = int(__removeControlCharacters(typeBId))
            nodeA = nodeTypeAMap[typeAId]
            nodeB = nodeTypeBMap[typeBId]
            graph.add_edge(nodeA, nodeB)
            graph.add_edge(nodeB, nodeA)
    __parseEdgeType(nodeIndex['paper'], nodeIndex['author'], graph, 'paper_author.txt')
    __parseEdgeType(nodeIndex['paper'], nodeIndex['conference'], graph, 'paper_conf.txt')
    __parseEdgeType(nodeIndex['paper'], nodeIndex['conference'], graph, 'paper_conf.txt')

    return graph, nodeIndex


def getMetaPathAdjacencyData(graph, nodeIndex, metaPath):
    """
      Get the adjacency matrix along some meta path (given by an array of keywords)

        NOTE: This cannot handle paths with repeated types
    """

    assert len(metaPath) >= 1

    # Build all of the paths
    paths = [[node] for node in nodeIndex[metaPath[0]].values()]
    for nodeType in metaPath[1:]:
        nextPaths = []
        eligibleNodes = set(nodeIndex[nodeType].values())
        for path in paths:
            for neighbor in graph.successors(path[-1]):

                # Do not check for repeated nodes... (could result in infinite loop if path/graph allows backtracking)
                if neighbor in eligibleNodes:
                    nextPaths.append(path + [neighbor])

        paths = nextPaths

    # Build the index into the rows of the graph
    fromNodes = nodeIndex[metaPath[0]].values()
    fromNodesIndex = {fromNodes[i]: i for i in xrange(0, len(fromNodes))}
    toNodes = nodeIndex[metaPath[-1]].values()
    toNodesIndex = {toNodes[i]: i for i in xrange(0, len(toNodes))}

    # Build the adjacency matrix
    adjMatrix = numpy.zeros((len(fromNodes), len(toNodes)), dtype=numpy.float16)
    for path in paths:
        adjMatrix[fromNodesIndex[path[0]]][toNodesIndex[path[-1]]] += 1

    extraData = {
        'paths': paths,
        'nodeIndex': nodeIndex,
        'fromNodes': fromNodes,
        'fromNodesIndex': fromNodesIndex,
        'toNodes': toNodes,
        'toNodesIndex': toNodesIndex
    }

    return adjMatrix, extraData

def addCitationsToGraph(graph, nodeIndex):

    file = open(os.path.join('data','DBLP-citation-Feb21.txt'))
    fileStart = file.tell()
    paperTitles = set(nodeIndex['paper'].values())

    # Build an index of int -> paper title (including only papers found in the graph)
    dblpPaperIndex = {}
    lastTitle = None
    for line in file:
        if line.startswith('#*'):
            title = str(line[2:]).strip()
            lastTitle = title if title in paperTitles else None
        elif line.startswith('#index'):
            i = int(__removeControlCharacters(line[len('#index'):]))
            if lastTitle is not None:
                dblpPaperIndex[i] = lastTitle
        elif len(__removeControlCharacters(line)) == 0:
            lastTitle = None

    # Add citations to the papers in the graph
    citationsSkipped = 0
    citationsSucceeded = 0
    file.seek(fileStart) # Rewind the file pointer
    for line in file:

        # Found new paper block
        if line.startswith('#*'):
            title = __removeControlCharacters(line[2:])
            lastTitle = title if title in paperTitles else None

        # Found new citations
        elif line.startswith('#%'):
            if lastTitle is not None and lastTitle in paperTitles:
                citationIndex = int(__removeControlCharacters(line[2:]))
                try:
                    graph.add_edge(lastTitle, dblpPaperIndex[citationIndex])
                    citationsSucceeded += 1
                except KeyError:
                    citationsSkipped +=1

        # Reached end of the paper block, reset title if no citation was found (error check)
        elif len(__removeControlCharacters(line)) == 0:
            lastTitle = None

    print("Missing %d cited papers..." % citationsSkipped)
    print("Cited %d papers..." % citationsSucceeded)
    file.close()



def getPathSimScore(adjacencyMatrix, sI, dI):
    if adjacencyMatrix[sI][dI] == 0: return 0
    return (2.0 * adjacencyMatrix[sI][dI]) / float(adjacencyMatrix[sI][sI] + adjacencyMatrix[dI][dI])

def getNeighborSimScore(adjacencyMatrix, xI, yI, smoothed = False):

    # Find the shared in-neighbors of these nodes in the projected graph
    xInNeighborIndices = set()
    yInNeighborIndices = set()
    for citingAuthorIndex in xrange(0, len(adjacencyMatrix)):
        if adjacencyMatrix[citingAuthorIndex][xI] != 0: xInNeighborIndices.add(citingAuthorIndex)
        if adjacencyMatrix[citingAuthorIndex][yI] != 0: yInNeighborIndices.add(citingAuthorIndex)
    sharedInNeighborIndices = xInNeighborIndices.intersection(yInNeighborIndices)

    # Calculate numerator
    total = 1 if smoothed else 0
    for sharedNIndex in sharedInNeighborIndices:
        total += (adjacencyMatrix[sharedNIndex][xI] * adjacencyMatrix[sharedNIndex][yI])

    if total == 0: return 0

    # Accumulate normalizations
    sourceNormalization = 1 if smoothed else 0
    for sourceNeighborIndex in xInNeighborIndices:
        sourceNormalization += adjacencyMatrix[sourceNeighborIndex][xI] ** 2
    destNormalization = 1 if smoothed else 0
    for destNeighborIndex in yInNeighborIndices:
        destNormalization += adjacencyMatrix[destNeighborIndex][yI] ** 2

    similarityScore = total
    if total > 0:
        similarityScore = 2 * total / float(sourceNormalization + destNormalization)

    return similarityScore

def findMostSimilarNodes(adjMatrix, source, extraData, method=getPathSimScore, k=10):
    sourceIndex = extraData['fromNodesIndex'][source]
    toNodes = extraData['toNodes']

    similarityScores = {toNodes[i]: method(adjMatrix, sourceIndex, i) for i in xrange(0, len(toNodes))}
    mostSimilarNodes = sorted(similarityScores.iteritems(), key=operator.itemgetter(1))
    mostSimilarNodes.reverse()
    number = min([k, len(mostSimilarNodes)])
    mostSimilarNodes = mostSimilarNodes[:number]
    return mostSimilarNodes


def pathSimPaperExample():

    def add_apc_to_graph(graph, author, conference, n):
        papers = []
        for i in xrange(0, n):
            newPaper = '%s-%s-%d' % (author, conference, i)
            graph.add_node(newPaper)
            graph.add_edges_from([(author, newPaper), (newPaper, author), (newPaper, conference), (conference, newPaper)])
            papers.append(newPaper)
        return papers

    graph = MultiDiGraph()
    graph.add_nodes_from(['Mike', 'Jim', 'Mary', 'Bob', 'Ann'])
    graph.add_nodes_from(['SIGMOD', 'VLDB', 'ICDE', 'KDD'])
    papers = []
    papers += add_apc_to_graph(graph, 'Mike', 'SIGMOD', 2)
    papers += add_apc_to_graph(graph, 'Mike', 'VLDB', 1)
    papers += add_apc_to_graph(graph, 'Jim', 'SIGMOD', 50)
    papers += add_apc_to_graph(graph, 'Jim', 'VLDB', 20)
    papers += add_apc_to_graph(graph, 'Mary', 'SIGMOD', 2)
    papers += add_apc_to_graph(graph, 'Mary', 'ICDE', 1)
    papers += add_apc_to_graph(graph, 'Bob', 'SIGMOD', 2)
    papers += add_apc_to_graph(graph, 'Bob', 'VLDB', 1)
    papers += add_apc_to_graph(graph, 'Ann', 'ICDE', 1)
    papers += add_apc_to_graph(graph, 'Ann', 'KDD', 1)
    nodeIndex = {
        'paper': {i: papers[i] for i in xrange(0, len(papers))},
        'conference': {0: 'SIGMOD', 1: 'VLDB', 2: 'ICDE', 3: 'KDD'},
        'author': {0: 'Mike', 1: 'Jim', 2: 'Mary', 3: 'Bob'}
    }

    apcAdjMatrix, extraData = getMetaPathAdjacencyData(graph, nodeIndex, ['author', 'paper', 'conference'])
    cpaAdjMatrix, data = getMetaPathAdjacencyData(graph, nodeIndex, ['conference', 'paper', 'author'])
    apcpaAdjMatrix = numpy.dot(apcAdjMatrix, cpaAdjMatrix)
    extraData['toNodes'] = data['toNodes']
    extraData['toNodesIndex'] = data['toNodesIndex']

    author = 'Mike'
    mostSimilar = findMostSimilarNodes(apcpaAdjMatrix, author, extraData)
    print('\nMost Similar to "%s":' % author)
    mostSimilarTable = texttable.Texttable()
    rows = [['Author', 'Score']]
    rows += [[name, score] for name, score in mostSimilar]
    mostSimilarTable.add_rows(rows)
    print(mostSimilarTable.draw())


def constructGraphAndDumpToFile():

    # Parse 4-area dataset graph & dump it to disk
    graph, nodeIndex = parseFourAreaDataset()
    addCitationsToGraph(graph, nodeIndex)

    cPickle.dump((graph, nodeIndex), open(os.path.join('data', 'four_area', 'graphWithCitations'), 'w'))


# When run as script, runs through pathsim papers example experiment
if __name__ == '__main__':
#    constructGraphAndDumpToFile()
    pathSimPaperExample()