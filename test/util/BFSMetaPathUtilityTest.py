from src.graph.GraphFactory import GraphFactory
from src.model.edge.dblp.Authorship import Authorship
from src.model.edge.dblp.Citation import Citation
from src.model.edge.dblp.Publication import Publication
from src.model.node.dblp.Author import Author
from src.model.node.dblp.Conference import Conference
from src.model.node.dblp.Paper import Paper
from src.util.BFSMetaPathUtility import BFSMetaPathUtility
from test.util.MetaPathUtilityTest import MetaPathUtilityTest

__author__ = 'jontedesco'

class BFSMetaPathUtilityTest(MetaPathUtilityTest):
    """
      Tests the depth-first-search implementation of the meta path utility.
    """

    def setUp(self):

        self.maxDiff = None

        # Construct template graph for tests
        graph = GraphFactory.createInstance()

        # Put references to graph objects on test object
        self.author = Author(0, 'author')
        self.coauthor = Author(1, 'coauthor')
        self.conference1 = Conference(0, 'conference1')
        self.conference2 = Conference(1, 'conference2')
        self.paper1 = Paper(0, 'paper1')
        self.paper2 = Paper(1, 'paper2')
        self.paper3 = Paper(2, 'paper3')

        # Construct graph
        graph.addNodes([self.author, self.conference1, self.conference2, self.paper1, self.paper2, self.paper3])
        graph.addBothEdges(self.paper1, self.author, Authorship())
        graph.addBothEdges(self.paper2, self.author, Authorship())
        graph.addBothEdges(self.paper3, self.author, Authorship())
        graph.addBothEdges(self.paper3, self.coauthor, Authorship())
        graph.addBothEdges(self.paper1, self.conference1, Publication())
        graph.addBothEdges(self.paper2, self.conference1, Publication())
        graph.addBothEdges(self.paper3, self.conference2, Publication())
        graph.addEdge(self.paper1, self.paper2, Citation())
        graph.addBothEdges(self.paper2, self.paper3, Citation())

        self.templateGraph = graph

        self.metaPathUtility = BFSMetaPathUtility()
