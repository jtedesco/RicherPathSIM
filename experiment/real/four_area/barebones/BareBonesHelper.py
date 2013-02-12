from Stemmer import Stemmer
import json
import os
from pprint import pprint
import re
from networkx import MultiDiGraph
import numpy
import operator
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


def getMetaPathAdjacencyData(graph, nodeIndex, metaPath, givenNode = None):
    """
      Get the adjacency matrix along some meta path (given by an array of keywords)

        NOTE: This cannot handle paths with repeated types
    """

    assert len(metaPath) >= 1

    # Build all of the paths
    paths = [givenNode] if (givenNode is not None) else [[node] for node in nodeIndex[metaPath[0]].values()]
    for nodeType in metaPath[1:]:
        nextPaths = []
        eligibleNodes = set(nodeIndex[nodeType].values())
        for path in paths:
            for neighbor in graph.successors(path[-1]):

                # Do not check for repeated nodes, because we assume meta path has no repeats
                if neighbor in eligibleNodes: nextPaths.append(path + [neighbor])
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


def getPathSimScore(adjMatrix, sI, dI):
    if adjMatrix[sI][dI] == 0: return 0
    return (2.0 * adjMatrix[sI][dI]) / float(adjMatrix[sI][sI] + adjMatrix[dI][dI])


def findMostSimilarNodesPathSim(adjMatrix, source, extraData, k=10):
    sourceIndex = extraData['fromNodesIndex'][source]
    toNodes = extraData['toNodes']

    similarityScores = {toNodes[i]: getPathSimScore(adjMatrix, sourceIndex, i) for i in xrange(0, len(toNodes))}
    mostSimilarNodes = sorted(similarityScores.iteritems(), key=operator.itemgetter(1))
    mostSimilarNodes.reverse()
    number = min([k, len(mostSimilarNodes)])
    mostSimilarNodes = mostSimilarNodes[:number]
    return mostSimilarNodes


# When run as script, runs through pathsim papers example experiment
if __name__ == '__main__':

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

    pprint(getMetaPathAdjacencyData(graph, nodeIndex, ['author', 'paper', 'conference']))
