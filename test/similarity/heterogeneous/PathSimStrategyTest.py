from pprint import pprint
import unittest
from src.model.metapath.MetaPath import MetaPath
from src.model.node.dblp.Author import Author
from src.model.node.dblp.Paper import Paper
from src.model.node.dblp.Venue import Venue
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

        graph, authorMap, venueMap  = SampleGraphUtility.constructPathSimExampleThree()
        metaPath = MetaPath([Author, Paper, Venue, Paper, Author])
        strategy = PathSimStrategy(graph, metaPath)

        mike = authorMap['Mike']
        jimScore = strategy.findSimilarityScore(mike, authorMap['Jim'])
        maryScore = strategy.findSimilarityScore(mike, authorMap['Mary'])
        bobScore = strategy.findSimilarityScore(mike, authorMap['Bob'])
        annScore = strategy.findSimilarityScore(mike, authorMap['Ann'])

        # TODO: Enforce results from paper
        print(jimScore, maryScore, bobScore, annScore)


    def testFindAllSimilarityFromNodeOnPathSimExampleThree(self):
        """
          Tests similarity for all other nodes given a single node, using example 3 from PathSim paper
        """

        graph, authorMap, venueMap  = SampleGraphUtility.constructPathSimExampleThree()
        metaPath = MetaPath([Author, Paper, Venue, Paper, Author])
        strategy = PathSimStrategy(graph, metaPath)

        mike = authorMap['Mike']
        mostSimilarNodes = strategy.findMostSimilarNodes(mike, len(graph.nodes()))

        # TODO: Enforce results from paper
        pprint(mostSimilarNodes[0].toDict())
