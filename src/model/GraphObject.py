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
        if id is not None:
            self.id = id
        self.dictionary = None


    def toDict(self):
        """
          Returns a dictionary containing all data for this object
        """
        try:
            return self.dictionary
        except AttributeError:
            self.dictionary = self.__dict__
            self.dictionary['type'] = self.__class__.__name__
            return self.dictionary


    def __eq__(self, other):
        return self.toDict() == other.toDict()