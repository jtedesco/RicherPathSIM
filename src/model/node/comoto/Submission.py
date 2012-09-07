from src.model.node.Node import Node

__author__ = 'jon'

class Submission(Node):
    """
      Represents a particular student's submission for an assignment
    """

    def __init__(self, submissionId, isSolution):
        super().__init__(submissionId)

        self.attributes['isSolution'] = isSolution


