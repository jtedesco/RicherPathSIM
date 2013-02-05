import operator
from src.similarity.SimilarityStrategy import SimilarityStrategy

__author__ = 'jontedesco'

class AggregateSimilarityStrategy(SimilarityStrategy):
    """
      Generic class that linearly weights and combines multiple similarity strategies
    """

    def __init__(self, graph, strategies, strategyWeights):
        super(AggregateSimilarityStrategy, self).__init__(graph)

        self.strategies = strategies
        self.strategyWeights = strategyWeights


    def findSimilarityScore(self, source, destination):
        """
          Find the similarity score between two nodes
        """

        if self.getFromCache(source, destination) is not None:
            return self.getFromCache(source, destination)
        similarityScores = [strategy.findSimilarityScore(source, destination) for strategy in self.strategies]
        similarityScore = sum([weight * score for weight, score in zip(self.strategyWeights, similarityScores)])
        self.addToCache(source, destination, similarityScore)

        return similarityScore


    def findMostSimilarNodes(self, node, number=None):
        """
          Find the most similar nodes, assuming that the most similar nodes are in the most similar nodes of at least
          one of the most similar nodes of the inner strategies.
        """

        # Compute similarity scores for all of the "most similar" nodes according to any sub-strategy
        nodesToConsider = set()
        for strategy in self.strategies:
            nodesToConsider = nodesToConsider.union(set(strategy.findMostSimilarNodes(node, number)))
        for otherNode in nodesToConsider:
            self.findSimilarityScore(node, otherNode)

        # Sort by increasing score
        mostSimilarNodes = sorted(self.similarityScores[node].iteritems(), key=operator.itemgetter(1))

        # Remove source, nodes of different types, and reverse
        newMostSimilarNodes = []
        for node, score in mostSimilarNodes:
            if node != node and node.__class__ == node.__class__:
                newMostSimilarNodes.append(node)
        newMostSimilarNodes.reverse()
        number = min([number, len(newMostSimilarNodes)])
        mostSimilarNodes = newMostSimilarNodes[:number]

        return mostSimilarNodes