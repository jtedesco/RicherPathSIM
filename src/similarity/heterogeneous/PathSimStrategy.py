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

        # Get score from cache if possible
        cachedScore = self.getFromCache(source, destination)
        if cachedScore is not None:
            return cachedScore

        # Get the meta paths between the source and destination
        sourceDestinationPaths = MetaPathUtility.findMetaPaths(self.graph, source, destination, self.metaPath)
        sourceCycles = MetaPathUtility.findMetaPaths(self.graph, source, source, self.metaPath)
        destinationCycles = MetaPathUtility.findMetaPaths(self.graph, destination, destination, self.metaPath)

        # Compute the PathSim similarity scores of the two nodes
        similarityScore = (2.0 * len(sourceDestinationPaths)) / float(len(sourceCycles) + len(destinationCycles))

        self.addToCache(source, destination, similarityScore)

        return similarityScore