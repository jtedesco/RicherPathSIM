__author__ = 'jontedesco'

class SimilarityStrategy(object):
    """
      Generic class for graph node similarity
    """

    def __init__(self, graph):
        self.graph = graph
        self.n = len(graph.getNodes())

        # Two level dictionary, indexed by nodes, giving similarity scores, of the form dict[source][destination]
        self.similarityScores = {}


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


    def getFromCache(self, source, destination):
        if source in self.similarityScores:
            if destination in self.similarityScores[source]:
                return self.similarityScores[source][destination]


    def addToCache(self, source, destination, score):
        if source not in self.similarityScores:
            self.similarityScores[source] = {}
        self.similarityScores[source][destination] = score