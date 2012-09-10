from src.model.node.Node import Node

__author__ = 'jon'

class Student(Node):
    """
      Represents a particular student from CoMoTo (separate from a particular assignment or semester)
    """

    def __init__(self, studentId, displayName, netId, retake = False):
        """
          Creates a new student

            @param  retake      Whether or not this student is retaking the class
        """
        super(Student, self).__init__(studentId)

        self.displayName = displayName
        self.netId = netId
        self.retake = retake

