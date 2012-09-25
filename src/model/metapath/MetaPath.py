__author__ = 'jontedesco'

class MetaPath(object):
    """
      Represents a meta path in a heterogeneous graph
    """

    def __init__(self, classes, weight = 1.0):
        """
          Constructs a meta path object

            @param  classes     The (ordered) list of classes comprising the meta path. Should start and end at the same
                                type of node
            @param  weight      The weight associated with this meta path (defaults to 1, meaning all paths are equally
                                important)
        """

        self.classes = classes
        self.weight = weight


    def __eq__(self, other):
        return self.classes == other.classes and self.weight == other.weight

    def __len__(self):
        return len(self.classes)
