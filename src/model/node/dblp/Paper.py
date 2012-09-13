from src.model.node.Node import Node

__author__ = 'jontedesco'


class Paper(Node):
    """
      Node representing a paper in the DBLP dataset
    """

    def __init__(self, id, title):
        super(Paper, self).__init__(id)

        self.title = title

