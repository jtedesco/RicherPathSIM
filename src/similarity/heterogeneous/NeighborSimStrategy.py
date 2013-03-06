import numpy
from src.similarity.MetaPathSimilarityStrategy import MetaPathSimilarityStrategy

__author__ = 'jontedesco'

class NeighborSimStrategy(MetaPathSimilarityStrategy):
    """
      Class that implements a meta-neighbor based similarity strategy, that counts half-paths, not necessarily connecting
      the two nodes, but connecting to shared neighbors.
    """

    def __init__(self, graph, metaPath=None, symmetric=False, reversed=False, smoothed=False, commonNeighbors=True):
        super(NeighborSimStrategy, self).__init__(graph, metaPath, symmetric)
        self.reversed = reversed
        self.smoothed = smoothed

        # Flag to control whether or not the neighbors must be 'common' neighbors
        # (if false, just uses differences in neighbor counts)
        self.commonNeighbors = commonNeighbors

    def findSimilarityScore(self, source, destination):
        """
          Find the similarity score between two nodes
        """

        # Project graph
        adjMatrix, adjIndex = self.metaPathUtility.getAdjacencyMatrixFromGraph(
            self.graph, self.metaPath, project=True, symmetric=self.symmetric
        )

        # Consider the reverse meta path if flag is enabled
        if self.reversed:
            adjMatrix = adjMatrix.transpose()

        transpAdjMatrix = adjMatrix.transpose()
        sourceColumn = transpAdjMatrix[adjIndex[source]]
        destColumn = transpAdjMatrix[adjIndex[destination]]

        # Compute numerator dot product
        total = 1 if self.smoothed else 0
        if self.commonNeighbors:
            total += numpy.dot(destColumn.transpose(), sourceColumn)
            total *= 2
        else:
            destNorm = numpy.dot(destColumn.transpose(), destColumn)
            sourceNorm = numpy.dot(sourceColumn.transpose(), sourceColumn)
            total += 2 * (max(destNorm, sourceNorm) - abs(destNorm - sourceNorm))

        # Compute normalization dot products
        sourceNormalization = 1 if self.smoothed else 0
        sourceNormalization += numpy.dot(sourceColumn.transpose(), sourceColumn)
        destNormalization = 1 if self.smoothed else 0
        destNormalization += numpy.dot(destColumn.transpose(), destColumn)

        similarityScore = total
        if total > 0:
            similarityScore = total / float(sourceNormalization + destNormalization)

        return similarityScore