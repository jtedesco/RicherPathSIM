from src.model.node.Node import Node

__author__ = 'jon'

class Student(Node):
    """
      Represents a particular student from CoMoTo (separate from a particular assignment or semester)
    """

    def __init__(self, studentId, displayName, netId, retake):
        """
          Creates a new student

            @param  retake      Whether or not this student is retaking the class
        """
        super().__init__(studentId)

        self.attributes['displayName'] = displayName
        self.attributes['netId'] = netId
        self.attributes['retake'] = retake

