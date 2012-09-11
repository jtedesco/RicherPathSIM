import unittest
from src.importers.ArnetMinerDataImporter import ArnetMinerDataImporter

__author__ = 'jontedesco'

class ArnetMinerDataImporterTest(unittest.TestCase):
    """
      Unit tests for the ArnetMinerDataImporter
    """

    def setUp(self):

        self.dataImporter = ArnetMinerDataImporter(None, None)

        pass

    def testParseSimplePapersWithoutCitationsInput(self):
        # Test both -1 and 0 for citations
        pass

    def testParseSimplePapersWithCorrectCitationsInput(self):
        pass

    def testParseSimplePapersWithInvalidCitationsInput(self):
        pass

    def testMissingPaperAttributesInput(self):
        pass

    def testExtraPaperAttributesInput(self):
        pass
