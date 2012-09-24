from src.model.node.Node import Node

__author__ = 'jontedesco'

class Conference(Node):
    """
      Node representing a conference in the DBLP data set
    """

    def __init__(self, id, name):
        super(Conference, self).__init__(id)

        self.name = name
