from src.model.GraphObject import GraphObject

__author__ = 'jon'

class Node(GraphObject):
    """
      Represents a general node for a heterogeneous graph
    """

    def __init__(self, id):
        super(Node, self).__init__(id)
