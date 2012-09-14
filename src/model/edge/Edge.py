__author__ = 'jon'

class Edge(object):
    """
      Represents a general edge for a heterogeneous graph
    """

    def __init__(self, id = None):
        """
          Creates a new edge

            @param  id  Guaranteed to be unique amongst edges of the same type
        """

        # A map of attributes to expose
        self.id = id

    def toDict(self):
        """
          Returns a dictionary containing all data for this object
        """
        return dict((name, getattr(self, name)) for name in dir(self) if not name.startswith('__'))
