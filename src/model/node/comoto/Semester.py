from src.model.node.Node import Node

__author__ = 'jon'

class Semester(Node):
    """
      Represents a particular semester offering of the class
    """

    def __init__(self, semesterId, season, year):
        super(Semester, self).__init__(semesterId)

        self.attributes['season'] = season
        self.attributes['year'] = year

