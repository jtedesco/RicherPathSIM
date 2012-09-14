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
        self.id = id

    def toDict(self):
        """
          Returns a dictionary containing all data for this object
        """
        return dict((name, getattr(self, name)) for name in dir(self) if not name.startswith('__'))
