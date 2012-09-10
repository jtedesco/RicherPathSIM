from src.model.node.Node import Node

__author__ = 'jon'

class Submission(Node):
    """
      Represents a particular student's submission for an assignment
    """

    def __init__(self, submissionId, isSolution = False):
        super(Submission, self).__init__(submissionId)

        self.isSolution = isSolution


