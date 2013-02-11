import numpy
from src.similarity.MetaPathSimilarityStrategy import MetaPathSimilarityStrategy

__author__ = 'jontedesco'

class PathSimStrategy(MetaPathSimilarityStrategy):
    """
      Class that implements the PathSim similarity measure for same-typed nodes on heterogeneous graphs. Based on
      publication by Yizhou Sun et al. NOTE: This assumes that any given meta path is symmetric.

        @see    http://citeseer.ist.psu.edu/viewdoc/summary?doi=10.1.1.220.2455
    """

    def findSimilarityScore(self, source, destination):
        """
          Find the similarity score between
        """

        partialMetaPath = self.metaPath[:len(self.metaPath)/2 + len(self.metaPath) % 2]

        # Get the number of meta paths between source and destination
        if self.conserveMemory:

            # Slow, but less in-memory storage
            numSourceDestinationPaths = len(self.metaPathUtility.findMetaPaths(self.graph, source, destination, self.metaPath, True))

        else:

            # Faster, but requires more memory
            firstHalfAdjMatrix, firstHalfIndex = self.metaPathUtility.getAdjacencyMatrixFromGraph(
                self.graph, partialMetaPath, project=True, symmetric=True)
            secHalfAdjMatrix, secHalfIndex = self.metaPathUtility.getAdjacencyMatrixFromGraph(
                self.graph, list(reversed(partialMetaPath)), project=True, symmetric=True)
            adjMatrix = numpy.dot(firstHalfAdjMatrix, secHalfAdjMatrix)
            numSourceDestinationPaths = adjMatrix[firstHalfIndex[source]][secHalfIndex[destination]]

        # Get cycle counts
        sourceNeighbors = self.metaPathUtility.findMetaPathNeighbors(self.graph, source, partialMetaPath, True)
        destinationNeighbors = self.metaPathUtility.findMetaPathNeighbors(self.graph, destination, partialMetaPath, True)
        numSourceDestinationCycles = 0
        for node, neighbors in [(source, sourceNeighbors), (destination, destinationNeighbors)]:
            for neighbor in neighbors:
                paths = self.metaPathUtility.findMetaPaths(self.graph, node, neighbor, partialMetaPath, True)
                numSourceDestinationCycles += len(paths) ** 2

        # Compute the PathSim similarity scores of the two nodes
        similarityScore = (2.0 * numSourceDestinationPaths) / float(numSourceDestinationCycles)

        return similarityScore