import unittest
from test.util.BFSMetaPathUtilityTest import BFSMetaPathUtilityTest
from test.util.DFSMetaPathUtilityTest import DFSMetaPathUtilityTest

__author__ = 'jontedesco'

if __name__ == '__main__':

    utilityTestSuite = unittest.TestLoader().loadTestsFromTestCase(DFSMetaPathUtilityTest)
    utilityTestSuite.addTests(unittest.TestLoader().loadTestsFromTestCase(BFSMetaPathUtilityTest))
    unittest.TextTestRunner().run(utilityTestSuite)
