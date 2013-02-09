import unittest
from test.util.EdgeBasedMetaPathUtilityTest import EdgeBasedMetaPathUtilityTest

__author__ = 'jontedesco'

if __name__ == '__main__':

    utilityTestSuite = unittest.TestLoader().loadTestsFromTestCase(EdgeBasedMetaPathUtilityTest)
    unittest.TextTestRunner().run(utilityTestSuite)
