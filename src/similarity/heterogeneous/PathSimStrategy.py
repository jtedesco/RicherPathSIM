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

        if self.getFromCache(source, destination) is not None:
            return self.getFromCache(source, destination)

        # Get the meta paths between the source and destination
        numSourceDestinationPaths = len(self.metaPathUtility.findMetaPaths(self.graph, source, destination, self.metaPath, True))

        # Get cycle counts
        partialMetaPath = self.metaPath[:len(self.metaPath)/2 + len(self.metaPath) % 2]
        sourceNeighbors = self.metaPathUtility.findMetaPathNeighbors(self.graph, source, partialMetaPath, True)
        destinationNeighbors = self.metaPathUtility.findMetaPathNeighbors(self.graph, source, partialMetaPath, True)
        numSourceDestinationCycles = 0
        for node, neighbors in [(source, sourceNeighbors), (destination, destinationNeighbors)]:
            for neighbor in neighbors:
                paths = self.metaPathUtility.findMetaPaths(self.graph, node, neighbor, partialMetaPath, True)
                numSourceDestinationCycles += len(paths) ** 2

        # Compute the PathSim similarity scores of the two nodes
        similarityScore = (2.0 * numSourceDestinationPaths) / float(numSourceDestinationCycles)

        self.addToCache(source, destination, similarityScore)

        return similarityScore