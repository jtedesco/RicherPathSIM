from src.model.edge.Edge import Edge

__author__ = 'jon'

class Match(Edge):
    """
      Represents the relationship between two submissions
    """

    def __init__(self, matchId, percent):
        super().__init__(matchId)

        self.attributes['percent'] = percent