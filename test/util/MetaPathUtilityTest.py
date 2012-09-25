import unittest
from src.graph.GraphFactory import GraphFactory
from src.model.edge.dblp.Authorship import Authorship
from src.model.edge.dblp.Citation import Citation
from src.model.edge.dblp.Publication import Publication
from src.model.metapath.MetaPath import MetaPath
from src.model.node.dblp.Author import Author
from src.model.node.dblp.Paper import Paper
from src.model.node.dblp.Conference import Conference
from src.util.GraphUtility import GraphUtility
from src.util.MetaPathUtility import MetaPathUtility

__author__ = 'jontedesco'

class MetaPathUtilityTest(unittest.TestCase):
    """
      Tests the meta path utility functions
    """

    def __init__(self, methodName='runTest'):
        super(MetaPathUtilityTest, self).__init__(methodName)

        self.maxDiff = None

        # Construct template graph for tests
        graph = GraphFactory.createInstance()

        # Put references to graph objects on test object
        self.author = Author(0, 'author')
        self.coauthor = Author(1, 'coauthor')
        self.conference1 = Conference(0, 'conference1')
        self.conference2 = Conference(1, 'conference2')
        self.paper1 = Paper(0, 'paper1')
        self.paper2 = Paper(1, 'paper2')
        self.paper3 = Paper(2, 'paper3')

        # Construct graph
        graph.addNodes([self.author, self.conference1, self.conference2, self.paper1, self.paper2, self.paper3])
        GraphUtility.addEdgesToGraph(graph, self.paper1, self.author, Authorship())
        GraphUtility.addEdgesToGraph(graph, self.paper2, self.author, Authorship())
        GraphUtility.addEdgesToGraph(graph, self.paper3, self.author, Authorship())
        GraphUtility.addEdgesToGraph(graph, self.paper3, self.coauthor, Authorship())
        GraphUtility.addEdgesToGraph(graph, self.paper1, self.conference1, Publication())
        GraphUtility.addEdgesToGraph(graph, self.paper2, self.conference1, Publication())
        GraphUtility.addEdgesToGraph(graph, self.paper3, self.conference2, Publication())
        graph.addEdge(self.paper1, self.paper2, Citation())
        GraphUtility.addEdgesToGraph(graph, self.paper2, self.paper3, Citation())

        self.templateGraph = graph


    def testFindMetaPathNeighborsLengthTwo(self):
        """
          Tests finding neighbors along a length two meta path in template graph
        """

        # Test case with many neighbors
        self.assertEquals({
            self.conference1, self.conference2
        }, MetaPathUtility.findMetaPathNeighbors(
            self.templateGraph, self.author, MetaPath([Author, Paper, Conference])
        ))

        # Test case with only one neighbor
        self.assertEquals({
            self.author
        }, MetaPathUtility.findMetaPathNeighbors(
            self.templateGraph, self.conference1, MetaPath([Conference, Paper, Author])
        ))


    def testFindMetaPathsLengthTwo(self):
        """
          Tests finding the meta path(s) of length two between two nodes in template graph
        """

        # Author published in conference meta path
        metaPath = MetaPath([Author, Paper, Conference])

        # Test case with many paths
        self.assertItemsEqual([
            [self.author, self.paper1, self.conference1],
            [self.author, self.paper2, self.conference1]
        ], MetaPathUtility.findMetaPaths(
            self.templateGraph, self.author, self.conference1, metaPath
        ))

        # Test case with only one path
        self.assertEquals([
            [self.author, self.paper3, self.conference2]
        ], MetaPathUtility.findMetaPaths(
            self.templateGraph, self.author, self.conference2, metaPath
        ))


    def testFindMetaPathNeighborsLengthOne(self):
        """
          Tests finding neighbors along a length one meta path in template graph
        """

        # Test case with many neighbors
        self.assertEquals({
            self.paper1, self.paper2, self.paper3
        }, MetaPathUtility.findMetaPathNeighbors(
            self.templateGraph, self.author, MetaPath([Author, Paper])
        ))

        # Test case with only one neighbor
        self.assertEquals({
            self.author
        }, MetaPathUtility.findMetaPathNeighbors(
            self.templateGraph, self.paper1, MetaPath([Paper, Author])
        ))


    def testFindMetaPathsLengthOne(self):
        """
          Tests finding the meta path(s) of length one between two nodes in template graph
        """

        metaPath = MetaPath([Author, Paper])

        self.assertItemsEqual([
            [self.author, self.paper1]
        ], MetaPathUtility.findMetaPaths(
            self.templateGraph, self.author, self.paper1, metaPath
        ))


    def testFindOddLengthRepeatedMetaPathNeighbors(self):
        """
          Tests finding the meta path neighbors when the meta paths are symmetric
        """

        # Co-authorship
        self.assertItemsEqual([
            self.author, self.coauthor
        ], MetaPathUtility.findMetaPathNeighbors(
            self.templateGraph, self.author, MetaPath([Author, Paper, Author])
        ))
        self.assertItemsEqual([
            self.author, self.coauthor
        ], MetaPathUtility.findMetaPathNeighbors(
            self.templateGraph, self.coauthor, MetaPath([Author, Paper, Author])
        ))

        # Author citation (asymmetric)
        self.assertItemsEqual([
            self.author, self.coauthor
        ], MetaPathUtility.findMetaPathNeighbors(
            self.templateGraph, self.author, MetaPath([Author, Paper, Paper, Author])
        ))
        self.assertItemsEqual([
            self.author
        ], MetaPathUtility.findMetaPathNeighbors(
            self.templateGraph, self.coauthor, MetaPath([Author, Paper, Paper, Author])
        ))

        # Self-citation (asymmetric)
        self.assertItemsEqual({
            self.paper2, self.paper3,
        }, MetaPathUtility.findMetaPathNeighbors(
            self.templateGraph, self.author, MetaPath([Author, Paper, Paper])
        ))


    def testFindOddLengthRepeatedMetaPaths(self):
        """
          Tests finding meta paths when the meta paths are symmetric, with different source & destination nodes
        """

        # Co-authorship
        self.assertItemsEqual([
            [self.author, self.paper3, self.coauthor]
        ], MetaPathUtility.findMetaPaths(
            self.templateGraph, self.author, self.coauthor, MetaPath([Author, Paper, Author])
        ))

        # Author citation
        self.assertItemsEqual([
            [self.author, self.paper2, self.paper3, self.coauthor]
        ], MetaPathUtility.findMetaPaths(
            self.templateGraph, self.author, self.coauthor, MetaPath([Author, Paper, Paper, Author])
        ))

        # Citation (asymmetric)
        self.assertItemsEqual([
            [self.author, self.paper1, self.paper2],
            [self.author, self.paper3, self.paper2]
        ], MetaPathUtility.findMetaPaths(
            self.templateGraph, self.author, self.paper2, MetaPath([Author, Paper, Paper])
        ))


    def testFindOddLengthSymmetricMetaPathNeighbors(self):
        """
          Tests neighbors via meta paths when symmetry is enforced
        """

        # Remove paper3 authorship -- should not contain paper2 in this case, since paper2 -> paper3, but not vice versa
        self.templateGraph.remove_edge(self.author, self.paper3)
        self.templateGraph.remove_edge(self.paper3, self.author)

        # Citation
        self.assertItemsEqual({
            self.paper3
        }, MetaPathUtility.findMetaPathNeighbors(
            self.templateGraph, self.author, MetaPath([Author, Paper, Paper]), True
        ))


    def testFindOddLengthSymmetricMetaPaths(self):
        """
          Tests finding meta paths when the meta paths may or may not be symmetric, and we are looking for symmetric
          paths only (still starting & ending at different points) of odd length
        """

        # Co-authorship
        self.assertItemsEqual([
            [self.author, self.paper3, self.coauthor]
        ], MetaPathUtility.findMetaPaths(self.templateGraph, self.author,
            self.coauthor, MetaPath([Author, Paper, Author]), True
        ))


    def testExpandPartialMetaPathOddUnweighted(self):
        """
          Tests the helper function to expand partial meta paths on the utility class, using even length unweighted path
        """

        self.assertEquals(
            MetaPath([Author, Paper, Author]),
            MetaPathUtility.expandPartialMetaPath((MetaPath([Author, Paper])))
        )


    def testExpandPartialMetaPathEvenUnweighted(self):
        """
          Tests the helper function to expand partial meta paths on the utility class, using odd length unweighted path
        """

        self.assertEquals(
            MetaPath([Author, Paper, Paper, Author]),
            MetaPathUtility.expandPartialMetaPath((MetaPath([Author, Paper])), True)
        )


    def testExpandPartialMetaPathOddWeighted(self):
        """
          Tests the helper function to expand partial meta paths on the utility class, using even length weighted path
        """

        self.assertEquals(
            MetaPath([Author, Paper, Author], 0.123),
            MetaPathUtility.expandPartialMetaPath((MetaPath([Author, Paper], 0.123)))
        )


    def testExpandPartialMetaPathEvenWeighted(self):
        """
          Tests the helper function to expand partial meta paths on the utility class, using odd length weighted path
        """

        self.assertEquals(
            MetaPath([Author, Paper, Paper, Author], 0.445),
            MetaPathUtility.expandPartialMetaPath((MetaPath([Author, Paper], 0.445)), True)
        )


    def testFindLoopMetaPaths(self):
        """
          Tests finding meta paths where paths are not necessarily symmetric, but meta paths start and end at the same
          node, with no other repeated nodes
        """

        # Self-citation
        self.assertItemsEqual([
            [self.author, self.paper1, self.paper2, self.author],
            [self.author, self.paper2, self.paper3, self.author],
            [self.author, self.paper3, self.paper2, self.author]
        ], MetaPathUtility.findMetaPaths(
            self.templateGraph, self.author, self.author, MetaPath([Author, Paper, Paper, Author])
        ))

        # Publishing multiple papers in a single conference
        self.assertItemsEqual([
            [self.author, self.paper1, self.conference1, self.paper2, self.author],
            [self.author, self.paper2, self.conference1, self.paper1, self.author]
        ], MetaPathUtility.findMetaPaths(
            self.templateGraph, self.author, self.author, MetaPath([Author, Paper, Conference, Paper, Author])
        ))


    def testFindLoopMetaPathsWithSymmetry(self):
        """
          Tests finding meta paths where paths are symmetric (of both even & odd length), where paths are cycles
        """

        # Self-citation using symmetry
        self.assertItemsEqual([
            [self.author, self.paper2, self.paper3, self.author],
            [self.author, self.paper3, self.paper2, self.author]
        ], MetaPathUtility.findMetaPaths(
            self.templateGraph, self.author, self.author, MetaPath([Author, Paper, Paper, Author]), True
        ))