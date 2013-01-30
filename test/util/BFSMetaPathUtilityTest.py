from src.util.BFSMetaPathUtility import BFSMetaPathUtility
from test.util.MetaPathUtilityTest import MetaPathUtilityTest

__author__ = 'jontedesco'

class BFSMetaPathUtilityTest(MetaPathUtilityTest):
    """
      Tests the breadth-first-search implementation of the meta path utility.
    """

    def _getImplementation(self):
        return BFSMetaPathUtility()
