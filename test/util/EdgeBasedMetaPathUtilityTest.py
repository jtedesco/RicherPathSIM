from src.model.edge.dblp.Citation import Citation
from src.model.node.dblp.Author import Author
from src.model.node.dblp.Paper import Paper
from src.util.EdgeBasedMetaPathUtility import EdgeBasedMetaPathUtility
from test.util.MetaPathUtilityTest import MetaPathUtilityTest

__author__ = 'jontedesco'


class EdgeBasedMetaPathUtilityTest(MetaPathUtilityTest):
    """
      Tests the edge-based implementation of the meta path utility.
    """

    def _getImplementation(self):
        return EdgeBasedMetaPathUtility()


    def testMultipleEdges(self):
        """
          Tests that multiple edges are correctly counted by edge-based implementation
        """

        for i in xrange(0, 5):
            self.templateGraph.addEdge(self.paper1, self.paper2, Citation()) # I know this doesn't make sense, testing purposes

        # Citation (asymmetric)
        self.assertItemsOrReverseItemsEqual(
            [[self.author, self.paper1, self.paper2]] * 6 + [[self.author, self.paper3, self.paper2]]
        , self.metaPathUtility.findMetaPaths(
            self.templateGraph, self.author, self.paper2, [Author, Paper, Paper]
        ))
