import unittest
from src.similarity.homogeneous.PageRankStrategy import PageRankStrategy
from src.util.SampleGraphUtility import SampleGraphUtility

__author__ = 'jontedesco'

class PageRankStrategyTest(unittest.TestCase):
    """
      Tests a basic PageRank strategy
    """

    def testFindSingleSimilarityPathSimExampleThree(self):
        """
          Tests pairwise similarity for nodes, using example 3 from PathSim paper (compute similarity scores from Mike)
        """

        graph, authorMap, conferenceMap  = SampleGraphUtility.constructPathSimExampleThree()
        strategy = PageRankStrategy(graph)

        mike = authorMap['Mike']
        jimScore = strategy.findSimilarityScore(mike, authorMap['Jim'])
        maryScore = strategy.findSimilarityScore(mike, authorMap['Mary'])
        bobScore = strategy.findSimilarityScore(mike, authorMap['Bob'])
        annScore = strategy.findSimilarityScore(mike, authorMap['Ann'])

        self.assertTrue(annScore >= maryScore)
        self.assertTrue(annScore >= jimScore)
        self.assertTrue(annScore >= bobScore)


    def testFindAllSimilarityFromNodeOnPathSimExampleThree(self):
        """
          Tests similarity for all other nodes given a signle node, using example 3 from PathSim paper
        """

        graph, authorMap, conferenceMap  = SampleGraphUtility.constructPathSimExampleThree()
        strategy = PageRankStrategy(graph)

        mike = authorMap['Mike']
        mostSimilarNodes = strategy.findMostSimilarNodes(mike, 1)

        self.assertEquals([authorMap['Ann']], mostSimilarNodes)
