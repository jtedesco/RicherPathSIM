from src.similarity.heterogeneous.GlobalInfluenceDistanceStrategy import GlobalInfluenceDistanceStrategy

__author__ = 'jontedesco'

class PageRankDistanceStrategy(GlobalInfluenceDistanceStrategy):
    """
      Class that computes the absolute difference between some influence measure of nodes
    """

    def getGlobalInfluenceMeasure(self, projectedGraph):

        # Calculate PageRank in network (default alpha & no personalization)
        return projectedGraph.pageRank()
