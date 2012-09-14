import unittest

__author__ = 'jontedesco'

class ImporterTest(unittest.TestCase):
    """
      Class containing common utility functions for importer tests
    """

    def addEdgesToGraph(self, graph, a, b, object):
        """
          Helper function to add bi-directional directed edges to directed graph
        """

        graph.add_edge(a, b, object.toDict())
        graph.add_edge(b, a, object.toDict())


    def assertGraphsEqual(self, expectedGraph, actualGraph):
        """
          Checks equality node by node and edge by edge
        """

        expectedGraphNodeData = list(node.toDict() for node in expectedGraph.nodes())
        actualGraphNodeData = list(node.toDict() for node in actualGraph.nodes())
        expectedGraphNodeData.sort()
        actualGraphNodeData.sort()

        self.assertEqual(expectedGraphNodeData, actualGraphNodeData)
