from scipy.sparse import csr_matrix, csc_matrix

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


def getMetaPathAdjacencyData(graph, nodeIndex, metaPath, rows=False):
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
    data, row, col = [], [], []
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