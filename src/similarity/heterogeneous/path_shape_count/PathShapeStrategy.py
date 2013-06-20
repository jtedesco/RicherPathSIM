from collections import defaultdict
import numpy
from src.similarity.MetaPathSimilarityStrategy import MetaPathSimilarityStrategy

__author__ = 'jontedesco'


class PathShapeStrategy(MetaPathSimilarityStrategy):
    """
      Abstract class that performs similarity on the path shape to shared neighbors
    """

    def __init__(self, graph, weight=1.0, omit=list(), metaPath=None, symmetric=False, vectorSimilarity=None):
        super(PathShapeStrategy, self).__init__(graph, metaPath, symmetric)
        self.similarityScores = defaultdict(dict)
        self.vectorSimilarity = self.__pathsimSimilarity if vectorSimilarity is None else vectorSimilarity
        self.weight = weight
        self.omit = omit

    def findSimilarityScore(self, source, destination):
        """
          Compute the path shape count similarity, by using path sequences from shared neighbors to source & destination
        """

        if destination in self.similarityScores[source]:
            return self.similarityScores[source][destination]

        # Find shared neighbors
        projectedGraph = self.metaPathUtility.createHeterogeneousProjection(self.graph, self.metaPath)
        sourceInMetaNeighbors = set(projectedGraph.getPredecessors(source))
        destinationInMetaNeighbors = set(projectedGraph.getPredecessors(destination))
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
                    sequences.append([0.0] * (len(self.metaPath) - len(self.omit)))
                continue

            # Get the path sequence vectors for source & destination
            newSourceSequence = self.__pathSequence(neighbor, source)
            newDestinationSequence = self.__pathSequence(neighbor, destination)

            # Remove the indices to ignore
            for omitI in self.omit:
                del newSourceSequence[omitI]
                del newDestinationSequence[omitI]

            # Create the normalized
            normalizedSourceSequence = [el / float(sum(newSourceSequence)) for el in newSourceSequence]
            normalizedDestinationSequence = [el / float(sum(newDestinationSequence)) for el in newDestinationSequence]

            sourceSequences.append(newSourceSequence)
            destinationSequences.append(newDestinationSequence)
            normalizedSourceSequences.append(normalizedSourceSequence)
            normalizedDestinationSequences.append(normalizedDestinationSequence)

        # Form the two matrices original and two normalized matrices
        sourceMatrix = numpy.array(sourceSequences, dtype=object)
        destinationMatrix = numpy.array(destinationSequences, dtype=object)
        normalizedSourceMatrix = numpy.array(normalizedSourceSequences, dtype=object)
        normalizedDestinationMatrix = numpy.array(normalizedDestinationSequences, dtype=object)

        # Get the similarity
        self.similarityScores[source][destination] = self.getSimilarityScoreFromMatrices(
            sourceMatrix, destinationMatrix, normalizedSourceMatrix, normalizedDestinationMatrix
        )

        return self.similarityScores[source][destination]

    def getSimilarityScoreFromMatrices(self, sourceMatrix, destinationMatrix,
                                       normalizedDestinationMatrix, normalizedSourceMatrix):
        """
          Get the similarity score given the original and normalized matrices for each of the source and destination
        """

        raise NotImplementedError()

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

        return edgeCuts

    def __pathsimSimilarity(self, _, vectorA, vectorB):
        """
          Normalized cosine similarity as computed by PathSim
        """
        num = 2 * vectorA.dot(vectorB)
        if num == 0:
            return 0
        return round(num / float(vectorA.dot(vectorA) + vectorB.dot(vectorB)), 2)