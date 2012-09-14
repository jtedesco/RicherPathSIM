import unittest
from networkx import networkx
from src.importer.ArnetMinerDataImporter import ArnetMinerDataImporter
from src.importer.error import ArnetParseError
from src.model.edge.dblp.Authorship import Authorship
from src.model.edge.dblp.Citation import Citation
from src.model.edge.dblp.Mention import Mention
from src.model.edge.dblp.Publication import Publication
from src.model.node.dblp.Author import Author
from src.model.node.dblp.Paper import Paper
from src.model.node.dblp.Topic import Topic
from src.model.node.dblp.Venue import Venue
from test.importers.ImporterTestHelper import addEdgesToGraph

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
            #@Author One,Author Two
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
                'authors': ['Author One', 'Author Two'],
                'conference': 'Modern Database Systems',
                'references': [],
                'title': 'Some paper title',
                'year': 1995
            },
            1: {
                'id': 1,
                'arnetid': 2,
                'authors': ['Author Two'],
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
                'authors': ['Author One'],
                'conference': 'Modern Database Systems',
                'references': [1],
                'title': 'Some paper title',
                'year': 1999
            },
            1: {
                'id': 1,
                'arnetid': 2,
                'authors': ['Author Two'],
                'conference': 'Modern Database Systems',
                'references': [],
                'title': 'Some other paper title',
                'year': 1995
            },
            2: {
                'id': 2,
                'arnetid': 3,
                'authors': ['Author Three'],
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


    def testSeparatePapersAuthorsVenuesSharedTopicGraph(self):

        # Build sample data & expected output
        parsedData = {
            0: {
                'id': 0,
                'arnetid': 1,
                'authors': ['Author One'],
                'conference': 'Conference One',
                'references': [],
                'title': 'Databases',
                'year': 1995
            },
            1: {
                'id': 1,
                'arnetid': 2,
                'authors': ['Author Two'],
                'conference': 'Conference Two',
                'references': [],
                'title': 'Databases',
                'year': 1999
            }
        }

        expectedGraph = networkx.DiGraph()

        # Expect unspecified ids to auto-increment
        author1 = Author(0, 'Author One')
        author2 = Author(1, 'Author Two')
        paper1 = Paper(0, 'Databases')
        paper2 = Paper(1, 'Databases')
        topic = Topic(0, ['databases'])
        venue1 = Venue(0, 'Conference One')
        venue2 = Venue(1, 'Conference Two')
        expectedGraph.add_node(author1)
        expectedGraph.add_node(author2)
        expectedGraph.add_node(paper1)
        expectedGraph.add_node(paper2)
        expectedGraph.add_node(topic)
        expectedGraph.add_node(venue1)
        expectedGraph.add_node(venue2)

        addEdgesToGraph(expectedGraph, author1, paper1, Authorship())
        addEdgesToGraph(expectedGraph, author2, paper2, Authorship())
        addEdgesToGraph(expectedGraph, paper1, topic, Mention())
        addEdgesToGraph(expectedGraph, paper2, topic, Mention())
        addEdgesToGraph(expectedGraph, paper1, venue1, Publication())
        addEdgesToGraph(expectedGraph, paper2, venue2, Publication())

        actualGraph = self.dataImporter.buildGraph(parsedData)

        self.assertEqual(actualGraph, expectedGraph)


    def testSeparatePapersAuthorsTopicSharedVenueGraph(self):

        # Build sample data & expected output
        parsedData = {
            0: {
                'id': 0,
                'arnetid': 1,
                'authors': ['Author One'],
                'conference': 'Conference One',
                'references': [],
                'title': 'Databases',
                'year': 1995
            },
            1: {
                'id': 1,
                'arnetid': 2,
                'authors': ['Author Two'],
                'conference': 'Conference One',
                'references': [],
                'title': 'Knowledge',
                'year': 1999
            }
        }

        expectedGraph = networkx.DiGraph()

        # Expect unspecified ids to auto-increment
        author1 = Author(0, 'Author One')
        author2 = Author(1, 'Author Two')
        paper1 = Paper(0, 'Databases')
        paper2 = Paper(1, 'Knowledge')
        topic1 = Topic(0, ['databases'])
        topic2 = Topic(0, ['knowledge'])
        venue = Venue(0, 'Conference One')
        expectedGraph.add_node(author1)
        expectedGraph.add_node(author2)
        expectedGraph.add_node(paper1)
        expectedGraph.add_node(paper2)
        expectedGraph.add_node(topic1)
        expectedGraph.add_node(topic2)
        expectedGraph.add_node(venue)

        addEdgesToGraph(expectedGraph, author1, paper1, Authorship())
        addEdgesToGraph(expectedGraph, author2, paper2, Authorship())
        addEdgesToGraph(expectedGraph, paper1, topic1, Mention())
        addEdgesToGraph(expectedGraph, paper2, topic2, Mention())
        addEdgesToGraph(expectedGraph, paper1, venue, Publication())
        addEdgesToGraph(expectedGraph, paper2, venue, Publication())

        actualGraph = self.dataImporter.buildGraph(parsedData)

        self.assertEqual(actualGraph, expectedGraph)


    def testSeparatePapersAuthorsSharedVenueTopicGraph(self):

        # Build sample data & expected output
        parsedData = {
            0: {
                'id': 0,
                'arnetid': 1,
                'authors': ['Author One'],
                'conference': 'Conference One',
                'references': [],
                'title': 'Databases',
                'year': 1995
            },
            1: {
                'id': 1,
                'arnetid': 2,
                'authors': ['Author Two'],
                'conference': 'Conference One',
                'references': [],
                'title': 'Databases',
                'year': 1999
            }
        }

        expectedGraph = networkx.DiGraph()

        # Expect unspecified ids to auto-increment
        author1 = Author(0, 'Author One')
        author2 = Author(1, 'Author Two')
        paper1 = Paper(0, 'Databases')
        paper2 = Paper(1, 'Knowledge')
        topic = Topic(0, ['databases'])
        venue = Venue(0, 'Conference One')
        expectedGraph.add_node(author1)
        expectedGraph.add_node(author2)
        expectedGraph.add_node(paper1)
        expectedGraph.add_node(paper2)
        expectedGraph.add_node(topic)
        expectedGraph.add_node(venue)

        addEdgesToGraph(expectedGraph, author1, paper1, Authorship())
        addEdgesToGraph(expectedGraph, author2, paper2, Authorship())
        addEdgesToGraph(expectedGraph, paper1, topic, Mention())
        addEdgesToGraph(expectedGraph, paper2, topic, Mention())
        addEdgesToGraph(expectedGraph, paper1, venue, Publication())
        addEdgesToGraph(expectedGraph, paper2, venue, Publication())

        actualGraph = self.dataImporter.buildGraph(parsedData)

        self.assertEqual(actualGraph, expectedGraph)


    def testCoAuthorsGraph(self):
        """
          Sample (simple) scenario as the first case, except that three authors exist, and two of them are co-authors.
        """

        # Build sample data & expected output
        parsedData = {
            0: {
                'id': 0,
                'arnetid': 1,
                'authors': ['Author One', 'Author Three'],
                'conference': 'Conference One',
                'references': [],
                'title': 'Databases',
                'year': 1995
            },
            1: {
                'id': 1,
                'arnetid': 2,
                'authors': ['Author Two'],
                'conference': 'Conference Two',
                'references': [],
                'title': 'Databases',
                'year': 1999
            }
        }

        expectedGraph = networkx.DiGraph()

        # Expect unspecified ids to auto-increment
        author1 = Author(0, 'Author One')
        author2 = Author(1, 'Author Two')
        author3 = Author(2, 'Author Three')
        paper1 = Paper(0, 'Databases')
        paper2 = Paper(1, 'Databases')
        topic = Topic(0, ['databases'])
        venue1 = Venue(0, 'Conference One')
        venue2 = Venue(1, 'Conference Two')
        expectedGraph.add_node(author1)
        expectedGraph.add_node(author2)
        expectedGraph.add_node(author3)
        expectedGraph.add_node(paper1)
        expectedGraph.add_node(paper2)
        expectedGraph.add_node(topic)
        expectedGraph.add_node(venue1)
        expectedGraph.add_node(venue2)

        addEdgesToGraph(expectedGraph, author1, paper1, Authorship())
        addEdgesToGraph(expectedGraph, author3, paper1, Authorship())
        addEdgesToGraph(expectedGraph, author2, paper2, Authorship())
        addEdgesToGraph(expectedGraph, paper1, topic, Mention())
        addEdgesToGraph(expectedGraph, paper2, topic, Mention())
        addEdgesToGraph(expectedGraph, paper1, venue1, Publication())
        addEdgesToGraph(expectedGraph, paper2, venue2, Publication())

        actualGraph = self.dataImporter.buildGraph(parsedData)

        self.assertEqual(actualGraph, expectedGraph)


    def testCitationFromSameConferenceGraph(self):

        # Build sample data & expected output
        parsedData = {
            0: {
                'id': 0,
                'arnetid': 1,
                'authors': ['Author One'],
                'conference': 'Conference One',
                'references': [],
                'title': 'Databases',
                'year': 1995
            },
            1: {
                'id': 1,
                'arnetid': 2,
                'authors': ['Author Two'],
                'conference': 'Conference One',
                'references': [0],
                'title': 'Databases',
                'year': 1999
            }
        }

        expectedGraph = networkx.DiGraph()

        # Expect unspecified ids to auto-increment
        author1 = Author(0, 'Author One')
        author2 = Author(1, 'Author Two')
        paper1 = Paper(0, 'Databases')
        paper2 = Paper(1, 'Knowledge')
        topic = Topic(0, ['databases'])
        venue = Venue(0, 'Conference One')
        expectedGraph.add_node(author1)
        expectedGraph.add_node(author2)
        expectedGraph.add_node(paper1)
        expectedGraph.add_node(paper2)
        expectedGraph.add_node(topic)
        expectedGraph.add_node(venue)

        addEdgesToGraph(expectedGraph, author1, paper1, Authorship())
        addEdgesToGraph(expectedGraph, author2, paper2, Authorship())
        addEdgesToGraph(expectedGraph, paper1, topic, Mention())
        addEdgesToGraph(expectedGraph, paper2, topic, Mention())
        addEdgesToGraph(expectedGraph, paper1, venue, Publication())
        addEdgesToGraph(expectedGraph, paper2, venue, Publication())

        # Not symmetric!
        expectedGraph.add_edge(paper2, paper1, Citation().toDict())

        actualGraph = self.dataImporter.buildGraph(parsedData)

        self.assertEqual(actualGraph, expectedGraph)


    def testCitationFromDifferentConferenceGraph(self):

        # Build sample data & expected output
        parsedData = {
            0: {
                'id': 0,
                'arnetid': 1,
                'authors': ['Author One'],
                'conference': 'Conference One',
                'references': [1],
                'title': 'Databases',
                'year': 2000
            },
            1: {
                'id': 1,
                'arnetid': 2,
                'authors': ['Author Two'],
                'conference': 'Conference Two',
                'references': [],
                'title': 'Databases',
                'year': 1999
            }
        }

        expectedGraph = networkx.DiGraph()

        # Expect unspecified ids to auto-increment
        author1 = Author(0, 'Author One')
        author2 = Author(1, 'Author Two')
        paper1 = Paper(0, 'Databases')
        paper2 = Paper(1, 'Databases')
        topic = Topic(0, ['databases'])
        venue1 = Venue(0, 'Conference One')
        venue2 = Venue(1, 'Conference Two')
        expectedGraph.add_node(author1)
        expectedGraph.add_node(author2)
        expectedGraph.add_node(paper1)
        expectedGraph.add_node(paper2)
        expectedGraph.add_node(topic)
        expectedGraph.add_node(venue1)
        expectedGraph.add_node(venue2)

        addEdgesToGraph(expectedGraph, author1, paper1, Authorship())
        addEdgesToGraph(expectedGraph, author2, paper2, Authorship())
        addEdgesToGraph(expectedGraph, paper1, topic, Mention())
        addEdgesToGraph(expectedGraph, paper2, topic, Mention())
        addEdgesToGraph(expectedGraph, paper1, venue1, Publication())
        addEdgesToGraph(expectedGraph, paper2, venue2, Publication())

        # Not symmetric!
        expectedGraph.add_edge(paper2, paper1, Citation().toDict())

        actualGraph = self.dataImporter.buildGraph(parsedData)

        self.assertEqual(actualGraph, expectedGraph)


    def testMutualCitationGraph(self):

        # Build sample data & expected output
        parsedData = {
            0: {
                'id': 0,
                'arnetid': 1,
                'authors': ['Author One'],
                'conference': 'Conference One',
                'references': [1],
                'title': 'Databases',
                'year': 1999
            },
            1: {
                'id': 1,
                'arnetid': 2,
                'authors': ['Author Two'],
                'conference': 'Conference Two',
                'references': [0],
                'title': 'Databases',
                'year': 1999
            }
        }

        expectedGraph = networkx.DiGraph()

        # Expect unspecified ids to auto-increment
        author1 = Author(0, 'Author One')
        author2 = Author(1, 'Author Two')
        paper1 = Paper(0, 'Databases')
        paper2 = Paper(1, 'Databases')
        topic = Topic(0, ['databases'])
        venue1 = Venue(0, 'Conference One')
        venue2 = Venue(1, 'Conference Two')
        expectedGraph.add_node(author1)
        expectedGraph.add_node(author2)
        expectedGraph.add_node(paper1)
        expectedGraph.add_node(paper2)
        expectedGraph.add_node(topic)
        expectedGraph.add_node(venue1)
        expectedGraph.add_node(venue2)

        addEdgesToGraph(expectedGraph, author1, paper1, Authorship())
        addEdgesToGraph(expectedGraph, author2, paper2, Authorship())
        addEdgesToGraph(expectedGraph, paper1, topic, Mention())
        addEdgesToGraph(expectedGraph, paper2, topic, Mention())
        addEdgesToGraph(expectedGraph, paper1, venue1, Publication())
        addEdgesToGraph(expectedGraph, paper2, venue2, Publication())

        # Symmetric in this case only!
        addEdgesToGraph(expectedGraph, paper1, paper2, Citation())

        actualGraph = self.dataImporter.buildGraph(parsedData)

        self.assertEqual(actualGraph, expectedGraph)


    def testSelfCitationGraph(self):

        # Build sample data & expected output
        parsedData = {
            0: {
                'id': 0,
                'arnetid': 1,
                'authors': ['Author One'],
                'conference': 'Conference One',
                'references': [1],
                'title': 'Databases',
                'year': 2001
            },
            1: {
                'id': 1,
                'arnetid': 2,
                'authors': ['Author One'],
                'conference': 'Conference Two',
                'references': [],
                'title': 'Databases',
                'year': 1999
            }
        }

        expectedGraph = networkx.DiGraph()

        # Expect unspecified ids to auto-increment
        author = Author(0, 'Author One')
        paper1 = Paper(0, 'Databases')
        paper2 = Paper(1, 'Databases')
        topic = Topic(0, ['databases'])
        venue1 = Venue(0, 'Conference One')
        venue2 = Venue(1, 'Conference Two')
        expectedGraph.add_node(author)
        expectedGraph.add_node(paper1)
        expectedGraph.add_node(paper2)
        expectedGraph.add_node(topic)
        expectedGraph.add_node(venue1)
        expectedGraph.add_node(venue2)

        addEdgesToGraph(expectedGraph, author, paper1, Authorship())
        addEdgesToGraph(expectedGraph, author, paper2, Authorship())
        addEdgesToGraph(expectedGraph, paper1, topic, Mention())
        addEdgesToGraph(expectedGraph, paper2, topic, Mention())
        addEdgesToGraph(expectedGraph, paper1, venue1, Publication())
        addEdgesToGraph(expectedGraph, paper2, venue2, Publication())

        # Not symmetric!
        expectedGraph.add_edge(paper1, paper2, Citation().toDict())

        actualGraph = self.dataImporter.buildGraph(parsedData)

        self.assertEqual(actualGraph, expectedGraph)
