import unittest
from test.importers.ArnetMinerDataImporterTest import ArnetMinerDataImporterTest
from test.importers.CoMoToDataImporterTest import CoMoToDataImporterTest
from test.importers.DBISDataImporterTest import DBISDataImporterTest
from test.importers.FourAreaDataImporterTest import FourAreaDataImporterTest
from test.model.GraphObjectFactoryTest import GraphObjectFactoryTest
from test.similarity.heterogeneous.PathSimStrategyTest import PathSimStrategyTest
from test.similarity.heterogeneous.ProjectedPageRankStrategyTest import ProjectedPageRankStrategyTest
from test.similarity.homogeneous.PageRankStrategyTest import PageRankStrategyTest
from test.util.BFSMetaPathUtilityTest import BFSMetaPathUtilityTest
from test.util.DFSMetaPathUtilityTest import DFSMetaPathUtilityTest
from test.util.EdgeBasedMetaPathUtilityTest import EdgeBasedMetaPathUtilityTest
from test.util.SampleGraphUtilityTest import SampleGraphUtilityTest

__author__ = 'jontedesco'

if __name__ == '__main__':

    # Data importer tests
    importerTestSuite = unittest.TestLoader().loadTestsFromTestCase(CoMoToDataImporterTest)
    importerTestSuite.addTests(unittest.TestLoader().loadTestsFromTestCase(ArnetMinerDataImporterTest))
    importerTestSuite.addTests(unittest.TestLoader().loadTestsFromTestCase(DBISDataImporterTest))
    importerTestSuite.addTests(unittest.TestLoader().loadTestsFromTestCase(FourAreaDataImporterTest))
    unittest.TextTestRunner().run(importerTestSuite)

    # Model tests
    utilityTestSuite = unittest.TestLoader().loadTestsFromTestCase(GraphObjectFactoryTest)
    unittest.TextTestRunner().run(utilityTestSuite)

    # Strategy tests
    strategyTestSuite = unittest.TestLoader().loadTestsFromTestCase(PageRankStrategyTest)
    strategyTestSuite.addTests(unittest.TestLoader().loadTestsFromTestCase(PathSimStrategyTest))
    strategyTestSuite.addTests(unittest.TestLoader().loadTestsFromTestCase(ProjectedPageRankStrategyTest))
    unittest.TextTestRunner().run(strategyTestSuite)

    # Utility tests
    utilityTestSuite = unittest.TestLoader().loadTestsFromTestCase(DFSMetaPathUtilityTest)
    utilityTestSuite.addTests(unittest.TestLoader().loadTestsFromTestCase(BFSMetaPathUtilityTest))
    utilityTestSuite.addTests(unittest.TestLoader().loadTestsFromTestCase(EdgeBasedMetaPathUtilityTest))
    utilityTestSuite.addTests(unittest.TestLoader().loadTestsFromTestCase(SampleGraphUtilityTest))
    unittest.TextTestRunner().run(utilityTestSuite)
