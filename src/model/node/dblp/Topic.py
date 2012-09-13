from src.model.node.Node import Node

__author__ = 'jontedesco'

class Topic(Node):
    """
      Node representing an topic in the DBLP dataset
    """

    def __init__(self, id, keywords):
        super(Topic, self).__init__(id)

        self.keywords = keywords

