from src.importer.FourAreaDataImporter import FourAreaDataImporter
from src.model.node.dblp.Author import Author
from src.model.node.dblp.Conference import Conference
from src.model.node.dblp.Paper import Paper
from src.model.node.dblp.Topic import Topic
from test.importers.ImporterTest import ImporterTest

__author__ = 'jontedesco'

class FourAreaDataImporterTest(ImporterTest):

    def setUp(self):
        self.dataImporter = FourAreaDataImporter('data/real/four_area', 'graphs/fourArea')


    def testBasicParsedIndexData(self):
        """
          Checks that the expected number of nodes are parsed from input files, and that parsed data is non-null
        """

        graph, actualNodeIndex = self.dataImporter.parseNodeContent({'author':{}})

        # For conferences, authors, and papers, count should be the same (don't check exact count for topics)
        expectedAuthorCount = 28702
        expectedConferenceCount = 20
        expectedPaperCount = 28569
        self.assertEquals(expectedAuthorCount, len(actualNodeIndex['author']))
        self.assertEquals(expectedConferenceCount, len(actualNodeIndex['conference']))
        self.assertEquals(expectedPaperCount, len(actualNodeIndex['paper']))

        # Assert that non-null data was parsed into all objects (including topics)
        for nodeType in actualNodeIndex:
            for nodeId in actualNodeIndex[nodeType]:
                nodeData = actualNodeIndex[nodeType][nodeId].toDict()
                for key in nodeData:
                    self.assertIsNotNone(nodeData[key])
                    nodeValue = len(nodeData[key]) if type(nodeData[key]) == type('') else nodeData[key]
                    self.assertTrue(nodeValue > 0)


    def testParsedIndexDataTopicKeywords(self):
        """
          Checks that the topics are parsed correctly (i.e. stop words are removed, and words are stemmed)
        """

        graph, actualNodeIndex = self.dataImporter.parseNodeContent({'author':{}})

        actualKeywords = set()
        for nodeId in actualNodeIndex['topic']:
            actualKeywords.add(actualNodeIndex['topic'][nodeId].keywords[0])

        # Check that a few stop words are removed
        sampleStopWords = {'of', 'the', 'for', 'or', 'to', 'a'}
        self.assertEqual(0, len(sampleStopWords.intersection(actualKeywords)))

        # Check that a few samples (known to be in the actual input) are properly stemmed
        stemmedRemovedWords = {'individuals', 'formalisms', 'challenges', 'challenging'}
        self.assertEqual(0, len(stemmedRemovedWords.intersection(actualKeywords)))

        # Check that the number of keywords is at least 20% smaller than the input keywords
        self.assertLess(len(actualKeywords), 13575 * 0.8)


    def testParsedGraphNodes(self):
        """
          Checks nodes are constructed corresponding to every entry in the index
        """

        graph, actualNodeIndex = self.dataImporter.parseNodeContent({'author':{}})

        expectedTypeCounts = {}
        for key in actualNodeIndex:
            expectedTypeCounts[key] = 0
            for nodeId in actualNodeIndex[key]:
                expectedTypeCounts[key] += 1

        actualTypeCounts = {
            'topic': 0,
            'paper': 0,
            'author': 0,
            'conference': 0
        }
        otherTypeCounts = 0
        for node in graph.getNodes():
            if isinstance(node, Topic):
                actualTypeCounts['topic'] += 1
            elif isinstance(node, Paper):
                actualTypeCounts['paper'] += 1
            elif isinstance(node, Conference):
                actualTypeCounts['conference'] += 1
            elif isinstance(node, Author):
                actualTypeCounts['author'] += 1
            else:
                otherTypeCounts += 1

        self.assertEquals(expectedTypeCounts, actualTypeCounts)
        self.assertEquals(0, otherTypeCounts)
