import networkx
from src.similarity.SimilarityStrategy import SimilarityStrategy

__author__ = 'jontedesco'

class PageRankStrategy(SimilarityStrategy):
    """
      Implementation of personal PageRank strategy for node similarity in a homogeneous graph. Simply performs PageRank
      on graph reachable from a given node
    """

    def __init__(self, graph):
        super(PageRankStrategy, self).__init__(graph)

        # Dictionary indexed by graph nodes, where each entry is a dictionary of similarity scores in [0,1] between that
        # node and reachable nodes in the graph
        self.similarityScores = {}


    def findSimilarityScore(self, source, destination):
        """
          Return the similarity score in [0,1] between the source and destination nodes in the graph
        """

        # Just return pre-computed value if possible
        if source in self.similarityScores:
            return self.__getSimilarityScore(source, destination)

        # Perform PageRank on the subgraph reachable from the source
        self.__computeSimilarityScores(source)

        return self.__getSimilarityScore(source, destination)


    def findMostSimilarNodes(self, node, number=5):

        if node not in self.similarityScores:
            self.__computeSimilarityScores(node)

        return super(PageRankStrategy, self).findMostSimilarNodes(node, number)


    def __computeSimilarityScores(self, source):
        """
          Compute the similarity scores for all reachable nodes from the source node in the graph
        """

        subgraph = networkx.bfs_tree(self.graph, source)
        self.similarityScores[source] = networkx.pagerank_numpy(subgraph)


    def __getSimilarityScore(self, source, destination):
        """
          Get a similarity score between two nodes, assuming it has already been computed
        """

        if destination in self.similarityScores[source]:
            return self.similarityScores[source][destination]
        else:
            return 0