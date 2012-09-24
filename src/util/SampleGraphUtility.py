import networkx
from src.model.edge.dblp.Authorship import Authorship
from src.model.edge.dblp.Publication import Publication
from src.model.node.dblp.Author import Author
from src.model.node.dblp.Paper import Paper
from src.model.node.dblp.Venue import Venue
from src.util.GraphUtility import GraphUtility

__author__ = 'jontedesco'

class SampleGraphUtility(object):
    """
      Utility for creating sample graphs for unit testing and manual tests or experiments.
    """


    __nextId = 0


    @staticmethod
    def constructPathSimExampleThree():
        """
          Constructs "Example 3" from PathSim publication, ignoring topic nodes

            @see    http://citeseer.ist.psu.edu/viewdoc/summary?doi=10.1.1.220.2455
        """

        graph = networkx.DiGraph()
        authorMap = {}
        venueMap = {}

        # Add authors
        mike = Author(SampleGraphUtility.__getNextId(), 'Mike')
        jim = Author(SampleGraphUtility.__getNextId(), 'Jim')
        mary = Author(SampleGraphUtility.__getNextId(), 'Mary')
        bob = Author(SampleGraphUtility.__getNextId(), 'Bob')
        ann = Author(SampleGraphUtility.__getNextId(), 'Ann')
        authors = [mike, jim, mary, bob, ann]
        graph.add_nodes_from(authors)

        # Add conferences
        sigmod = Venue(SampleGraphUtility.__getNextId(), 'SIGMOD')
        vldb = Venue(SampleGraphUtility.__getNextId(), 'VLDB')
        icde = Venue(SampleGraphUtility.__getNextId(), 'ICDE')
        kdd = Venue(SampleGraphUtility.__getNextId(), 'KDD')
        venues = [sigmod, vldb, icde, kdd]
        graph.add_nodes_from([sigmod, vldb, icde, kdd])

        # Add author / venue index
        for author in authors:
            authorMap[author.name] = author
        for venue in venues:
            venueMap[venue.name] = venue

        # Add number of papers & edges mentioned in example
        SampleGraphUtility.__addSimilarAuthorsPapers(graph, mike, sigmod, vldb)
        for i in xrange(0, 70):
            conference = sigmod if i < 50 else vldb
            paper = Paper(SampleGraphUtility.__getNextId(), '%s Paper %d' % (conference.name, i + 1))
            graph.add_node(paper)
            GraphUtility.addEdgesToGraph(graph, jim, paper, Authorship())
            GraphUtility.addEdgesToGraph(graph, paper, conference, Publication())
        SampleGraphUtility.__addSimilarAuthorsPapers(graph, mary, sigmod, icde)
        SampleGraphUtility.__addSimilarAuthorsPapers(graph, bob, sigmod, vldb)
        annsPaper1 = Paper(SampleGraphUtility.__getNextId(), 'ICDE Paper')
        annsPaper2 = Paper(SampleGraphUtility.__getNextId(), 'KDD Paper')
        GraphUtility.addEdgesToGraph(graph, ann, annsPaper1, Authorship())
        GraphUtility.addEdgesToGraph(graph, ann, annsPaper2, Authorship())
        GraphUtility.addEdgesToGraph(graph, annsPaper1, icde, Publication())
        GraphUtility.addEdgesToGraph(graph, annsPaper2, kdd, Publication())

        return graph, authorMap, venueMap


    @staticmethod
    def __addSimilarAuthorsPapers(graph, author, sigmod, secondConference):
        """
          Helper function to construct the papers & edges associated with the three very similar authors in example 3.
          (i.e. Mike, Mary, and Bob). Will only construct the third paper if these papers are not from Mary.
        """

        paper1 = Paper(SampleGraphUtility.__getNextId(), 'SIGMOD Paper 1')
        paper2 = Paper(SampleGraphUtility.__getNextId(), 'SIGMOD Paper 2')
        graph.add_node(paper1)
        graph.add_node(paper2)

        GraphUtility.addEdgesToGraph(graph, author, paper1, Authorship())
        GraphUtility.addEdgesToGraph(graph, author, paper2, Authorship())
        GraphUtility.addEdgesToGraph(graph, paper1, sigmod, Publication())
        GraphUtility.addEdgesToGraph(graph, paper2, sigmod, Publication())

        paper3 = Paper(SampleGraphUtility.__getNextId(), 'Third Paper')
        graph.add_node(paper3)
        GraphUtility.addEdgesToGraph(graph, author, paper3, Authorship())
        GraphUtility.addEdgesToGraph(graph, paper3, secondConference, Publication())


    @staticmethod
    def __getNextId():
        """
          Increment (or initialize) nextId field, and return previous value (equivalent to ++ operator)
        """

        nextId = SampleGraphUtility.__nextId
        SampleGraphUtility.__nextId += 1
        return nextId