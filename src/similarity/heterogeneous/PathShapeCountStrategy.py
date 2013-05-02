from collections import defaultdict
import numpy
from scipy.spatial.distance import cosine
from src.similarity.MetaPathSimilarityStrategy import MetaPathSimilarityStrategy

__author__ = 'jontedesco'


class WeightedPathShapeCount(MetaPathSimilarityStrategy):
    """
      Class that performs similarity on the path counts to shared neighbors
    """

    def __init__(self, graph, weight=1.0, metaPath=None, symmetric=False, vectorSimilarity=None):
        super(WeightedPathShapeCount, self).__init__(graph, metaPath, symmetric)
        self.similarityScores = defaultdict(dict)
        self.vectorSimilarity = self.__pathsimSimilarity if vectorSimilarity is None else vectorSimilarity
        self.weight = weight

    def findSimilarityScore(self, source, destination):
        """
          Compute the path shape count similarity, by using path sequences from shared neighbors to source & destination
        """

        if destination in self.similarityScores[source]:
            return self.similarityScores[source][destination]

        # Find shared neighbors
        cppaProjectedGraph = self.metaPathUtility.createHeterogeneousProjection(self.graph, self.metaPath)
        sourceInMetaNeighbors = set(cppaProjectedGraph.getPredecessors(source))
        destinationInMetaNeighbors = set(cppaProjectedGraph.getPredecessors(destination))
        allNeighbors = sourceInMetaNeighbors.union(destinationInMetaNeighbors)
        sharedInNeighbors = sourceInMetaNeighbors.intersection(destinationInMetaNeighbors)

        # Path count sequences and normalized sequences
        sourceSequences, destinationSequences = [], []
        normalizedSourceSequences, normalizedDestinationSequences = [], []

        for neighbor in allNeighbors:

            # Tally this as a zero, since one has it and the other doesn't
            if neighbor not in sharedInNeighbors:
                for sequences in [sourceSequences, destinationSequences,
                                  normalizedSourceSequences, normalizedDestinationSequences]:
                    sequences.append([0.0] * len(self.metaPath))
                continue

            # Otherwise, get the path sequence from this neighbor to each node and the corresponding unit vectors
            newSourceSequence = self.__pathSequence(neighbor, source)
            newDestinationSequence = self.__pathSequence(neighbor, destination)
            normalizedSourceSequence = [el / float(sum(newSourceSequence)) for el in newSourceSequence]
            normalizedDestinationSequence = [el / float(sum(newDestinationSequence)) for el in newDestinationSequence]

            sourceSequences.append(newSourceSequence)
            destinationSequences.append(newDestinationSequence)
            normalizedSourceSequences.append(normalizedSourceSequence)
            normalizedDestinationSequences.append(normalizedDestinationSequence)

        # Form the two matrices and flatten them into two vectors
        sourceMatrix = numpy.array(sourceSequences, dtype=object)
        destinationMatrix = numpy.array(destinationSequences, dtype=object)
        sourceVector = numpy.hstack(sourceMatrix)
        destinationVector = numpy.hstack(destinationMatrix)

        # Form the two normalized matrices and flatten them into two vectors
        normalizedSourceMatrix = numpy.array(normalizedSourceSequences, dtype=object)
        normalizedDestinationMatrix = numpy.array(normalizedDestinationSequences, dtype=object)
        normalizedSourceVector = numpy.hstack(normalizedSourceMatrix)
        normalizedDestinationVector = numpy.hstack(normalizedDestinationMatrix)

        # Weight the absolute and relative similarity scores together
        absSim = self.vectorSimilarity(self.graph, sourceVector, destinationVector)
        relSim = self.vectorSimilarity(self.graph, normalizedSourceVector, normalizedDestinationVector)
        self.similarityScores[source][destination] = (self.weight * absSim) + ((1 - self.weight) * relSim)

        return self.similarityScores[source][destination]

    def __pathSequence(self, source, destination):
        """
          Get the path count sequence between the two nodes along the meta path in the graph, using edge counts only.

            @source         The source object
            @destination    The destination object
            @return         A numpy vector of the sequence
        """

        edgeCuts = []
        metaPathInstances = self.metaPathUtility.findMetaPaths(self.graph, source, destination, self.metaPath)
        for i in xrange(0, len(self.metaPath)-1):
            edgePairs = {(pathInstance[i], pathInstance[i+1]) for pathInstance in metaPathInstances}
            edgeCuts.append(len(edgePairs))

        return numpy.array(edgeCuts)

    def __pathsimSimilarity(self, _, vectorA, vectorB):
        """
          Normalized cosine similarity as computed by PathSim
        """
        return round(2 * vectorA.dot(vectorB) / float(vectorA.dot(vectorA) + vectorB.dot(vectorB)), 2)