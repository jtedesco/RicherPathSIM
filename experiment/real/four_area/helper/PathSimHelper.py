import operator

from networkx import MultiDiGraph
from scipy.sparse import lil_matrix
import texttable
from experiment.real.four_area.helper.MetaPathHelper import getMetaPathAdjacencyData


__author__ = 'jontedesco'

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
        similarityScore = total / float(sourceNormalization + destNormalization)

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

# When run as script, runs through pathsim papers example experiment
if __name__ == '__main__':
   pathSimPaperExample()
