from src.similarity.SimilarityStrategy import SimilarityStrategy
from src.util.MetaPathUtility import MetaPathUtility

__author__ = 'jontedesco'

class MetaPathSimilarityStrategy(SimilarityStrategy):
    """
      Generic class for similarity strategies that use meta paths
    """

    def __init__(self, graph, metaPaths, symmetric = True):
        """
          Constructs a meta path similarity strategy, storing the meta path data for this strategy.

            @param  metaPaths   A list of meta path data, where each entry is a tuple of a list of classes and a weight,
                                where the list of classes contains classes of nodes in the graph, and weights in [0,1]
                                containing the importance of the meta path

            @param  symmetric   Whether or not to interpret meta paths as truly half meta paths (i.e. if true, for meta
                                path 'ABC', we will only count meta paths 'ABCBA')
        """

        super(MetaPathSimilarityStrategy, self).__init__(graph)

        # Dictionary of meta path objects, indexed by type tuples (to ensure only one of each is included)
        self.metaPaths = metaPaths

        self.numberOfNodes = len(graph.nodes())

        # Two level dictionary, indexed by nodes, giving similarity scores, of the form dict[source][destination]
        self.similarityScores = {}


    def findSimilarityScore(self, source, destination):

        if source not in self.similarityScores:
            self.similarityScores[source] = {}

        if destination in self.similarityScores[source]:
            return self.similarityScores[source][destination]
        else:

            similarityScore = 0
            for metaPath in self.metaPaths:

                outNodes = MetaPathUtility.findMetaPathNeighbors(self.graph, source, metaPath)




    def findMostSimilarNodes(self, node, number=5):
        return super(MetaPathSimilarityStrategy, self).findMostSimilarNodes(node, number)
