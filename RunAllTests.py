import unittest
from test.importers.ArnetMinerDataImporterTest import ArnetMinerDataImporterTest
from test.importers.CoMoToDataImporterTest import CoMoToDataImporterTest
from test.similarity.homogeneous.PageRankStrategyTest import PageRankStrategyTest
from test.util.MetaPathUtilityTest import MetaPathUtilityTest
from test.util.SampleGraphUtilityTest import SampleGraphUtilityTest

__author__ = 'jontedesco'

if __name__ == '__main__':

    # Data importer tests
    importerTestSuite = unittest.TestLoader().loadTestsFromTestCase(CoMoToDataImporterTest)
    importerTestSuite.addTests(unittest.TestLoader().loadTestsFromTestCase(ArnetMinerDataImporterTest))
    unittest.TextTestRunner(verbosity=2).run(importerTestSuite)

    # Utility tests
    utilityTestSuite = unittest.TestLoader().loadTestsFromTestCase(MetaPathUtilityTest)
    utilityTestSuite.addTests(unittest.TestLoader().loadTestsFromTestCase(SampleGraphUtilityTest))
    unittest.TextTestRunner(verbosity=2).run(utilityTestSuite)

    # Strategy tests
    strategyTestSuite = unittest.TestLoader().loadTestsFromTestCase(PageRankStrategyTest)
    unittest.TextTestRunner(verbosity=2).run(strategyTestSuite)