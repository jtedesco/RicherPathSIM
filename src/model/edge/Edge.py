__author__ = 'jon'

class Edge(object):
    """
      Represents a general edge for a heterogeneous graph
    """

    def __init__(self, id):
        """
          Creates a new edge

            @param  id  Guaranteed to be unique amongst edges of the same type
        """

        # A map of attributes to expose
        self.attributes = {
            'id': id
        }
