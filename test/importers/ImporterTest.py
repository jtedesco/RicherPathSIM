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
        expectedNodes = sorted(expectedGraph.getNodes(), key=lambda node: str(node.toDict()).__hash__())
        actualNodes = sorted(actualGraph.getNodes(), key=lambda node: str(node.toDict()).__hash__())
        expectedGraphNodeData = [node.toDict() for node in expectedNodes]
        actualGraphNodeData = [node.toDict() for node in actualNodes]
        expectedGraphNodeData.sort()
        actualGraphNodeData.sort()

        self.assertEqual(expectedGraphNodeData, actualGraphNodeData)

        # Check edges
        expectedGraphEdgeData = list(expectedGraph.getEdgeData(a,b) for (a,b) in expectedGraph.getEdges())
        actualGraphEdgeData = list(actualGraph.getEdgeData(a,b) for (a,b) in actualGraph.getEdges())
        expectedGraphEdgeData.sort()
        actualGraphEdgeData.sort()

        self.assertEqual(expectedGraphEdgeData, actualGraphEdgeData)

        # Check that edges exist where they should
        for expectedNodeA, actualNodeA in zip(expectedNodes, actualNodes):
            for expectedNodeB, actualNodeB in zip(expectedNodes, actualNodes):
                if expectedGraph.hasEdge(actualNodeA, actualNodeB):
                    self.assertTrue(actualGraph.hasEdge(expectedNodeA, expectedNodeB))
                else:
                    self.assertFalse(actualGraph.hasEdge(expectedNodeA, expectedNodeB))