import operator
from src.similarity.SimilarityStrategy import SimilarityStrategy
from src.util.MetaPathUtility import MetaPathUtility

__author__ = 'jontedesco'

class MetaPathSimilarityStrategy(SimilarityStrategy):
    """
      Generic class for similarity strategies that use meta paths
    """

    def __init__(self, graph, metaPath, symmetric = False):
        """
          Constructs a meta path similarity strategy, storing the meta path data for this strategy.

            @param  metaPath    Meta path object where the list of classes contains classes of nodes in the graph,
                                and weights in [0,1] containing the importance of the meta path

            @param  symmetric   Whether or not to enforce that meta paths must be symmetric

            For example, if 'symmetric' and 'evenLength' are both 'true', for meta path 'ABC', we will only count meta
            path 'ABCCBA', depending on, and if 'symmetric' is 'true' while 'evenLength' is 'false', we will only count
            meta paths 'ABCBA'
        """

        super(MetaPathSimilarityStrategy, self).__init__(graph)

        self.metaPath = metaPath
        self.symmetric = symmetric

        # Two level dictionary, indexed by nodes, giving similarity scores, of the form dict[source][destination]
        self.similarityScores = {}


    def findMostSimilarNodes(self, source, number=None):
        """
          Simple find the similarity scores between this node and all reachable nodes on this meta path. Note that if
          there are fewer reachable nodes than "number", the number of reachable nodes will be returned.
        """

        # If no number is provided, default to the number of nodes in the graph
        if number is None:
            number = self.n

        # Get similarity scores for all entries
        reachableNodes = MetaPathUtility.findMetaPathNeighbors(self.graph, source, self.metaPath)
        for reachableNode in reachableNodes:
            self.findSimilarityScore(source, reachableNode)


        # Sort by increasing score
        mostSimilarNodes = sorted(self.similarityScores[source].iteritems(), key=operator.itemgetter(1))

        # Remove source, nodes of different types, and reverse
        newMostSimilarNodes = []
        for node, score in mostSimilarNodes:
            if node != source and node.__class__ == source.__class__:
                newMostSimilarNodes.append(node)
        newMostSimilarNodes.reverse()
        number = min([number, len(newMostSimilarNodes)])
        mostSimilarNodes = newMostSimilarNodes[:number]

        return mostSimilarNodes


    def getFromCache(self, source, destination):
        if source in self.similarityScores:
            if destination in self.similarityScores[source]:
                return self.similarityScores[source][destination]


    def addToCache(self, source, destination, score):
        if source not in self.similarityScores:
            self.similarityScores[source] = {}
        self.similarityScores[source][destination] = score