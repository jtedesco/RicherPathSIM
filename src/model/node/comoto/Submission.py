from src.model.node.Node import Node

__author__ = 'jon'

class Submission(Node):
    """
      Represents a particular student's submission for an assignment
    """

    def __init__(self, id, partnerIds = set(), isSolution = False):
        super(Submission, self).__init__(id)

        self.isSolution = isSolution
        self.partnerIds = partnerIds

        if partnerIds is None:
            self.partnerIds = set()
