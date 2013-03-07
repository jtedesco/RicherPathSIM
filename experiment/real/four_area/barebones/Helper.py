from Stemmer import Stemmer
from collections import defaultdict
import json
import os
import re
import cPickle
import operator

from networkx import MultiDiGraph
from scipy.sparse import  csr_matrix, lil_matrix, csc_matrix
import texttable

from src.importer.error.FourAreaParseError import FourAreaParseError


__author__ = 'jontedesco'

# Authors & papers to use for experiments
testAuthors = [
    'Christos Faloutsos',
    'Rakesh Agrawal',
#    'Jiawei Han',
    'Sergey Brin',
#    'Sanjay Ghemawat',
    'Philip S. Yu',
    'AnHai Doan'
]
testPapers = [
    'Mining Association Rules between Sets of Items in Large Databases.',
    'R-Trees: A Dynamic Index Structure for Spatial Searching.',
    'Efficient Reasoning in Qualitative Probabilistic Networks.',
    'Self-Tuning Database Systems: A Decade of Progress.',
    'R-trees with Update Memos.'
]


# Regex for stripping non-visible characters
controlChars = ''.join(map(unichr, range(0,32) + range(127,160)))
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
        inputFile = open(os.path.join(projectRoot, inputFolderPath, fileName))
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


def getMetaPathAdjacencyData(graph, nodeIndex, metaPath, rows = False):
    """
      Get the adjacency matrix along some meta path (given by an array of keywords)
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

    # Build the adjacency matrix (as a sparse array)
    data, row, col =  [], [], []
    for path in paths:
        row.append(fromNodesIndex[path[0]])
        col.append(toNodesIndex[path[-1]])
        data.append(1)
    matrixType = csr_matrix if rows else csc_matrix
    adjMatrix = matrixType((data, (row,col)), shape=(len(fromNodes), len(toNodes)))

    extraData = {
        'fromNodes': fromNodes,
        'fromNodesIndex': fromNodesIndex,
        'toNodes': toNodes,
        'toNodesIndex': toNodesIndex
    }

    return adjMatrix, extraData

def addCitationsToGraph(graph, nodeIndex):

    file = open(os.path.join(projectRoot, 'data','DBLP-citation-Feb21.txt'))
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

    file.seek(fileStart)

    # Use to perform error checking
    existingNodes = set(graph.nodes())

    # Dictionary of paper titles to their citation counts
    citationCounts = defaultdict(int)

    # Add citations to the papers in the graph
    for line in file:

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

    file.close()

    # Output papers ordered by number of citations
    bestPapers = sorted(citationCounts.iteritems(), key=operator.itemgetter(1))
    bestPapers.reverse()
    paperCitationsFile = open(os.path.join('data', 'paperCitationCounts'), 'w')
    for i in xrange(0, len(bestPapers)):
        paperCitationsFile.write('%d: %s\n' % (bestPapers[i][1], bestPapers[i][0]))


def getPathSimScore(adjacencyMatrix, sI, dI):
    if adjacencyMatrix[sI,dI] == 0: return 0
    return (2.0 * adjacencyMatrix[sI,dI]) / float(adjacencyMatrix[sI,sI] + adjacencyMatrix[dI,dI])


def getNeighborSimScore(adjacencyMatrix, xI, yI, smoothed = False):

    sourceColumn = adjacencyMatrix.getcol(xI)
    destColumn = adjacencyMatrix.getcol(yI)

    # Compute numerator dot product
    total = 1 if smoothed else 0
    total += (destColumn.transpose() * sourceColumn)[0,0]
    if total == 0: return 0

    # Compute normalization dot products
    sourceNormalization = 1 if smoothed else 0
    sourceNormalization += (sourceColumn.transpose() * sourceColumn)[0,0]
    destNormalization = 1 if smoothed else 0
    destNormalization += (destColumn.transpose() * destColumn)[0,0]

    similarityScore = total
    if total > 0:
        similarityScore = 2 * total / float(sourceNormalization + destNormalization)

    return similarityScore


def getAbsNeighborSimScore(adjacencyMatrix, xI, yI, smoothed = False):

    sourceColumn = adjacencyMatrix.getcol(xI)
    destColumn = adjacencyMatrix.getcol(yI)

    sourceNorm = (sourceColumn.transpose() * sourceColumn)[0,0]
    destNorm = (destColumn.transpose() * destColumn)[0,0]

    # Compute numerator
    total = 1 if smoothed else 0
    total += 2 * (max(destNorm, sourceNorm) - abs(destNorm - sourceNorm))
    if total == 0: return 0

    # Compute normalization
    sourceNormalization = 1 if smoothed else 0
    sourceNormalization += sourceNorm
    destNormalization = 1 if smoothed else 0
    destNormalization += destNorm

    similarityScore = total
    if total > 0:
        similarityScore = 2 * total / float(sourceNormalization + destNormalization)

    return similarityScore


def findMostSimilarNodes(adjMatrix, source, extraData, method=getPathSimScore, k=10, skipZeros=True):
    sourceIndex = extraData['fromNodesIndex'][source]
    toNodes = extraData['toNodes']

    # Find all similarity scores, optionally skipping nonzero scores for memory usage
    if skipZeros:
        similarityScores = {}
        for i in xrange(len(toNodes)):
            sim = method(adjMatrix, sourceIndex, i)
            if sim > 0: similarityScores[toNodes[i]] = sim
    else:
        similarityScores = {toNodes[i]: method(adjMatrix, sourceIndex, i) for i in xrange(0, len(toNodes))}

    # Sort according to most similar (descending order)
    mostSimilarNodes = sorted(similarityScores.iteritems(), key=operator.itemgetter(1))
    mostSimilarNodes.reverse()
    number = min([k, len(mostSimilarNodes)])
    mostSimilarNodes = mostSimilarNodes[:number]

    return mostSimilarNodes, similarityScores

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

    # Compute PathSim similarity scores
    apcAdjMatrix, extraData = getMetaPathAdjacencyData(graph, nodeIndex, ['author', 'paper', 'conference'], rows=True)
    cpaAdjMatrix, data = getMetaPathAdjacencyData(graph, nodeIndex, ['conference', 'paper', 'author'])
    apcpaAdjMatrix = lil_matrix(apcAdjMatrix * cpaAdjMatrix)
    extraData['toNodes'] = data['toNodes']
    extraData['toNodesIndex'] = data['toNodesIndex']
    author = 'Mike'
    pathSimMostSimilar, similarityScores = findMostSimilarNodes(apcpaAdjMatrix, author, extraData)

    # Compute NeighborSim similarity scores
    cpaAdjMatrix, data = getMetaPathAdjacencyData(graph, nodeIndex, ['conference', 'paper', 'author'])
    data['fromNodes'] = data['toNodes']
    data['fromNodesIndex'] = data['toNodesIndex']
    author = 'Mike'
    neighborSimMostSimilar, similarityScores = findMostSimilarNodes(cpaAdjMatrix, author, extraData, method=getNeighborSimScore)

    for name, mostSimilar in [('PathSim', pathSimMostSimilar), ('NeighborSim', neighborSimMostSimilar)]:
        print('\n%s Most Similar to "%s":' % (name, author))
        mostSimilarTable = texttable.Texttable()
        rows = [['Author', 'Score']]
        rows += [[name, score] for name, score in mostSimilar]
        mostSimilarTable.add_rows(rows)
        print(mostSimilarTable.draw())


def constructGraphAndDumpToFile():

    # Parse 4-area dataset graph & dump it to disk
    graph, nodeIndex = parseFourAreaDataset()
    addCitationsToGraph(graph, nodeIndex)

    cPickle.dump((graph, nodeIndex), open(os.path.join('data', 'graphWithCitations'), 'w'))


# When run as script, runs through pathsim papers example experiment
if __name__ == '__main__':
    constructGraphAndDumpToFile()
#    pathSimPaperExample()
