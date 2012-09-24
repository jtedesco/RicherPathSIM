import unittest
from src.model.metapath.MetaPath import MetaPath
from src.model.node.dblp.Author import Author
from src.model.node.dblp.Paper import Paper
from src.model.node.dblp.Conference import Conference
from src.similarity.heterogeneous.PathSimStrategy import PathSimStrategy
from src.util.SampleGraphUtility import SampleGraphUtility

__author__ = 'jontedesco'

class PathSimStrategyTest(unittest.TestCase):
    """
      Tests the PathSim similarity strategy
    """

    def testFindSingleSimilarityPathSimExampleThree(self):
        """
          Tests pairwise similarity for nodes, using example 3 from PathSim paper (compute similarity scores from Mike)
        """

        graph, authorMap, conferenceMap  = SampleGraphUtility.constructPathSimExampleThree()
        metaPath = MetaPath([Author, Paper, Conference, Paper, Author])
        strategy = PathSimStrategy(graph, metaPath)

        mike = authorMap['Mike']
        jimScore, maryScore, bobScore, annScore = strategy.findSimilarityScores(
            mike, [authorMap['Jim'], authorMap['Mary'], authorMap['Bob'], authorMap['Ann']]
        )

        self.assertEquals(bobScore, 1.0)
        self.assertEquals(annScore, 0)


    def testFindAllSimilarityFromNodeOnPathSimExampleThree(self):
        """
          Tests similarity for all other nodes given a single node, using example 3 from PathSim paper
        """

        graph, authorMap, conferenceMap  = SampleGraphUtility.constructPathSimExampleThree()
        metaPath = MetaPath([Author, Paper, Conference, Paper, Author])
        strategy = PathSimStrategy(graph, metaPath)

        mike = authorMap['Mike']
        mostSimilarNodes = strategy.findMostSimilarNodes(mike, 5)

        self.assertEquals([authorMap['Bob'], authorMap['Mary'], authorMap['Jim']], mostSimilarNodes)
