from src.util.DFSMetaPathUtility import DFSMetaPathUtility
from test.util.MetaPathUtilityTest import MetaPathUtilityTest

__author__ = 'jontedesco'

class DFSMetaPathUtilityTest(MetaPathUtilityTest):
    """
      Tests the depth-first-search implementation of the meta path utility.
    """

    def _getImplementation(self):
        return DFSMetaPathUtility()
