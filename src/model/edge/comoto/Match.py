from src.model.edge.Edge import Edge

__author__ = 'jon'

class Match(Edge):
    """
      Represents the relationship between two submissions
    """

    def __init__(self, id, percent):
        super(Match, self).__init__(id)

        self.percent = percent