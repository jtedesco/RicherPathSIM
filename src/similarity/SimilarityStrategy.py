__author__ = 'jontedesco'

class SimilarityStrategy(object):
    """
      Generic class for graph node similarity
    """

    def __init__(self, graph):
        self.graph = graph


    def findSimilarityScore(self, source, destination):
        """
          Find the similarity score between two nodes (score may or may not be symmetric)
        """

        raise NotImplementedError()


    def findMostSimilarNodes(self, node, number=5):
        """
          Find the most similar nodes to some given node

            @param  node    The node for which to find the most similar other nodes in the graph
            @param  number  The number of similar nodes to find
        """

        raise NotImplementedError()
