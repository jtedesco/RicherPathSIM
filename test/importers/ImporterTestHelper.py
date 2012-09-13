"""
  File containing utility functions for importer tests
"""

__author__ = 'jontedesco'

def addEdgesToGraph(graph, a, b, object):
    """
      Helper function to add bi-directional directed edges
    """
    graph.add_edge(a, b, object.attributes())
    graph.add_edge(b, a, object.attributes())
