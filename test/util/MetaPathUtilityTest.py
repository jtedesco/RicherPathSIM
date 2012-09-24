import unittest
import networkx
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
        graph = networkx.DiGraph()

        author = Author(0, 'author')
        coauthor = Author(1, 'coauthor')
        conference1 = Conference(0, 'conference1')
        conference2 = Conference(1, 'conference2')
        paper1 = Paper(0, 'paper1')
        paper2 = Paper(1, 'paper2')
        paper3 = Paper(2, 'paper3')
        graph.add_nodes_from([author, conference1, conference2, paper1, paper2, paper3])

        GraphUtility.addEdgesToGraph(graph, paper1, author, Authorship())
        GraphUtility.addEdgesToGraph(graph, paper2, author, Authorship())
        GraphUtility.addEdgesToGraph(graph, paper3, author, Authorship())
        GraphUtility.addEdgesToGraph(graph, paper3, coauthor, Authorship())
        GraphUtility.addEdgesToGraph(graph, paper1, conference1, Publication())
        GraphUtility.addEdgesToGraph(graph, paper2, conference1, Publication())
        GraphUtility.addEdgesToGraph(graph, paper3, conference2, Publication())
        graph.add_edge(paper1, paper2, Citation().toDict())
        GraphUtility.addEdgesToGraph(graph, paper2, paper3, Citation().toDict())

        self.templateGraph = graph
        self.templateGraphMap = {}
        for node in graph.nodes():
            try:
                self.templateGraphMap[node.name] = node
            except AttributeError:
                self.templateGraphMap[node.title] = node


    def testFindMetaPathNeighborsLengthTwo(self):
        """
          Tests finding neighbors along a length two meta path in template graph
        """

        # Test case with many neighbors
        self.assertEquals({
            self.templateGraphMap['conference1'], self.templateGraphMap['conference2']
        }, MetaPathUtility.findMetaPathNeighbors(
            self.templateGraph, self.templateGraphMap['author'], MetaPath([Author, Paper, Conference])
        ))

        # Test case with only one neighbor
        self.assertEquals({
            self.templateGraphMap['author']
        }, MetaPathUtility.findMetaPathNeighbors(
            self.templateGraph, self.templateGraphMap['conference1'], MetaPath([Conference, Paper, Author])
        ))


    def testFindMetaPathNeighborsLengthOne(self):
        """
          Tests finding neighbors along a length one meta path in template graph
        """

        # Test case with many neighbors
        self.assertEquals({
            self.templateGraphMap['paper1'], self.templateGraphMap['paper2'], self.templateGraphMap['paper3']
        }, MetaPathUtility.findMetaPathNeighbors(
            self.templateGraph, self.templateGraphMap['author'], MetaPath([Author, Paper])
        ))

        # Test case with only one neighbor
        self.assertEquals({
            self.templateGraphMap['author']
        }, MetaPathUtility.findMetaPathNeighbors(
            self.templateGraph, self.templateGraphMap['paper1'], MetaPath([Paper, Author])
        ))


    def testFindMetaPathsLengthTwo(self):
        """
          Tests finding the meta path(s) of length two between two nodes in template graph
        """

        # Test case with many paths
        self.assertItemsEqual([
            [self.templateGraphMap['author'], self.templateGraphMap['paper1'], self.templateGraphMap['conference1']],
            [self.templateGraphMap['author'], self.templateGraphMap['paper2'], self.templateGraphMap['conference1']]
        ], MetaPathUtility.findMetaPaths(
            self.templateGraph, self.templateGraphMap['author'], self.templateGraphMap['conference1'], MetaPath([Author, Paper, Conference])
        ))

        # Test case with only one path
        self.assertEquals([
            [self.templateGraphMap['author'], self.templateGraphMap['paper3'], self.templateGraphMap['conference2']]
        ], MetaPathUtility.findMetaPaths(
            self.templateGraph, self.templateGraphMap['author'], self.templateGraphMap['conference2'], MetaPath([Author, Paper, Conference])
        ))


    def testFindMetaPathsLengthOne(self):
        """
          Tests finding the meta path(s) of length one between two nodes in template graph
        """

        self.assertItemsEqual([
            [self.templateGraphMap['author'], self.templateGraphMap['paper1']]
        ], MetaPathUtility.findMetaPaths(
            self.templateGraph, self.templateGraphMap['author'], self.templateGraphMap['paper1'], MetaPath([Author, Paper])
        ))


    def testFindOddLengthRepeatedMetaPaths(self):
        """
          Tests finding meta paths when the meta paths are symmetric, with different source & destination nodes
        """

        # Co-authorship
        self.assertItemsEqual([
            [self.templateGraphMap['author'], self.templateGraphMap['paper3'], self.templateGraphMap['coauthor']]
        ], MetaPathUtility.findMetaPaths(
            self.templateGraph, self.templateGraphMap['author'], self.templateGraphMap['coauthor'], MetaPath([Author, Paper, Author])
        ))

        # Co-author citation
        self.assertItemsEqual([
            [self.templateGraphMap['author'], self.templateGraphMap['paper2'], self.templateGraphMap['paper3'], self.templateGraphMap['coauthor']]
        ], MetaPathUtility.findMetaPaths(
            self.templateGraph, self.templateGraphMap['author'], self.templateGraphMap['coauthor'], MetaPath([Author, Paper, Paper, Author])
        ))

        # Self-citation (asymmetric)
        self.assertItemsEqual([
            [self.templateGraphMap['author'], self.templateGraphMap['paper1'], self.templateGraphMap['paper2']],
            [self.templateGraphMap['author'], self.templateGraphMap['paper3'], self.templateGraphMap['paper2']]
        ], MetaPathUtility.findMetaPaths(
            self.templateGraph, self.templateGraphMap['author'], self.templateGraphMap['paper2'], MetaPath([Author, Paper, Paper])
        ))


    def testFindOddLengthSymmetricMetaPaths(self):
        """
          Tests finding meta paths when the meta paths may or may not be symmetric, and we are looking for symmetric paths
          only (still starting & ending at different points) of odd length
        """

        # Co-authorship
        self.assertItemsEqual([
            [self.templateGraphMap['author'], self.templateGraphMap['paper3'], self.templateGraphMap['coauthor']]
        ], MetaPathUtility.findMetaPaths(self.templateGraph, self.templateGraphMap['author'],
            self.templateGraphMap['coauthor'], MetaPath([Author, Paper]), True
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



    def testFindEvenLengthSymmetricMetaPaths(self):
        """
          Tests finding meta paths when the meta paths may or may not be symmetric, and we are looking for symmetric paths
          only (still starting & ending at different points) of even length
        """

        # Author citation
        self.assertItemsEqual([
            [self.templateGraphMap['author'], self.templateGraphMap['paper2'], self.templateGraphMap['paper3'], self.templateGraphMap['coauthor']]
        ], MetaPathUtility.findMetaPaths(
            self.templateGraph, self.templateGraphMap['author'], self.templateGraphMap['coauthor'], MetaPath([Author, Paper]), True, True
        ))


    def testFindLoopMetaPaths(self):
        """
          Tests finding meta paths where paths are not necessarily symmetric, but meta paths start and end at the same node,
          with no other repeated nodes
        """

        # Self-citation
        self.assertItemsEqual([
            [self.templateGraphMap['author'], self.templateGraphMap['paper1'], self.templateGraphMap['paper2'], self.templateGraphMap['author']],
            [self.templateGraphMap['author'], self.templateGraphMap['paper2'], self.templateGraphMap['paper3'], self.templateGraphMap['author']],
            [self.templateGraphMap['author'], self.templateGraphMap['paper3'], self.templateGraphMap['paper2'], self.templateGraphMap['author']]
        ], MetaPathUtility.findMetaPaths(
            self.templateGraph, self.templateGraphMap['author'], self.templateGraphMap['author'], MetaPath([Author, Paper, Paper, Author])
        ))

        # Publishing multiple papers in a single conference
        self.assertItemsEqual([
            [self.templateGraphMap['author'], self.templateGraphMap['paper1'], self.templateGraphMap['conference1'], self.templateGraphMap['paper2'], self.templateGraphMap['author']],
            [self.templateGraphMap['author'], self.templateGraphMap['paper2'], self.templateGraphMap['conference1'], self.templateGraphMap['paper1'], self.templateGraphMap['author']]
        ], MetaPathUtility.findMetaPaths(
            self.templateGraph, self.templateGraphMap['author'], self.templateGraphMap['author'], MetaPath([Author, Paper, Conference, Paper, Author])
        ))


    def testFindLoopMetaPathsWithSymmetry(self):
        """
          Tests finding meta paths where paths are symmetric (of both even & odd length), where paths are cycles
        """

        # Self-citation using symmetry
        self.assertItemsEqual([
            [self.templateGraphMap['author'], self.templateGraphMap['paper1'], self.templateGraphMap['paper2'], self.templateGraphMap['author']],
            [self.templateGraphMap['author'], self.templateGraphMap['paper2'], self.templateGraphMap['paper3'], self.templateGraphMap['author']],
            [self.templateGraphMap['author'], self.templateGraphMap['paper3'], self.templateGraphMap['paper2'], self.templateGraphMap['author']]
        ], MetaPathUtility.findMetaPaths(
            self.templateGraph, self.templateGraphMap['author'], self.templateGraphMap['author'], MetaPath([Author, Paper]), True, True
        ))

        # Publishing multiple papers in a single conference using symmetry
        self.assertItemsEqual([
            [self.templateGraphMap['author'], self.templateGraphMap['paper1'], self.templateGraphMap['conference1'], self.templateGraphMap['paper2'], self.templateGraphMap['author']],
            [self.templateGraphMap['author'], self.templateGraphMap['paper2'], self.templateGraphMap['conference1'], self.templateGraphMap['paper1'], self.templateGraphMap['author']]
        ], MetaPathUtility.findMetaPaths(
            self.templateGraph, self.templateGraphMap['author'], self.templateGraphMap['author'], MetaPath([Author, Paper, Conference]), True
        ))
