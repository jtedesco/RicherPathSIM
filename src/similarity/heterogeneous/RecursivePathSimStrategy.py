from collections import defaultdict
from datetime import datetime
from itertools import product
import numpy
from scipy.spatial.distance import cosine
from whoosh.query import Term
from src.model.node.dblp.Author import Author
from src.model.node.dblp.Conference import Conference
from src.model.node.dblp.Paper import Paper
from src.similarity.MetaPathSimilarityStrategy import MetaPathSimilarityStrategy
from src.similarity.heterogeneous.NeighborSimStrategy import NeighborSimStrategy

__author__ = 'jontedesco'

def print_metapath(metaPath):

    replacements = {
        Conference: 'C',
        Author: 'A',
        Paper: 'P',
        Term: 'T'
    }
    return [replacements[t] for t in metaPath]



class RecursivePathSimStrategy(MetaPathSimilarityStrategy):
    """
      Class that calculates a SimRank / PathSim amalgamation

        NOTE: Assumes meta paths are specified in the half-length format, with shared neighbors first
    """

    # Cache of similarity strategies, to avoid object creation
    __neighborSimStrategyCache = {}

    def findSimilarityScore(self, source, destination):
        return self.__findSimilarityScoreHelper(source, destination, self.metaPath)

    def __findSimilarityScoreHelper(self, source, destination, metaPath):
        """
          Recursive helper to calculate the similarity score between two objects
        """

        print print_metapath(metaPath), tuple([(x.name if 'name' in x.toDict() else x.title) for x in (source, destination)])

        if len(metaPath) <= 1:
            return 1 if (source == destination) else 0

        # Calculate initial similarity score, based on the current meta path
        initialScore = self.__getNeighborSimStrategy(metaPath).findSimilarityScore(source, destination)

        # Get neighbors and meta path for next iteration
        nextMetaPath = metaPath[:-1]
        sourceNeighbors = self.graph.getPredecessorsOfType(source, nextMetaPath[-1])
        destinationNeighbors = self.graph.getPredecessorsOfType(destination, nextMetaPath[-1])

        # Calculate the recursive score for partial meta path
        totalSimilarity = 0.0
        for sourceNeighbor, destinationNeighbor in product(sourceNeighbors, destinationNeighbors):
            totalSimilarity += self.__findSimilarityScoreHelper(sourceNeighbor, destinationNeighbor, nextMetaPath)
        averageSimilarity = totalSimilarity / (len(sourceNeighbors) * len(destinationNeighbors))

        similarityScore = initialScore * averageSimilarity

        return similarityScore

    def __getNeighborSimStrategy(self, metaPath):
        metaPath = tuple(metaPath)
        if metaPath in RecursivePathSimStrategy.__neighborSimStrategyCache:
            return RecursivePathSimStrategy.__neighborSimStrategyCache[metaPath]
        return NeighborSimStrategy(self.graph, metaPath)