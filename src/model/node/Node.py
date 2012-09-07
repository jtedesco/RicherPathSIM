__author__ = 'jon'

class Node(object):
    """
      Represents a general node for a heterogeneous graph
    """

    def __init__(self, id):
        """
          Creates a new node

            @param  id  Guaranteed to be unique amongst nodes of the same type
        """

        # A map of attributes to expose
        self.attributes = {
            'id': id
        }
