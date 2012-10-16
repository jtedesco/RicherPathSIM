from src.similarity.MetaPathSimilarityStrategy import MetaPathSimilarityStrategy
from src.util.MetaPathUtility import MetaPathUtility

__author__ = 'jontedesco'

class PathSimStrategy(MetaPathSimilarityStrategy):
    """
      Class that implements the PathSim similarity measure for same-typed nodes on heterogeneous graphs. Based on
      publication by Yizhou Sun et al.

        @see    http://citeseer.ist.psu.edu/viewdoc/summary?doi=10.1.1.220.2455
    """

    def findSimilarityScore(self, source, destination):
        """
          Find the similarity score between
        """

        if self.getFromCache(source, destination) is not None:
            return self.getFromCache(source, destination)

        # Get the meta paths between the source and destination
        numSourceDestinationPaths = len(MetaPathUtility.findMetaPaths(self.graph, source, destination, self.metaPath, True))

        # Get cycle counts
        numSourceCycles = len(MetaPathUtility.findMetaPaths(self.graph, source, source, self.metaPath))
        numDestinationCycles = len(MetaPathUtility.findMetaPaths(self.graph, destination, destination, self.metaPath))

        # Compute the PathSim similarity scores of the two nodes
        similarityScore = (2.0 * numSourceDestinationPaths) / float(numDestinationCycles + numSourceCycles)

        self.addToCache(source, destination, similarityScore)

        return similarityScore