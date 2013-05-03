from collections import defaultdict
import operator
from scipy.sparse import csr_matrix, csc_matrix
from experiment.real.four_area.helper.SparseArray import SparseArray

__author__ = 'jontedesco'

# Authors & papers to use for experiments
testAuthors = [
    'Christos Faloutsos',
    'Rakesh Agrawal',
    # 'Jiawei Han',
    'Sergey Brin',
    # 'Sanjay Ghemawat',
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


def buildPathsMap(graph, metaPath, nodeIndex):
    """
      Build the path instances map for a particular meta path
    """

    # Build all of the paths
    pathsMap = {node: [[node]] for node in nodeIndex[metaPath[0]].values()}
    for nodeType in metaPath[1:]:
        nextPathsMap = defaultdict(list)
        eligibleNodes = set(nodeIndex[nodeType].values())

        for startNode in pathsMap:
            for path in pathsMap[startNode]:
                for neighbor in graph.successors(path[-1]):

                    # Do not check for repeated nodes... (could result in infinite loop?)
                    if neighbor in eligibleNodes:
                        nextPathsMap[startNode].append(path + [neighbor])

        pathsMap = nextPathsMap

    # Rebuild as a two-level dictionary, indexed by start and end node
    newPathsMap = defaultdict(lambda: defaultdict(list))
    for startNode in pathsMap:
        for path in pathsMap[startNode]:
            newPathsMap[startNode][path[-1]].append(path)

    return newPathsMap


def getMetaPathAdjacencyData(graph, nodeIndex, metaPath, rows=False):
    """
      Get the adjacency matrix along some meta path (given by an array of keywords)
    """

    assert len(metaPath) >= 1

    pathsMap = buildPathsMap(graph, metaPath, nodeIndex)

    # Build the index into the rows of the graph
    fromNodes = nodeIndex[metaPath[0]].values()
    fromNodesIndex = {fromNodes[i]: i for i in xrange(0, len(fromNodes))}
    toNodes = nodeIndex[metaPath[-1]].values()
    toNodesIndex = {toNodes[i]: i for i in xrange(0, len(toNodes))}

    extraData = {
        'fromNodes': fromNodes,
        'fromNodesIndex': fromNodesIndex,
        'toNodes': toNodes,
        'toNodesIndex': toNodesIndex
    }

    # Build the adjacency matrix (as a sparse array)
    data, row, col = [], [], []
    for startNode in pathsMap:
        for endNode in pathsMap[startNode]:
            for _ in pathsMap[startNode][endNode]:
                row.append(fromNodesIndex[startNode])
                col.append(toNodesIndex[endNode])
                data.append(1)
    matrixType = csr_matrix if rows else csc_matrix
    adjMatrix = matrixType((data, (row, col)), shape=(len(fromNodes), len(toNodes)))

    return adjMatrix, extraData


def getMetaPathAdjacencyTensorData(graph, nodeIndex, metaPath, rows=False):
    """
      Get the adjacency tensor along some meta path
    """

    assert len(metaPath) >= 1

    pathsMap = buildPathsMap(graph, metaPath, nodeIndex)

    # Build the index into the rows of the graph
    fromNodes = nodeIndex[metaPath[0]].values()
    fromNodesIndex = {fromNodes[i]: i for i in xrange(0, len(fromNodes))}
    toNodes = nodeIndex[metaPath[-1]].values()
    toNodesIndex = {toNodes[i]: i for i in xrange(0, len(toNodes))}

    # Build the adjacency tensor
    adjacencyTensor = SparseArray((len(fromNodesIndex), len(toNodesIndex), len(metaPath)))  # M x N x K tensor
    for startNode in pathsMap:
        for endNode in pathsMap[startNode]:
            pathInstances = pathsMap[startNode][endNode]

            # Get the set of edge cuts for each step along the meta path
            for i in xrange(0, len(metaPath)-1):
                edgePairs = {(pathInstance[i], pathInstance[i+1]) for pathInstance in pathInstances}
                adjacencyTensor[fromNodesIndex[startNode], toNodesIndex[endNode], i] = len(edgePairs)

    extraData = {
        'fromNodes': fromNodes,
        'fromNodesIndex': fromNodesIndex,
        'toNodes': toNodes,
        'toNodesIndex': toNodesIndex
    }
    return adjacencyTensor, extraData


def findMostSimilarNodes(adjMatrix, source, extraData, method, k=10, skipZeros=True, **kwargs):
    """
      Find the top-k most similar nodes using the given method
    """

    sourceIndex = extraData['fromNodesIndex'][source]
    toNodes = extraData['toNodes']

    # Find all similarity scores, optionally skipping nonzero scores for memory usage
    if skipZeros:
        similarityScores = {}
        for i in xrange(len(toNodes)):
            sim = method(adjMatrix, sourceIndex, i, kwargs)
            if sim > 0:
                similarityScores[toNodes[i]] = sim
    else:
        similarityScores = {toNodes[i]: method(adjMatrix, sourceIndex, i, kwargs) for i in xrange(0, len(toNodes))}

    # Sort according to most similar (descending order)
    mostSimilarNodes = sorted(similarityScores.iteritems(), key=operator.itemgetter(1))
    mostSimilarNodes.reverse()
    number = min([k, len(mostSimilarNodes)])
    mostSimilarNodes = mostSimilarNodes[:number]

    return mostSimilarNodes, similarityScores