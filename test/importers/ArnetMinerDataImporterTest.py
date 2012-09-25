from src.graph.GraphFacade import GraphFacade
from src.importer.ArnetMinerDataImporter import ArnetMinerDataImporter
from src.importer.error.ArnetParseError import ArnetParseError
from src.model.edge.dblp.Authorship import Authorship
from src.model.edge.dblp.Citation import Citation
from src.model.edge.dblp.Mention import Mention
from src.model.edge.dblp.Publication import Publication
from src.model.node.dblp.Author import Author
from src.model.node.dblp.Paper import Paper
from src.model.node.dblp.Topic import Topic
from src.model.node.dblp.Conference import Conference
from test.importers.ImporterTest import ImporterTest

__author__ = 'jontedesco'

class ArnetMinerDataImporterTest(ImporterTest):
    """
      Unit tests for the ArnetMinerDataImporter
    """

    def setUp(self):
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


    def testSeparatePapersAuthorsConferencesSharedTopicGraph(self):

        # Build sample data & expected output
        parsedData = {
            0: {
                'id': 0,
                'arnetid': 1,
                'authors': ['Author One'],
                'conference': 'Conference One',
                'references': [],
                'title': 'All Databases',
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

        expectedGraph = GraphFacade.getInstance()

        # Expect unspecified ids to auto-increment
        author1 = Author(0, 'Author One')
        author2 = Author(1, 'Author Two')
        paper1 = Paper(0, 'All Databases')
        paper2 = Paper(1, 'Databases')
        topic = Topic(0, ['databas'])
        conference1 = Conference(0, 'Conference One')
        conference2 = Conference(1, 'Conference Two')
        expectedGraph.addNode(author1)
        expectedGraph.addNode(author2)
        expectedGraph.addNode(paper1)
        expectedGraph.addNode(paper2)
        expectedGraph.addNode(topic)
        expectedGraph.addNode(conference1)
        expectedGraph.addNode(conference2)

        expectedGraph.addBothEdges(author1, paper1, Authorship())
        expectedGraph.addBothEdges(author2, paper2, Authorship())
        expectedGraph.addBothEdges(paper1, topic, Mention())
        expectedGraph.addBothEdges(paper2, topic, Mention())
        expectedGraph.addBothEdges(paper1, conference1, Publication())
        expectedGraph.addBothEdges(paper2, conference2, Publication())

        actualGraph = self.dataImporter.buildGraph(parsedData)

        self.assertGraphsEqual(actualGraph, expectedGraph)


    def testSeparatePapersAuthorsTopicSharedConferenceGraph(self):

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
                'title': 'All The Knowledge',
                'year': 1999
            }
        }

        expectedGraph = GraphFacade.getInstance()

        # Expect unspecified ids to auto-increment
        author1 = Author(0, 'Author One')
        author2 = Author(1, 'Author Two')
        paper1 = Paper(0, 'Databases')
        paper2 = Paper(1, 'All The Knowledge')
        topic1 = Topic(0, ['databas'])
        topic2 = Topic(1, ['knowledg'])
        conference = Conference(0, 'Conference One')
        expectedGraph.addNode(author1)
        expectedGraph.addNode(author2)
        expectedGraph.addNode(paper1)
        expectedGraph.addNode(paper2)
        expectedGraph.addNode(topic1)
        expectedGraph.addNode(topic2)
        expectedGraph.addNode(conference)

        expectedGraph.addBothEdges(author1, paper1, Authorship())
        expectedGraph.addBothEdges(author2, paper2, Authorship())
        expectedGraph.addBothEdges(paper1, topic1, Mention())
        expectedGraph.addBothEdges(paper2, topic2, Mention())
        expectedGraph.addBothEdges(paper1, conference, Publication())
        expectedGraph.addBothEdges(paper2, conference, Publication())

        actualGraph = self.dataImporter.buildGraph(parsedData)

        self.assertGraphsEqual(actualGraph, expectedGraph)


    def testSeparatePapersAuthorsSharedConferenceTopicGraph(self):

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

        expectedGraph = GraphFacade.getInstance()

        # Expect unspecified ids to auto-increment
        author1 = Author(0, 'Author One')
        author2 = Author(1, 'Author Two')
        paper1 = Paper(0, 'Databases')
        paper2 = Paper(1, 'Databases')
        topic = Topic(0, ['databas'])
        conference = Conference(0, 'Conference One')
        expectedGraph.addNode(author1)
        expectedGraph.addNode(author2)
        expectedGraph.addNode(paper1)
        expectedGraph.addNode(paper2)
        expectedGraph.addNode(topic)
        expectedGraph.addNode(conference)

        expectedGraph.addBothEdges(author1, paper1, Authorship())
        expectedGraph.addBothEdges(author2, paper2, Authorship())
        expectedGraph.addBothEdges(paper1, topic, Mention())
        expectedGraph.addBothEdges(paper2, topic, Mention())
        expectedGraph.addBothEdges(paper1, conference, Publication())
        expectedGraph.addBothEdges(paper2, conference, Publication())

        actualGraph = self.dataImporter.buildGraph(parsedData)

        self.assertGraphsEqual(actualGraph, expectedGraph)


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

        expectedGraph = GraphFacade.getInstance()

        # Expect unspecified ids to auto-increment
        author1 = Author(0, 'Author One')
        author2 = Author(2, 'Author Two')
        author3 = Author(1, 'Author Three')
        paper1 = Paper(0, 'Databases')
        paper2 = Paper(1, 'Databases')
        topic = Topic(0, ['databas'])
        conference1 = Conference(0, 'Conference One')
        conference2 = Conference(1, 'Conference Two')
        expectedGraph.addNode(author1)
        expectedGraph.addNode(author2)
        expectedGraph.addNode(author3)
        expectedGraph.addNode(paper1)
        expectedGraph.addNode(paper2)
        expectedGraph.addNode(topic)
        expectedGraph.addNode(conference1)
        expectedGraph.addNode(conference2)

        expectedGraph.addBothEdges(author1, paper1, Authorship())
        expectedGraph.addBothEdges(author3, paper1, Authorship())
        expectedGraph.addBothEdges(author2, paper2, Authorship())
        expectedGraph.addBothEdges(paper1, topic, Mention())
        expectedGraph.addBothEdges(paper2, topic, Mention())
        expectedGraph.addBothEdges(paper1, conference1, Publication())
        expectedGraph.addBothEdges(paper2, conference2, Publication())

        actualGraph = self.dataImporter.buildGraph(parsedData)

        self.assertGraphsEqual(actualGraph, expectedGraph)


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

        expectedGraph = GraphFacade.getInstance()

        # Expect unspecified ids to auto-increment
        author1 = Author(0, 'Author One')
        author2 = Author(1, 'Author Two')
        paper1 = Paper(0, 'Databases')
        paper2 = Paper(1, 'Databases')
        topic = Topic(0, ['databas'])
        conference = Conference(0, 'Conference One')
        expectedGraph.addNode(author1)
        expectedGraph.addNode(author2)
        expectedGraph.addNode(paper1)
        expectedGraph.addNode(paper2)
        expectedGraph.addNode(topic)
        expectedGraph.addNode(conference)

        expectedGraph.addBothEdges(author1, paper1, Authorship())
        expectedGraph.addBothEdges(author2, paper2, Authorship())
        expectedGraph.addBothEdges(paper1, topic, Mention())
        expectedGraph.addBothEdges(paper2, topic, Mention())
        expectedGraph.addBothEdges(paper1, conference, Publication())
        expectedGraph.addBothEdges(paper2, conference, Publication())

        # Not symmetric!
        expectedGraph.addEdge(paper2, paper1, Citation())

        actualGraph = self.dataImporter.buildGraph(parsedData)

        self.assertGraphsEqual(actualGraph, expectedGraph)


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

        expectedGraph = GraphFacade.getInstance()

        # Expect unspecified ids to auto-increment
        author1 = Author(0, 'Author One')
        author2 = Author(1, 'Author Two')
        paper1 = Paper(0, 'Databases')
        paper2 = Paper(1, 'Databases')
        topic = Topic(0, ['databas'])
        conference1 = Conference(0, 'Conference One')
        conference2 = Conference(1, 'Conference Two')
        expectedGraph.addNode(author1)
        expectedGraph.addNode(author2)
        expectedGraph.addNode(paper1)
        expectedGraph.addNode(paper2)
        expectedGraph.addNode(topic)
        expectedGraph.addNode(conference1)
        expectedGraph.addNode(conference2)

        expectedGraph.addBothEdges(author1, paper1, Authorship())
        expectedGraph.addBothEdges(author2, paper2, Authorship())
        expectedGraph.addBothEdges(paper1, topic, Mention())
        expectedGraph.addBothEdges(paper2, topic, Mention())
        expectedGraph.addBothEdges(paper1, conference1, Publication())
        expectedGraph.addBothEdges(paper2, conference2, Publication())

        # Not symmetric!
        expectedGraph.addEdge(paper2, paper1, Citation())

        actualGraph = self.dataImporter.buildGraph(parsedData)

        self.assertGraphsEqual(actualGraph, expectedGraph)


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

        expectedGraph = GraphFacade.getInstance()

        # Expect unspecified ids to auto-increment
        author1 = Author(0, 'Author One')
        author2 = Author(1, 'Author Two')
        paper1 = Paper(0, 'Databases')
        paper2 = Paper(1, 'Databases')
        topic = Topic(0, ['databas'])
        conference1 = Conference(0, 'Conference One')
        conference2 = Conference(1, 'Conference Two')
        expectedGraph.addNode(author1)
        expectedGraph.addNode(author2)
        expectedGraph.addNode(paper1)
        expectedGraph.addNode(paper2)
        expectedGraph.addNode(topic)
        expectedGraph.addNode(conference1)
        expectedGraph.addNode(conference2)

        expectedGraph.addBothEdges(author1, paper1, Authorship())
        expectedGraph.addBothEdges(author2, paper2, Authorship())
        expectedGraph.addBothEdges(paper1, topic, Mention())
        expectedGraph.addBothEdges(paper2, topic, Mention())
        expectedGraph.addBothEdges(paper1, conference1, Publication())
        expectedGraph.addBothEdges(paper2, conference2, Publication())

        # Symmetric in this case only!
        expectedGraph.addBothEdges(paper1, paper2, Citation())

        actualGraph = self.dataImporter.buildGraph(parsedData)

        self.assertGraphsEqual(actualGraph, expectedGraph)


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

        expectedGraph = GraphFacade.getInstance()

        # Expect unspecified ids to auto-increment
        author = Author(0, 'Author One')
        paper1 = Paper(0, 'Databases')
        paper2 = Paper(1, 'Databases')
        topic = Topic(0, ['databas'])
        conference1 = Conference(0, 'Conference One')
        conference2 = Conference(1, 'Conference Two')
        expectedGraph.addNode(author)
        expectedGraph.addNode(paper1)
        expectedGraph.addNode(paper2)
        expectedGraph.addNode(topic)
        expectedGraph.addNode(conference1)
        expectedGraph.addNode(conference2)

        expectedGraph.addBothEdges(author, paper1, Authorship())
        expectedGraph.addBothEdges(author, paper2, Authorship())
        expectedGraph.addBothEdges(paper1, topic, Mention())
        expectedGraph.addBothEdges(paper2, topic, Mention())
        expectedGraph.addBothEdges(paper1, conference1, Publication())
        expectedGraph.addBothEdges(paper2, conference2, Publication())

        # Not symmetric!
        expectedGraph.addEdge(paper1, paper2, Citation())

        actualGraph = self.dataImporter.buildGraph(parsedData)

        self.assertGraphsEqual(actualGraph, expectedGraph)
