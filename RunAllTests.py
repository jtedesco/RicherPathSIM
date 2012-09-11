import unittest
from test.importers.ArnetMinerDataImporterTest import ArnetMinerDataImporterTest
from test.importers.CoMoToDataImporterTest import CoMoToDataImporterTest

__author__ = 'jontedesco'

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(CoMoToDataImporterTest)
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(ArnetMinerDataImporterTest))

    unittest.TextTestRunner(verbosity=2).run(suite)