import unittest
from src.importer.ArnetMinerDataImporter import ArnetMinerDataImporter
from src.importer.error import ArnetParseError

__author__ = 'jontedesco'

class ArnetMinerDataImporterTest(unittest.TestCase):
    """
      Unit tests for the ArnetMinerDataImporter
    """

    def setUp(self):

        """

        """
        self.dataImporter = ArnetMinerDataImporter(None, None)

    def testParsePapersWithoutCitationsInput(self):

        papersWithoutCitationsInput = """
            #*Some paper title
            #@Author One
            #year1995
            #confModern Database Systems
            #citation-1
            #index0
            #arnetid1

            #*Some other paper title
            #@Author Two
            #year1999
            #confModern Database Systems
            #citation0
            #index1
            #arnetid2
            #!Some really long abstract
        """

        expectedParsedData = {
            0: {
                'id': 0,
                'arnetid': 1,
                'author': 'Author One',
                'conference': 'Modern Database Systems',
                'references': [],
                'title': 'Some paper title',
                'year': 1995
            },
            1: {
                'id': 1,
                'arnetid': 2,
                'author': 'Author Two',
                'conference': 'Modern Database Systems',
                'references': [],
                'title': 'Some other paper title',
                'year': 1999
            }
        }

        actualParsedData = self.dataImporter.parseInputContent(papersWithoutCitationsInput)

        self.assertDictEqual(actualParsedData, expectedParsedData)


    def testParsePapersWithCorrectCitationsInput(self):

        papersWithCorrectCitationsInput = """
            #*Some paper title
            #@Author One
            #year1999
            #confModern Database Systems
            #citation1
            #index0
            #arnetid1
            #%1
            #!Some really long abstract

            #*Some other paper title
            #@Author Two
            #year1995
            #confModern Database Systems
            #citation2
            #index1
            #arnetid2

            #*Yet another paper title
            #@Author Three
            #year2005
            #confData Mining
            #citation0
            #index2
            #arnetid3
            #%0
            #%1
        """

        expectedParsedData = {
            0: {
                'id': 0,
                'arnetid': 1,
                'author': 'Author One',
                'conference': 'Modern Database Systems',
                'references': [1],
                'title': 'Some paper title',
                'year': 1999
            },
            1: {
                'id': 1,
                'arnetid': 2,
                'author': 'Author Two',
                'conference': 'Modern Database Systems',
                'references': [],
                'title': 'Some other paper title',
                'year': 1995
            },
            2: {
                'id': 2,
                'arnetid': 3,
                'author': 'Author Three',
                'conference': 'Data Mining',
                'references': [0,1],
                'title': 'Yet another paper title',
                'year': 2005
            }
        }

        actualParsedData = self.dataImporter.parseInputContent(papersWithCorrectCitationsInput)

        self.assertDictEqual(actualParsedData, expectedParsedData)


    def testParsePapersWithInvalidCitationsInput(self):

        papersWithInvalidCitationsInput = """
            #*Some paper title
            #@Author One
            #year1995
            #confModern Database Systems
            #citation-1
            #index0
            #arnetid1
            #%4
            #%5

            #*Some other paper title
            #@Author Two
            #year1999
            #confModern Database Systems
            #citation0
            #index1
            #arnetid2
        """

        try:
            self.dataImporter.parseInputContent(papersWithInvalidCitationsInput)
            self.fail("Should have failed to parse input with invalid citations")
        except ArnetParseError:
            pass


    def testParseMissingPaperAttributesInput(self):

        papersWithMissingAttributesInput = """
            #*Some paper title
            #@Author One
            #year1995
            #arnetid1

            #*Some other paper title
            #@Author Two
            #year1999
            #confModern Database Systems
            #citation0
            #index1
            #arnetid2
        """

        try:
            self.dataImporter.parseInputContent(papersWithMissingAttributesInput)
            self.fail("Should have failed to parse input with missing attributes")
        except ArnetParseError:
            pass
