import math
from pprint import pprint
from src.graph.GraphFactory import GraphFactory
from src.model.edge.dblp.Authorship import Authorship
from src.model.edge.dblp.Citation import Citation
from src.model.edge.dblp.Publication import Publication
from src.model.node.dblp.Author import Author
from src.model.node.dblp.Paper import Paper
from src.model.node.dblp.Conference import Conference

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

        graph = GraphFactory.createInstance()
        authorMap = {}
        conferenceMap = {}

        # Add authors
        mike = Author(SampleGraphUtility.__getNextId(), 'Mike')
        jim = Author(SampleGraphUtility.__getNextId(), 'Jim')
        mary = Author(SampleGraphUtility.__getNextId(), 'Mary')
        bob = Author(SampleGraphUtility.__getNextId(), 'Bob')
        ann = Author(SampleGraphUtility.__getNextId(), 'Ann')
        authors = [mike, jim, mary, bob, ann]
        graph.addNodes(authors)

        # Add conferences
        sigmod = Conference(SampleGraphUtility.__getNextId(), 'SIGMOD')
        vldb = Conference(SampleGraphUtility.__getNextId(), 'VLDB')
        icde = Conference(SampleGraphUtility.__getNextId(), 'ICDE')
        kdd = Conference(SampleGraphUtility.__getNextId(), 'KDD')
        conferences = [sigmod, vldb, icde, kdd]
        graph.addNodes([sigmod, vldb, icde, kdd])

        # Add author / conference index
        for author in authors:
            authorMap[author.name] = author
        for conference in conferences:
            conferenceMap[conference.name] = conference

        # Add number of papers & edges mentioned in example
        SampleGraphUtility.__addSimilarAuthorsPapers(graph, mike, sigmod, vldb)
        for i in xrange(0, 70):
            conference = sigmod if i < 50 else vldb
            paper = Paper(SampleGraphUtility.__getNextId(), '%s Paper %d' % (conference.name, i + 1))
            graph.addNode(paper)
            graph.addBothEdges(jim, paper, Authorship())
            graph.addBothEdges(paper, conference, Publication())
        SampleGraphUtility.__addSimilarAuthorsPapers(graph, mary, sigmod, icde)
        SampleGraphUtility.__addSimilarAuthorsPapers(graph, bob, sigmod, vldb)
        annsPaper1 = Paper(SampleGraphUtility.__getNextId(), 'ICDE Paper')
        annsPaper2 = Paper(SampleGraphUtility.__getNextId(), 'KDD Paper')
        graph.addBothEdges(ann, annsPaper1, Authorship())
        graph.addBothEdges(ann, annsPaper2, Authorship())
        graph.addBothEdges(annsPaper1, icde, Publication())
        graph.addBothEdges(annsPaper2, kdd, Publication())

        return graph, authorMap, conferenceMap


    @staticmethod
    def constructMultiDisciplinaryAuthorExample():
        """
            Construct example DBLP graph where two authors are multi disciplinary, and no one else
        """

        # TODO: Change graph structure to be simple digraph, not mult-edge digraph (invalid for meta path definition)

        graph = GraphFactory.createInstance()
        authorMap = {}
        conferenceMap = {}

        # Add authors
        a = Author(SampleGraphUtility.__getNextId(), 'A')
        b = Author(SampleGraphUtility.__getNextId(), 'B')
        c = Author(SampleGraphUtility.__getNextId(), 'C')
        d = Author(SampleGraphUtility.__getNextId(), 'D')
        e = Author(SampleGraphUtility.__getNextId(), 'E')
        f = Author(SampleGraphUtility.__getNextId(), 'F')
        g = Author(SampleGraphUtility.__getNextId(), 'G')
        h = Author(SampleGraphUtility.__getNextId(), 'H')
        i = Author(SampleGraphUtility.__getNextId(), 'I')
        authors = [a,b,c,d,e,f,g,h,i]
        graph.addNodes(authors)

        # Add conferences
        sigmod = Conference(SampleGraphUtility.__getNextId(), 'SIGMOD') # Databases
        vldb = Conference(SampleGraphUtility.__getNextId(), 'VLDB') # Databases
        cikm = Conference(SampleGraphUtility.__getNextId(), 'CIKM') # Data mining
        kdd = Conference(SampleGraphUtility.__getNextId(), 'KDD') # Data mining
        conferences = [sigmod, vldb, cikm, kdd]
        graph.addNodes([sigmod, vldb, cikm, kdd])

        # Add author / conference index
        for author in authors:
            authorMap[author.name] = author
        for conference in conferences:
            conferenceMap[conference.name] = conference

        # Helper dictionary of total citation counts for each author (to fabricate) -- all divisible by 5, and multi-discipline authors divisible by 10
        # Results in the following total counts: {'A':100, 'B':80, 'C':12, 'D':120, 'E':80, 'F':100, 'G':80, 'H':12, 'I':}
        citationCounts = {'A':100, 'B':80, 'C':10, 'D':60, 'E':40, 'F':100, 'G':80, 'H':10, 'I':10} # Citations per paper
        paperMap = {} # Map of authors to the pairs of their papers

        # Create two papers for each author, one paper in each conference in each area
        dmAuthorNames = ['D', 'E', 'F', 'G', 'H', 'I']
        dbAuthorNames = ['A', 'B', 'C', 'D', 'E', 'I']
        dmConferenceNames = ['CIKM', 'KDD']
        dbConferenceNames = ['SIGMOD', 'VLDB']
        for prefix, authorNames, conferenceNames in [('dm-', dmAuthorNames, dmConferenceNames), ('db-', dbAuthorNames, dbConferenceNames)]:
            for authorName in authorNames:
                if authorName not in paperMap:
                    paperMap[prefix+authorName] = []
                for conferenceName in conferenceNames:
                    paper = Paper(SampleGraphUtility.__getNextId(), '%sPaperIn%s' % (authorName, conferenceName))
                    graph.addNode(paper)
                    graph.addBothEdges(authorMap[authorName], paper, Authorship())
                    graph.addBothEdges(paper, conferenceMap[conferenceName], Publication())
                    paperMap[prefix+authorName] = paperMap[prefix+authorName] + [paper]

        # Create equal number of citations from each other paper in the research area for each author's papers
        totalCitationCount = {}
        def f(x): totalCitationCount[x] = 0
        map(f, set(dmAuthorNames).union(set(dbAuthorNames)))
        for prefix, authorNames in [('dm-', dmAuthorNames), ('db-', dbAuthorNames)]:
            for authorName in authorNames:
                for citedPaper in paperMap[prefix+authorName]:

                    # Loop through papers of all other authors (4 per area)
                    for otherAuthorName in authorNames:
                        if authorName != otherAuthorName:
                            for citingPaper in paperMap[prefix+otherAuthorName]:
                                for j in xrange(0, (citationCounts[authorName] / (2*len(authorNames)-2))):
                                    graph.addEdge(citingPaper, citedPaper, Citation())
                                    totalCitationCount[authorName] += 1

        return graph, authorMap, conferenceMap, totalCitationCount


    @staticmethod
    def __addSimilarAuthorsPapers(graph, author, firstConference, secondConference):
        """
          Helper function to construct the papers & edges associated with the three very similar authors in example 3.
          (i.e. Mike, Mary, and Bob). Will only construct the third paper if these papers are not from Mary.
        """

        paper1 = Paper(SampleGraphUtility.__getNextId(), 'Paper 1')
        paper2 = Paper(SampleGraphUtility.__getNextId(), 'Paper 2')
        graph.addNode(paper1)
        graph.addNode(paper2)

        graph.addBothEdges(author, paper1, Authorship())
        graph.addBothEdges(author, paper2, Authorship())
        graph.addBothEdges(paper1, firstConference, Publication())
        graph.addBothEdges(paper2, firstConference, Publication())

        paper3 = Paper(SampleGraphUtility.__getNextId(), 'Paper 3')
        graph.addNode(paper3)
        graph.addBothEdges(author, paper3, Authorship())
        graph.addBothEdges(paper3, secondConference, Publication())


    @staticmethod
    def __getNextId():
        """
          Increment (or initialize) nextId field, and return previous value (equivalent to ++ operator)
        """

        nextId = SampleGraphUtility.__nextId
        SampleGraphUtility.__nextId += 1
        return nextId