from src.model.node.Node import Node

__author__ = 'jon'

class Semester(Node):
    """
      Represents a particular semester offering of the class
    """

    def __init__(self, id, season, year):
        super(Semester, self).__init__(id)

        self.season = season
        self.year = year

