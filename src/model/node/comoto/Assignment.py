from src.model.node.Node import Node

__author__ = 'jon'

class Assignment(Node):
    """
      Represents an assignment (in a particular semester) from CoMoTo
    """

    def __init__(self, assignmentId):
        super(Assignment, self).__init__(assignmentId)
