import math

__author__ = 'jontedesco'

class CumulativeGainMeasures(object):
    """
      Implements discounted cumulative gain, given some query (or queries) and relevance labels from 0 to 3 (least
      to most relevant).
    """

    @staticmethod
    def discountedCumulativeGain(queryNode, resultNodes, relevanceScores, attribute = 'name'):
        """
          Computes the discounted cumulative gain of some query
        """

        assert(len(resultNodes) > 1)

        queryAttribute = queryNode.toDict()[attribute]
        totalValue = relevanceScores[(queryAttribute, resultNodes[0].toDict()[attribute])]
        for i in xrange(1, len(resultNodes)):
            totalValue += (relevanceScores[(queryAttribute, resultNodes[i].toDict()[attribute])]) / math.log(i+1, 2)
        return totalValue

    @staticmethod
    def normalizedDiscountedCumulativeGain(queryNode, resultNodes, relevanceScores, attribute = 'name'):
        """
          Calculate
        """

        dcg = CumulativeGainMeasures.discountedCumulativeGain(queryNode, resultNodes, relevanceScores, attribute)
        idealRanking = [relevanceScores[t] for t in sorted(relevanceScores.keys(), key=lambda t: 1-relevanceScores[t])]
        idcg = idealRanking[0] + sum([idealRanking[i] / math.log(i+1, 2) for i in xrange(1, len(idealRanking))])
        return dcg / idcg