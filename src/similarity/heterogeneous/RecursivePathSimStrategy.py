import operator
from itertools import product

import numpy

from src.similarity.MetaPathSimilarityStrategy import MetaPathSimilarityStrategy


__author__ = 'jontedesco'


class RecursivePathSimStrategy(MetaPathSimilarityStrategy):
    """
      Class that calculates a SimRank / PathSim amalgamation

        NOTE: Assumes meta paths are specified in the half-length format, with shared neighbors first
    """

    def __init__(self, graph, metaPath=None, symmetric=False, k=None, compositionFunction=None):
        super(RecursivePathSimStrategy, self).__init__(graph, metaPath, symmetric)

        # Default the composition function to be multiplication
        self.compositionFunction = operator.mul if compositionFunction is None else compositionFunction

        # Default the k-length recursive limit to the length of the meta path
        self.k = len(metaPath) if k is None else k

    # Cache of projected adjacency matrices (map from meta path -> (adjacency matrix, adjacency index))
    __projectedGraphCache = {}

    def findSimilarityScore(self, source, destination):
        return self.__findSimilarityScoreHelper(source, destination, self.metaPath, self.k - 1)

    def __findSimilarityScoreHelper(self, source, destination, metaPath, iterationsRemaining):
        """
          Recursive helper to calculate the similarity score between two objects
        """

        if len(metaPath) <= 1:
            return 1 if (source == destination) else 0

        # Calculate initial similarity score, based on the current meta path
        initialScore = self.__pathSimSimilarityHelper(source, destination, metaPath)

        # Abort if we've reached the limit for recursion
        if iterationsRemaining == 0:
            return initialScore

        # Get neighbors and meta path for next iteration
        nextMetaPath = metaPath[:-1]
        sourceNeighbors = self.graph.getPredecessorsOfType(source, nextMetaPath[-1])
        destinationNeighbors = self.graph.getPredecessorsOfType(destination, nextMetaPath[-1])

        # Calculate the recursive score for partial meta path
        totalSimilarity = 0.0
        for sourceNeighbor, destinationNeighbor in product(sourceNeighbors, destinationNeighbors):
            totalSimilarity += self.__findSimilarityScoreHelper(
                sourceNeighbor, destinationNeighbor, nextMetaPath, iterationsRemaining - 1)
        averageSimilarity = totalSimilarity / (len(sourceNeighbors) * len(destinationNeighbors))

        # Use the provided function to compose this similarity score with neighbors' average scores
        similarityScore = self.compositionFunction(initialScore, averageSimilarity)

        return similarityScore

    def __pathSimSimilarityHelper(self, source, destination, metaPath):
        """
          Get the PathSim similarity between two objects, given a particular meta path
        """

        # Cache the projected graph to avoid recomputation
        if tuple(metaPath) in RecursivePathSimStrategy.__projectedGraphCache:
            adjMatrix, adjIndex = RecursivePathSimStrategy.__projectedGraphCache[tuple(metaPath)]
        else:
            adjMatrix, adjIndex = self.metaPathUtility.getAdjacencyMatrixFromGraph(
                self.graph, metaPath, project=True, symmetric=False
            )
            RecursivePathSimStrategy.__projectedGraphCache[tuple(metaPath)] = (adjMatrix, adjIndex)

        transpAdjMatrix = adjMatrix.transpose()
        sourceColumn = transpAdjMatrix[adjIndex[source]]
        destColumn = transpAdjMatrix[adjIndex[destination]]

        total = 2 * numpy.dot(destColumn.transpose(), sourceColumn)
        sourceNormalization = numpy.dot(sourceColumn.transpose(), sourceColumn)
        destNormalization = numpy.dot(destColumn.transpose(), destColumn)

        similarityScore = total
        if total > 0:
            similarityScore = total / float(sourceNormalization + destNormalization)

        return similarityScore