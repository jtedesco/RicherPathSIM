import operator
from src.similarity.SimilarityStrategy import SimilarityStrategy

__author__ = 'jontedesco'

class PageRankStrategy(SimilarityStrategy):
    """
      Implementation of personal PageRank strategy for node similarity in a homogeneous graph. Simply performs PageRank
      on graph reachable from a given node.
    """

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


    def findMostSimilarNodes(self, source, number=5):

        if source not in self.similarityScores:
            self.__computeSimilarityScores(source)

        # Sort by increasing score
        mostSimilarNodes = sorted(self.similarityScores[source].iteritems(), key=operator.itemgetter(1))

        # Remove source, nodes of different types, and reverse
        newMostSimilarNodes = []
        for node, score in mostSimilarNodes:
            if node != source and node.__class__ == source.__class__:
                newMostSimilarNodes.append(node)
        mostSimilarNodes = newMostSimilarNodes[-1 * number:]

        return mostSimilarNodes


    def __computeSimilarityScores(self, source):
        """
          Compute the similarity scores for all reachable nodes from the source node in the graph
        """

        subgraph = self.graph.breadthFirstSearch(source)
        self.similarityScores[source] = subgraph.pageRank()

        return self.similarityScores[source]


    def __getSimilarityScore(self, source, destination):
        """
          Get a similarity score between two nodes, assuming it has already been computed
        """

        if destination in self.similarityScores[source]:
            return self.similarityScores[source][destination]
        else:
            return 0