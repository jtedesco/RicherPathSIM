__author__ = 'jontedesco'


class GraphUtility(object):
    """
      Contains common helper methods for graphs
    """

    @staticmethod
    def addEdgesToGraph(graph, a, b, object):
        """
          Helper function to add bi-directional directed edges to directed graph
        """

        graph.addEdge(a, b, object)
        graph.addEdge(b, a, object)
