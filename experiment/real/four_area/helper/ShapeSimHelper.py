from collections import defaultdict
import itertools
from networkx import MultiDiGraph
from scipy.sparse import csc_matrix
import texttable
from experiment.real.four_area.helper.MetaPathHelper import getMetaPathAdjacencyData, getMetaPathAdjacencyTensorData
from experiment.real.four_area.helper.PathSimHelper import getNeighborSimScore, findMostSimilarNodes

__author__ = 'jontedesco'


def getShapeSimScore(adjacencyTensor, xI, yI, alpha=1.0, omit=list()):
    """
      Calculate the ShapeSim score on the given tensor

        @adjacencyTensor    The 3-dimensional tensor with path information
        @alpha              The weight in [0,1] of the 'absolute' similarity score, accounting for vector magnitude
    """

    # Configure based on tensor
    numTensorRows = adjacencyTensor.shape[0]
    metaPathLength = adjacencyTensor.shape[2]
    vectorsIndices = list(xrange(0, metaPathLength-1))
    vectorsIndices = [i for i in vectorsIndices if i not in omit]

    # Build the non-normalized matrices for x and y
    xRows, xCols, xData = [], [], []
    yRows, yCols, yData = [], [], []
    xPathSums, yPathSums = defaultdict(int), defaultdict(int)  # Maps of row to sum of path counts for each vector
    for i, j in itertools.product(xrange(0, numTensorRows), vectorsIndices):
        xEntry = adjacencyTensor[i, xI, j]
        if xEntry > 0:
            xRows.append(i)
            xCols.append(j)
            xData.append(xEntry)
            xPathSums[i] += xEntry
        yEntry = adjacencyTensor[i, yI, j]
        if yEntry > 0:
            yRows.append(i)
            yCols.append(j)
            yData.append(yEntry)
            yPathSums[i] += yEntry
    xMatrix = csc_matrix((xData, (xRows, xCols)), shape=(numTensorRows, metaPathLength))
    yMatrix = csc_matrix((yData, (yRows, yCols)), shape=(numTensorRows, metaPathLength))

    # Build the normalized matrices
    normalizedXData = [xData[i] / float(xPathSums[xRows[i]]) for i in xrange(0, len(xData))]
    normalizedYData = [yData[i] / float(yPathSums[yRows[i]]) for i in xrange(0, len(yData))]
    normalizedXMatrix = csc_matrix((normalizedXData, (xRows, xCols)), shape=(numTensorRows, metaPathLength))
    normalizedYMatrix = csc_matrix((normalizedYData, (yRows, yCols)), shape=(numTensorRows, metaPathLength))

    # Normalized cosine similarity (PathSim score)
    normalizedCosineScore = lambda u, v: round((2 * u.dot(v)[0, 0]) / float(u.dot(u)[0, 0] + v.dot(v)[0, 0]), 2)

    # Calculate the absolute & relative similarity using the product of similarity along each step (vector product)
    absSim, relSim = 1, 1
    for i in vectorsIndices:
        absSim *= normalizedCosineScore(xMatrix.getcol(i), yMatrix.getcol(i))
        relSim *= normalizedCosineScore(normalizedXMatrix.getcol(i), normalizedYMatrix.getcol(i))

    return (alpha * absSim) + ((1 - alpha) * relSim)


def imbalancedCitationsPublicationsExample():
    """
      Illustrative example of imbalanced citations / publications to verify ShapeSim is working correctly
    """

    graph = MultiDiGraph()
    authors = ['Alice', 'Bob', 'Carol', 'Dave', 'Ed', 'Frank']
    conference = 'KDD'

    # Citation & publication count configuration
    citationsPublications = {
        'Alice': (100, 10),
        'Bob': (80, 10),
        'Carol': (100, 100),
        'Dave': (50, 10),
        'Ed': (10, 10),
        'Frank': (1000, 100)
    }

    actualCitationsPublications = defaultdict(lambda: (0, 0))

    # Helper functions for repeatedly adding papers to the graph
    addPapersToAuthor = lambda n, author: [addPublicationPaper(author) for _ in itertools.repeat(None, n)]
    addCitationsToPaper = lambda n, paper, author: [addCitationPaper(paper, author) for _ in itertools.repeat(None, n)]

    # Helper for getting the next id
    def __getNextId():
        global nextId
        oldId = nextId
        nextId += 1
        return oldId

    def addPublicationPaper(author):
        """
          Helper method to add a 'publication' paper, connected to both an author and a conference
        """
        paper = "%s's Paper %d" % (author, (__getNextId()))
        graph.add_node(paper)
        graph.add_edges_from([(author, paper), (paper, author), (paper, conference), (conference, paper)])

        citationCount, publicationCount = actualCitationsPublications[author]
        actualCitationsPublications[author] = (citationCount, publicationCount + 1)

        return paper

    def addCitationPaper(citedPaper, citedAuthor):
        """
          Helper method to add a 'citation' paper, which is only connected to the conference and the paper it cites
        """
        citingPaper = "Citing Paper %d" % __getNextId()
        graph.add_node(citingPaper)
        graph.add_edges_from([(conference, citingPaper), (citingPaper, conference), (citingPaper, citedPaper)])

        citationCount, publicationCount = actualCitationsPublications[citedAuthor]
        actualCitationsPublications[citedAuthor] = (citationCount + 1, publicationCount)

        return citingPaper

    allPapers = []

    # Construct the graph
    graph.add_nodes_from(authors + [conference])
    for authorName in citationsPublications:
        citationCount, publicationCount = citationsPublications[authorName]

        # Add citations & publications to author
        authorPapers = addPapersToAuthor(publicationCount, authorName)
        allPapers.extend(authorPapers)
        citationsPerPaper = citationCount / publicationCount
        for paper in authorPapers:
            citingPapers = addCitationsToPaper(citationsPerPaper, paper, authorName)
            allPapers.extend(citingPapers)

    nodeIndex = {
        'paper': {i: allPapers[i] for i in xrange(0, len(allPapers))},
        'conference': {0: 'KDD'},
        'author': {0: 'Alice', 1: 'Bob', 2: 'Carol', 3: 'Dave', 4: 'Ed', 5: 'Frank'}
    }

    # Test PathSim / NeighborSim
    cpaAdjMatrix, extraData = getMetaPathAdjacencyData(graph, nodeIndex, ['conference', 'paper', 'author'])
    extraData['fromNodes'] = extraData['toNodes']
    extraData['fromNodesIndex'] = extraData['toNodesIndex']
    neighborSimMostSimilar, similarityScores = findMostSimilarNodes(
        cpaAdjMatrix, 'Alice', extraData, method=getNeighborSimScore
    )

    # Test ShapeSim
    cppaAdjTensor, extraData = getMetaPathAdjacencyTensorData(
        graph, nodeIndex, ['conference', 'paper', 'paper', 'author']
    )
    extraData['fromNodes'] = extraData['toNodes']
    extraData['fromNodesIndex'] = extraData['toNodesIndex']
    shapeSimMostSimilar, similarityScores = findMostSimilarNodes(
        cppaAdjTensor, 'Alice', extraData, method=getShapeSimScore, alpha=1.0
    )

    # Output similarity scores
    for name, mostSimilar in [('NeighborSim', neighborSimMostSimilar), ('ShapeSim', shapeSimMostSimilar)]:
        print('\n%s Most Similar to "%s":' % (name, 'Alice'))
        mostSimilarTable = texttable.Texttable()
        rows = [['Author', 'Score']]
        rows += [[name, score] for name, score in mostSimilar]
        mostSimilarTable.add_rows(rows)
        print(mostSimilarTable.draw())

nextId = 1

if __name__ == '__main__':
    imbalancedCitationsPublicationsExample()