import unittest
from test.importers.ArnetMinerDataImporterTest import ArnetMinerDataImporterTest
from test.importers.CoMoToDataImporterTest import CoMoToDataImporterTest
from test.util.MetaPathUtilityTest import MetaPathUtilityTest

__author__ = 'jontedesco'

if __name__ == '__main__':

    # Data importer tests
    importerTestSuite = unittest.TestLoader().loadTestsFromTestCase(CoMoToDataImporterTest)
    importerTestSuite.addTests(unittest.TestLoader().loadTestsFromTestCase(ArnetMinerDataImporterTest))
    unittest.TextTestRunner(verbosity=2).run(importerTestSuite)

    # Utility tests
    utilityTestSuite = unittest.TestLoader().loadTestsFromTestCase(MetaPathUtilityTest)
    unittest.TextTestRunner(verbosity=2).run(utilityTestSuite)
