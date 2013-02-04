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
    def constructPathSimExampleThree(extraAuthors = False):
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
        if extraAuthors:
            joe = Author(SampleGraphUtility.__getNextId(), 'Joe')
            nancy = Author(SampleGraphUtility.__getNextId(), 'Nancy')
            authors += [joe, nancy]
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

        # Add extra authors & citation data
        if extraAuthors:
            SampleGraphUtility.__addSimilarAuthorsPapers(graph, joe, sigmod, vldb)
            SampleGraphUtility.__addSimilarAuthorsPapers(graph, nancy, sigmod, vldb)

        return graph, authorMap, conferenceMap


    @staticmethod
    def constructMultiDisciplinaryAuthorExample():
        """
            Construct example DBLP graph where two authors are multi disciplinary, and no one else
        """

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
        # Results in the following total counts: {'A':100, 'B':80, 'C':10, 'D':120, 'E':60, 'F':100, 'G':80, 'H':10, 'I':24}
        citationCounts = {'A':100, 'B':80, 'C':10, 'D':60, 'E':30, 'F':100, 'G':80, 'H':10, 'I':12} # Citations per paper

        # Create two papers for each author, one paper in each conference in each area
        dmAuthorNames = ['D', 'E', 'F', 'G', 'H', 'I']
        dbAuthorNames = ['A', 'B', 'C', 'D', 'E', 'I']
        duplicateNames = set(dmAuthorNames).intersection(set(dbAuthorNames))
        dmConferenceNames = ['CIKM', 'KDD']
        dbConferenceNames = ['SIGMOD', 'VLDB']

        # Create equal number of citations from each other paper in the research area for each author's papers
        totalCitationCount = {}
        def f(x): totalCitationCount[x] = 0
        map(f, set(dmAuthorNames).union(set(dbAuthorNames)))
        for authorNames, conferenceNames in [(dmAuthorNames, dmConferenceNames), (dbAuthorNames, dbConferenceNames)]:
            for authorName in authorNames:

                totalCitationCount[authorName] = 0

                citedPaperMap = {}
                for conferenceName in conferenceNames:

                    # Add paper to be cited for author
                    citedPaper = Paper(SampleGraphUtility.__getNextId(), '%sPaperIn%s' % (authorName, conferenceName))
                    graph.addNode(citedPaper)
                    graph.addBothEdges(citedPaper, conferenceMap[conferenceName], Publication())
                    graph.addBothEdges(citedPaper, authorMap[authorName], Authorship())

                    citedPaperMap[conferenceName] = citedPaper

                # Figure out the number of incoming citation for this author from each other eligible authors
                if authorName in duplicateNames:
                    citingAuthors = set(authorNames).difference(duplicateNames)
                else:
                    citingAuthors = set(authorNames)
                    citingAuthors.remove(authorName)
                numberOfIncomingCitationsPerAuthor = citationCounts[authorName] / len(citingAuthors)

                # Loop through papers of all other authors
                for otherAuthorName in citingAuthors:
                    if authorName == otherAuthorName: continue
                    for conferenceName in conferenceNames:
                        for i in xrange(0, numberOfIncomingCitationsPerAuthor):

                            # Add fake paper for citing the other author
                            citingPaper = Paper(SampleGraphUtility.__getNextId(), 'Citation%d%sPaperIn%s' % (i, otherAuthorName, conferenceName))
                            graph.addNode(citingPaper)
                            graph.addBothEdges(authorMap[otherAuthorName], citingPaper, Authorship())
                            graph.addBothEdges(citingPaper, conferenceMap[conferenceName], Publication())

                            # Add citation
                            graph.addEdge(citingPaper, citedPaperMap[conferenceName], Citation())
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