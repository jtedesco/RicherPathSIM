import unittest
from src.model.node.dblp.Author import Author
from src.model.node.dblp.Paper import Paper
from src.model.node.dblp.Conference import Conference
from src.similarity.heterogeneous.ProjectedPageRankStrategy import ProjectedPageRankStrategy
from src.util.SampleGraphUtility import SampleGraphUtility

__author__ = 'jontedesco'

class ProjectedPageRankStrategyTest(unittest.TestCase):
    """
      Tests the PathSim similarity strategy
    """

    def testFindSingleSimilarityPathSimExampleThree(self):
        """
          Tests pairwise similarity for nodes, using example 3 from PathSim paper (compute similarity scores from Mike)
        """

        graph, authorMap, conferenceMap  = SampleGraphUtility.constructPathSimExampleThree()
        metaPath = [Author, Paper, Conference, Paper, Author]
        strategy = ProjectedPageRankStrategy(graph, metaPath)

        mike = authorMap['Mike']
        jimScore, maryScore, bobScore, annScore = strategy.findSimilarityScores(
            mike, [authorMap['Jim'], authorMap['Mary'], authorMap['Bob'], authorMap['Ann']]
        )

        self.assertEquals(jimScore, max([jimScore, maryScore, bobScore, annScore]))


    def testFindAllSimilarityFromNodeOnPathSimExampleThree(self):
        """
          Tests similarity for all other nodes given a single node, using example 3 from PathSim paper
        """

        graph, authorMap, conferenceMap  = SampleGraphUtility.constructPathSimExampleThree()
        metaPath = [Author, Paper, Conference, Paper, Author]
        strategy = ProjectedPageRankStrategy(graph, metaPath)

        mike = authorMap['Mike']
        mostSimilarNodes = strategy.findMostSimilarNodes(mike, 5)

        self.assertEquals([authorMap['Jim'], authorMap['Mary'], authorMap['Bob']], mostSimilarNodes)
