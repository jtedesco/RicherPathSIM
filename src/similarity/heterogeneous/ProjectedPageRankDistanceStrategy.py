from src.similarity.MetaPathSimilarityStrategy import MetaPathSimilarityStrategy

__author__ = 'jontedesco'

class ProjectedPageRankDistanceStrategy(MetaPathSimilarityStrategy):
    """
      Class that computes the absolute difference between the PageRank of two nodes
    """

    def findSimilarityScore(self, source, destination):
        """
          Find the similarity score between
        """

        if self.getFromCache(source, destination) is not None:
            return self.getFromCache(source, destination)

        # Project graph
        if self.metaPath[0] == self.metaPath[-1]: # Homogeneous projection?
            projectedGraph = self.metaPathUtility.createHomogeneousProjection(self.graph, self.metaPath)
        else:
            projectedGraph = self.metaPathUtility.createHeterogeneousProjection(self.graph, self.metaPath)

        # Calculate PageRank in network (default alpha & no personalization)
        pageRanks = projectedGraph.pageRank()
        similarityScore = abs(pageRanks[source] - pageRanks[destination])

        self.addToCache(source, destination, similarityScore)

        return similarityScore