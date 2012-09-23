from src.similarity.SimilarityStrategy import SimilarityStrategy

__author__ = 'jontedesco'

class MetaPathSimilarityStrategy(SimilarityStrategy):
    """
      Generic class for similarity strategies that use meta paths
    """

    def __init__(self, metaPaths):
        """
          Constructs a meta path similarity strategy, storing the meta path data for this strategy.

            @param  metaPaths   A list of meta path data, where each entry is a tuple of a list of classes and a weight,
                                where the list of classes contains classes of nodes in the graph, and weights in [0,1]
                                containing the importance of the meta path
        """

        super(MetaPathSimilarityStrategy, self).__init__()

        self.metaPaths = metaPaths