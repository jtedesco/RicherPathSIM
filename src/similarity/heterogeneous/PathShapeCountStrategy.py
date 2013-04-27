from collections import defaultdict
import numpy
from scipy.spatial.distance import cosine
from src.similarity.MetaPathSimilarityStrategy import MetaPathSimilarityStrategy

__author__ = 'jontedesco'


class NeighborPathShapeCount(MetaPathSimilarityStrategy):
    """
      Class that performs similarity on the path counts to shared neighbors
    """

    def __init__(self, graph, metaPath=None, symmetric=False, pathCountSimilarity=None, aggregateSimilarity=None):
        super(NeighborPathShapeCount, self).__init__(graph, metaPath, symmetric)
        self.similarityScores = defaultdict(dict)
        self.pathSequenceSimilarity = self.__pathsimSimilarity if pathCountSimilarity is None else pathCountSimilarity
        self.aggregateSimilarity = (lambda v: sum(v) / float(len(v))) if aggregateSimilarity is None else aggregateSimilarity

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

        # Find path count sequences from all shared neighbors to each object
        sequenceSimilarities = []
        for neighbor in allNeighbors:

            # Tally this as a zero, since one has it and the other doesn't
            if neighbor not in sharedInNeighbors:
                sequenceSimilarities.append(0.0)
                continue

            # Otherwise, get the path sequence from this neighbor to each node, and find the cosine similarity
            sourcePathSequence = self.__pathSequence(neighbor, source)
            destinationPathSequence = self.__pathSequence(neighbor, destination)
            sequenceSimilarities.append(
                self.pathSequenceSimilarity(self.graph, sourcePathSequence, destinationPathSequence)
            )

        self.similarityScores[source][destination] = self.aggregateSimilarity(sequenceSimilarities)
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

    def __cosineSimilarity(self, _, vectorA, vectorB):
        """
          Default cosine similarity between two numpy vectors
        """
        return round(1 - cosine(vectorA, vectorB), 2)


    def __pathsimSimilarity(self, _, vectorA, vectorB):
        """
          Normalized cosine similarity as computed by PathSim
        """
        return round(2 * vectorA.dot(vectorB) / float(vectorA.dot(vectorA) + vectorB.dot(vectorB)), 2)