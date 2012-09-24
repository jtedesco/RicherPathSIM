import unittest
from src.model.metapath.MetaPath import MetaPath
from src.model.node.dblp.Author import Author
from src.model.node.dblp.Paper import Paper
from src.model.node.dblp.Venue import Venue
from src.util.MetaPathUtility import MetaPathUtility
from src.util.SampleGraphUtility import SampleGraphUtility

__author__ = 'jontedesco'

class SampleGraphUtilityTest(unittest.TestCase):
    """
      Tests the creation of sample graphs by the SampleGraphUtility class

        NOTE: Has dependency on MetaPathUtility - if MetaPathUtilityTest is failing, this test case may fail as a result
    """


    def testConstructPathSimExampleThree(self):
        """
          Tests the construction of "Example 3" from PathSim paper. Specifically, checks adjacency matrix shown in
          this example for Author-Paper-Venue meta paths.
        """

        graph, authorMap, venueMap = SampleGraphUtility.constructPathSimExampleThree()
        metaPath = MetaPath([Author, Paper, Venue])

        # Mike's adjacency to conferences
        self.assertEquals(2, len(MetaPathUtility.findMetaPaths(graph, authorMap['Mike'], venueMap['SIGMOD'], metaPath)))
        self.assertEquals(1, len(MetaPathUtility.findMetaPaths(graph, authorMap['Mike'], venueMap['VLDB'], metaPath)))
        self.assertEquals(0, len(MetaPathUtility.findMetaPaths(graph, authorMap['Mike'], venueMap['ICDE'], metaPath)))
        self.assertEquals(0, len(MetaPathUtility.findMetaPaths(graph, authorMap['Mike'], venueMap['KDD'], metaPath)))

        # Jim's adjacency to conferences
        self.assertEquals(50, len(MetaPathUtility.findMetaPaths(graph, authorMap['Jim'], venueMap['SIGMOD'], metaPath)))
        self.assertEquals(20, len(MetaPathUtility.findMetaPaths(graph, authorMap['Jim'], venueMap['VLDB'], metaPath)))
        self.assertEquals(0, len(MetaPathUtility.findMetaPaths(graph, authorMap['Jim'], venueMap['ICDE'], metaPath)))
        self.assertEquals(0, len(MetaPathUtility.findMetaPaths(graph, authorMap['Jim'], venueMap['KDD'], metaPath)))

        # Mary's adjacency to conferences
        self.assertEquals(2, len(MetaPathUtility.findMetaPaths(graph, authorMap['Mary'], venueMap['SIGMOD'], metaPath)))
        self.assertEquals(0, len(MetaPathUtility.findMetaPaths(graph, authorMap['Mary'], venueMap['VLDB'], metaPath)))
        self.assertEquals(1, len(MetaPathUtility.findMetaPaths(graph, authorMap['Mary'], venueMap['ICDE'], metaPath)))
        self.assertEquals(0, len(MetaPathUtility.findMetaPaths(graph, authorMap['Mary'], venueMap['KDD'], metaPath)))

        # Bob's adjacency to conferences
        self.assertEquals(2, len(MetaPathUtility.findMetaPaths(graph, authorMap['Bob'], venueMap['SIGMOD'], metaPath)))
        self.assertEquals(1, len(MetaPathUtility.findMetaPaths(graph, authorMap['Bob'], venueMap['VLDB'], metaPath)))
        self.assertEquals(0, len(MetaPathUtility.findMetaPaths(graph, authorMap['Bob'], venueMap['ICDE'], metaPath)))
        self.assertEquals(0, len(MetaPathUtility.findMetaPaths(graph, authorMap['Bob'], venueMap['KDD'], metaPath)))

        # Ann's adjacency to conferences
        self.assertEquals(0, len(MetaPathUtility.findMetaPaths(graph, authorMap['Ann'], venueMap['SIGMOD'], metaPath)))
        self.assertEquals(0, len(MetaPathUtility.findMetaPaths(graph, authorMap['Ann'], venueMap['VLDB'], metaPath)))
        self.assertEquals(1, len(MetaPathUtility.findMetaPaths(graph, authorMap['Ann'], venueMap['ICDE'], metaPath)))
        self.assertEquals(1, len(MetaPathUtility.findMetaPaths(graph, authorMap['Ann'], venueMap['KDD'], metaPath)))
