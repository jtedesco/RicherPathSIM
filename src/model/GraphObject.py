__author__ = 'jontedesco'

class GraphObject(object):
    """
      Represents an object stored in a graph that contains at least an id and a translation to a dictionary
    """

    def __init__(self, id = None):
        """
          Creates a new graph object

            @param  id  Guaranteed to be unique amongst objects of the same type
        """

        # A map of attributes to expose
        self.id = id


    def toDict(self):
        """
          Returns a dictionary containing all data for this object
        """

        dictionary = dict((name, getattr(self, name)) for name in dir(self) if not name.startswith('__'))
        dictionary['type'] = self.__class__.__name__
        return dictionary
