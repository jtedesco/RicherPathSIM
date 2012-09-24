import unittest
from src.model.metapath.MetaPath import MetaPath
from src.model.node.dblp.Author import Author
from src.model.node.dblp.Paper import Paper
from src.model.node.dblp.Conference import Conference
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
          this example for Author-Paper-Conference meta paths.
        """

        graph, authorMap, conferenceMap = SampleGraphUtility.constructPathSimExampleThree()
        metaPath = MetaPath([Author, Paper, Conference])

        # Mike's adjacency to conferences
        self.assertEquals(2, len(MetaPathUtility.findMetaPaths(graph, authorMap['Mike'], conferenceMap['SIGMOD'], metaPath)))
        self.assertEquals(1, len(MetaPathUtility.findMetaPaths(graph, authorMap['Mike'], conferenceMap['VLDB'], metaPath)))
        self.assertEquals(0, len(MetaPathUtility.findMetaPaths(graph, authorMap['Mike'], conferenceMap['ICDE'], metaPath)))
        self.assertEquals(0, len(MetaPathUtility.findMetaPaths(graph, authorMap['Mike'], conferenceMap['KDD'], metaPath)))

        # Jim's adjacency to conferences
        self.assertEquals(50, len(MetaPathUtility.findMetaPaths(graph, authorMap['Jim'], conferenceMap['SIGMOD'], metaPath)))
        self.assertEquals(20, len(MetaPathUtility.findMetaPaths(graph, authorMap['Jim'], conferenceMap['VLDB'], metaPath)))
        self.assertEquals(0, len(MetaPathUtility.findMetaPaths(graph, authorMap['Jim'], conferenceMap['ICDE'], metaPath)))
        self.assertEquals(0, len(MetaPathUtility.findMetaPaths(graph, authorMap['Jim'], conferenceMap['KDD'], metaPath)))

        # Mary's adjacency to conferences
        self.assertEquals(2, len(MetaPathUtility.findMetaPaths(graph, authorMap['Mary'], conferenceMap['SIGMOD'], metaPath)))
        self.assertEquals(0, len(MetaPathUtility.findMetaPaths(graph, authorMap['Mary'], conferenceMap['VLDB'], metaPath)))
        self.assertEquals(1, len(MetaPathUtility.findMetaPaths(graph, authorMap['Mary'], conferenceMap['ICDE'], metaPath)))
        self.assertEquals(0, len(MetaPathUtility.findMetaPaths(graph, authorMap['Mary'], conferenceMap['KDD'], metaPath)))

        # Bob's adjacency to conferences
        self.assertEquals(2, len(MetaPathUtility.findMetaPaths(graph, authorMap['Bob'], conferenceMap['SIGMOD'], metaPath)))
        self.assertEquals(1, len(MetaPathUtility.findMetaPaths(graph, authorMap['Bob'], conferenceMap['VLDB'], metaPath)))
        self.assertEquals(0, len(MetaPathUtility.findMetaPaths(graph, authorMap['Bob'], conferenceMap['ICDE'], metaPath)))
        self.assertEquals(0, len(MetaPathUtility.findMetaPaths(graph, authorMap['Bob'], conferenceMap['KDD'], metaPath)))

        # Ann's adjacency to conferences
        self.assertEquals(0, len(MetaPathUtility.findMetaPaths(graph, authorMap['Ann'], conferenceMap['SIGMOD'], metaPath)))
        self.assertEquals(0, len(MetaPathUtility.findMetaPaths(graph, authorMap['Ann'], conferenceMap['VLDB'], metaPath)))
        self.assertEquals(1, len(MetaPathUtility.findMetaPaths(graph, authorMap['Ann'], conferenceMap['ICDE'], metaPath)))
        self.assertEquals(1, len(MetaPathUtility.findMetaPaths(graph, authorMap['Ann'], conferenceMap['KDD'], metaPath)))
