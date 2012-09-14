from src.model.GraphObject import GraphObject

__author__ = 'jon'

class Edge(GraphObject):
    """
      Represents a general edge for a heterogeneous graph
    """

    def __init__(self, id = None):
        super(Edge, self).__init__(id)

