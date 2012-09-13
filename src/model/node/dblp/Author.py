from src.model.node.Node import Node

__author__ = 'jontedesco'


class Author(Node):
    """
      Node representing an author in the DBLP dataset
    """

    def __init__(self, id, name):
        super(Author, self).__init__(id)

        self.name = name
