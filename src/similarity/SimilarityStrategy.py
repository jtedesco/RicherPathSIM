from collections import defaultdict

__author__ = 'jontedesco'

class SimilarityStrategy(object):
    """
      Generic class for graph node similarity
    """

    def __init__(self, graph):
        self.graph = graph
        self.n = len(graph.getNodes())

        # Two level dictionary, indexed by nodes, giving similarity scores, of the form dict[source][destination]
        self.similarityScores = defaultdict(lambda: defaultdict(int))


    def findSimilarityScore(self, source, destination):
        """
          Find the similarity score between two nodes (score may or may not be symmetric)
        """
        raise NotImplementedError()


    def findMostSimilarNodes(self, node, number=None):
        """
          Find the most similar nodes to some given node

            @param  node    The node for which to find the most similar other nodes in the graph
            @param  number  The number of similar nodes to find
        """
        raise NotImplementedError()


    def findSimilarityScores(self, source, destinations):
        """
          Find the similarity scores between a source and a list of destination, and normalize these scores by the
          maximum score for any destination
        """
        return [self.findSimilarityScore(source, destination) for destination in destinations]
