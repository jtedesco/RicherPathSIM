from src.model.GraphObject import GraphObject

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

        attributesDictionary = object.toDict() if isinstance(object, GraphObject) else None
        graph.add_edge(a, b, attributesDictionary)
        graph.add_edge(b, a, attributesDictionary)
