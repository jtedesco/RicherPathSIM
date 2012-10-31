from src.util.MetaPathUtility import MetaPathUtility

__author__ = 'jontedesco'

class BFSMetaPathUtility(MetaPathUtility):
    """
      Iterative implementation of meta path utility interface
    """

    def _findMetaPathsHelper(self, graph, node, metaPathTypes, previousNodes, symmetric):
        """
          Iterative helper function to find nodes not yet visited according to types in meta path. This helper
          function cannot handle loops back to the original node, it assumes that we are only interested in paths that
          do not repeat any nodes, not even the start/end node.
        """

        return [], []

