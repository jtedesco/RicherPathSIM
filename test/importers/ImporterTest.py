import unittest

__author__ = 'jontedesco'

class ImporterTest(unittest.TestCase):
    """
      Class containing common utility functions for importer tests
    """

    def __init__(self, methodName='runTest'):
        super(ImporterTest, self).__init__(methodName)

        self.maxDiff = None


    def assertGraphsEqual(self, expectedGraph, actualGraph):
        """
          Checks equality node by node and edge by edge
        """

        # Check nodes
        expectedGraphNodeData = list(node.toDict() for node in expectedGraph.getNodes())
        actualGraphNodeData = list(node.toDict() for node in actualGraph.getNodes())
        expectedGraphNodeData.sort()
        actualGraphNodeData.sort()

        self.assertEqual(expectedGraphNodeData, actualGraphNodeData)

        # Check edges
        expectedGraphEdgeData = list(expectedGraph.getEdgeData(a,b) for (a,b) in expectedGraph.getEdges())
        actualGraphEdgeData = list(actualGraph.getEdgeData(a,b) for (a,b) in actualGraph.getEdges())
        expectedGraphEdgeData.sort()
        actualGraphEdgeData.sort()

        self.assertEqual(expectedGraphEdgeData, actualGraphEdgeData)
