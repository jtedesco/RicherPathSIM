import unittest
from src.similarity.homogeneous.PageRankStrategy import PageRankStrategy
from src.util.SampleGraphUtility import SampleGraphUtility

__author__ = 'jontedesco'

class PageRankStrategyTest(unittest.TestCase):
    """
      Tests a basic PageRank strategy test
    """

    def testPathSimExampleThree(self):
        """
          Tests pairwise similarity for nodes, using example 3 from PathSim paper (compute similarity scores from Mike)
        """

        graph, authorMap, venueMap  = SampleGraphUtility.constructPathSimExampleThree()
        strategy = PageRankStrategy(graph)

        mike = authorMap['Mike']
        jimScore = strategy.findSimilarityScore(mike, authorMap['Jim'])
        maryScore = strategy.findSimilarityScore(mike, authorMap['Mary'])
        bobScore = strategy.findSimilarityScore(mike, authorMap['Bob'])

        # TODO: Research actual algorithm & setup in more detail to implement properly
        self.assertTrue(jimScore >= maryScore)
        self.assertTrue(bobScore >= maryScore)
