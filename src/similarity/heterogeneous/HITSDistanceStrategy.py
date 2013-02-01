from src.similarity.heterogeneous.GlobalInfluenceDistanceStrategy import GlobalInfluenceDistanceStrategy

__author__ = 'jontedesco'

class HITSDistanceStrategy(GlobalInfluenceDistanceStrategy):
    """
      Class that computes the absolute difference of HITS scores between some influence measure of nodes
    """

    def getGlobalInfluenceMeasure(self, projectedGraph):

        # Calculate HITS in network & combine into vectors
        h,a = projectedGraph.hits()
        scores = {}
        for key in h:
            scores[key] = [h[key], a[key]]
        return scores
