from collections import defaultdict
import random
import itertools
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
    def constructSkewedCitationPublicationExample(introduceRandomness=True, citationsPublicationsParameter=None):
        """
          Build the graph for an example with skewed citation / publication count ratios

            NOTE: Extraneous authors are omitted
        """

        graph = GraphFactory.createInstance()
        random.seed()

        # Create the authors & conference
        alice = Author(SampleGraphUtility.__getNextId(), 'Alice')
        bob = Author(SampleGraphUtility.__getNextId(), 'Bob')
        carol = Author(SampleGraphUtility.__getNextId(), 'Carol')
        dave = Author(SampleGraphUtility.__getNextId(), 'Dave')
        ed = Author(SampleGraphUtility.__getNextId(), 'Ed')
        frank = Author(SampleGraphUtility.__getNextId(), 'Frank')
        authors = [alice, bob, carol, dave, ed, frank]
        authorMap = {author.name: author for author in authors}
        conference = Conference(SampleGraphUtility.__getNextId(), 'KDD')

        # Citation & publication count configuration
        if citationsPublicationsParameter is not None:
            citationsPublications = citationsPublicationsParameter
        else:
            citationsPublications = {
                'Alice': (100, 10),
                'Bob': (80, 10),
                'Carol': (100, 100),
                'Dave': (50, 10),
                'Ed': (10, 10),
                'Frank': (1000, 100)
            }

        actualCitationsPublications = defaultdict(lambda: (0, 0))

        # Helper functions for repeatedly adding papers to the graph
        addPapersToAuthor = lambda n, author: [addPublicationPaper(author) for _ in itertools.repeat(None, n)]
        addCitationsToPaper = lambda n, paper, author: [addCitationPaper(paper, author) for _ in itertools.repeat(None, n)]

        def addPublicationPaper(author):
            """
              Helper method to add a 'publication' paper, connected to both an author and a conference
            """
            nextId = SampleGraphUtility.__getNextId()
            paper = Paper(nextId, "%s's Paper %d" % (author.name, nextId))
            graph.addNode(paper)
            graph.addBothEdges(author, paper)
            graph.addBothEdges(paper, conference)

            citationCount, publicationCount = actualCitationsPublications[author]
            actualCitationsPublications[author] = (citationCount, publicationCount + 1)

            return paper

        def addCitationPaper(citedPaper, citedAuthor):
            """
              Helper method to add a 'citation' paper, which is only connected to the conference and the paper it cites
            """
            nextId = SampleGraphUtility.__getNextId()
            citingPaper = Paper(nextId, "Citing Paper %d" % nextId)
            graph.addNode(citingPaper)
            graph.addBothEdges(citingPaper, conference)
            graph.addEdge(citingPaper, citedPaper)

            citationCount, publicationCount = actualCitationsPublications[citedAuthor]
            actualCitationsPublications[citedAuthor] = (citationCount + 1, publicationCount)

        # Construct the graph
        graph.addNodes(authors + [conference])
        for authorName in citationsPublications:
            citationCount, publicationCount = citationsPublications[authorName]

            # Optionally, introduce randomness
            if introduceRandomness:
                randomInterval = lambda x: (x + int(-0.1 * x), x + int(0.1 * x))
                citationCount = random.randint(*randomInterval(citationCount))
                publicationCount = random.randint(*randomInterval(publicationCount))

            # Add citations & publications to author
            authorPapers = addPapersToAuthor(publicationCount, authorMap[authorName])
            citationsPerPaper = citationCount / publicationCount
            remainingCitationsPerPaper = citationCount % publicationCount
            for paper in authorPapers:
                addCitationsToPaper(citationsPerPaper, paper, authorMap[authorName])
                if actualCitationsPublications[authorMap[authorName]][0] < citationsPublications[authorName][0] \
                        and remainingCitationsPerPaper > 0:
                    addCitationsToPaper(remainingCitationsPerPaper, paper, authorMap[authorName])

        return graph, authorMap, conference, actualCitationsPublications


    @staticmethod
    def constructPathSimExampleThree(extraAuthorsAndCitations=False, citationMap=None):
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
        if extraAuthorsAndCitations:
            joe = Author(SampleGraphUtility.__getNextId(), 'Joe')
            nancy = Author(SampleGraphUtility.__getNextId(), 'Nancy')
            authors += [joe, nancy]
        else:
            joe, nancy = None, None
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

        # Add author / conference / papers index
        authorConferencePaperMap = defaultdict(lambda : defaultdict(list))

        # Add jim's papers
        for i in xrange(0, 70):
            conference = sigmod if i < 50 else vldb
            paper = Paper(SampleGraphUtility.__getNextId(), '%s Paper %d' % (conference.name, i + 1))
            graph.addNode(paper)
            graph.addBothEdges(jim, paper, Authorship())
            graph.addBothEdges(paper, conference, Publication())
            authorConferencePaperMap[jim][conference].append(paper)

        # Add ann's papers
        annsPaper1 = Paper(SampleGraphUtility.__getNextId(), 'ICDE Paper')
        annsPaper2 = Paper(SampleGraphUtility.__getNextId(), 'KDD Paper')
        graph.addBothEdges(ann, annsPaper1, Authorship())
        graph.addBothEdges(ann, annsPaper2, Authorship())
        graph.addBothEdges(annsPaper1, icde, Publication())
        graph.addBothEdges(annsPaper2, kdd, Publication())
        authorConferencePaperMap[ann][icde].append(annsPaper1)
        authorConferencePaperMap[ann][kdd].append(annsPaper2)

        # Auto-add remaining authors (2,1) paper numbers
        SampleGraphUtility.__addSimilarAuthorsPapers(graph, mike, sigmod, vldb, authorConferencePaperMap)
        SampleGraphUtility.__addSimilarAuthorsPapers(graph, mary, sigmod, icde, authorConferencePaperMap)
        SampleGraphUtility.__addSimilarAuthorsPapers(graph, bob, sigmod, vldb, authorConferencePaperMap)

        # Add extra authors & citation data
        if extraAuthorsAndCitations:
            SampleGraphUtility.__addSimilarAuthorsPapers(graph, joe, sigmod, vldb, authorConferencePaperMap)
            SampleGraphUtility.__addSimilarAuthorsPapers(graph, nancy, sigmod, vldb, authorConferencePaperMap)
            SampleGraphUtility.__constructCitations(graph, authorMap, conferenceMap, authorConferencePaperMap, citationMap)

        return graph, authorMap, conferenceMap


    @staticmethod
    def __constructCitations(graph, authorMap, conferenceMap, acpMap, citationMap):
        """
          Add citations
        """

        def addCitations(authorOne, authorTwo, n):

            if n == 0: return

            # Find the shared conferences
            sharedConferences = []
            for conferenceName, conference in conferenceMap.iteritems():
                if len(acpMap[authorOne][conference]) > 0 and len(acpMap[authorTwo][conference]) > 0:
                    sharedConferences.append(conference)


            incomplete = True

            # Loop through shared conferences between authors until we find something that makes sense
            attempt = -1
            while incomplete:
                attempt += 1
                sharedConference = sharedConferences[attempt]

                # Cite the author, skip if it's not possible
                papersToCiteFrom = acpMap[authorOne][sharedConference]
                papersToCite = acpMap[authorTwo][sharedConference] # just select one of the papers published in the shared conference
                if n > len(papersToCiteFrom) * len(papersToCite):
                    continue
                for i in xrange(0, n):

                    if n > len(papersToCiteFrom):
                        paperToCiteFrom = papersToCiteFrom[0]
                        paperToCite = papersToCite[i]
                    else:
                        paperToCiteFrom = papersToCiteFrom[i]
                        paperToCite = papersToCite[0]

                    graph.addEdge(paperToCiteFrom, paperToCite, Citation())

                incomplete = False


        for citingAuthorName in citationMap:
            for citedAuthorName in citationMap[citingAuthorName]:
                numCitations = citationMap[citingAuthorName][citedAuthorName]
                addCitations(authorMap[citingAuthorName], authorMap[citedAuthorName], numCitations)


    @staticmethod
    def constructMultiDisciplinaryAuthorExample(indirectAuthor=False, uneven=False):
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
        authors = [a, b, c, d, e, f, g, h, i]
        if indirectAuthor:
            authors.append(Author(SampleGraphUtility.__getNextId(), 'J'))
        graph.addNodes(authors)

        # Add conferences
        vldb = Conference(SampleGraphUtility.__getNextId(), 'VLDB')  # Databases
        kdd = Conference(SampleGraphUtility.__getNextId(), 'KDD')  # Data mining
        conferences = [vldb, kdd]
        graph.addNodes(conferences)

        # Add author / conference index
        for author in authors:
            authorMap[author.name] = author
        for conference in conferences:
            conferenceMap[conference.name] = conference

        # Helper dictionary of total citation counts for each author (to fabricate) -- all divisible by 5, and multi-discipline authors divisible by 10
        # Results in the following total counts: {'A':100, 'B':80, 'C':10, 'D':120, 'E':60, 'F':100, 'G':80, 'H':10, 'I':24}
        citationCounts = {'A': 100, 'B': 80, 'C': 10, 'D': 60, 'E': 45, 'F': 100, 'G': 80, 'H': 10, 'I': 12, 'J': 60}

        # Create two papers for each author, one paper in each conference in each area
        dmAuthorNames = ['D', 'E', 'F', 'G', 'H', 'I']
        dbAuthorNames = ['A', 'B', 'C', 'D', 'E', 'I']
        if indirectAuthor:
            dmAuthorNames += ['J']
            dbAuthorNames += ['J']
        duplicateNames = set(dmAuthorNames).intersection(set(dbAuthorNames))
        dmConferenceNames = ['KDD']
        dbConferenceNames = ['VLDB']

        def f(x):
            totalCitationCount[x] = 0

        # Create equal number of citations from each other paper in the research area for each author's papers
        totalCitationCount = defaultdict(int)
        map(f, set(dmAuthorNames).union(set(dbAuthorNames)))
        for authorNames, conferenceNames in [(dmAuthorNames, dmConferenceNames), (dbAuthorNames, dbConferenceNames)]:
            for authorName in authorNames:

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
                citationsPerAuthor = citationCounts[authorName] / len(citingAuthors)

                # Make sure J is cited by the two non-D multi-disciplinary authors
                if authorName == 'J':
                    citationsPerAuthor = citationCounts[authorName] / 2
                    citingAuthors = ['E', 'I']

                # Loop through papers of all other authors
                for otherAuthorName in citingAuthors:
                    if authorName == otherAuthorName: continue
                    for conferenceName in conferenceNames:
                        for i in xrange(0, citationsPerAuthor):

                            # Add fake paper for citing the other author
                            citingPaper = Paper(SampleGraphUtility.__getNextId(), 'Citation%d%sPaperIn%s' % (i, otherAuthorName, conferenceName))
                            graph.addNode(citingPaper)
                            graph.addBothEdges(authorMap[otherAuthorName], citingPaper, Authorship())
                            graph.addBothEdges(citingPaper, conferenceMap[conferenceName], Publication())

                            # Add citation
                            graph.addEdge(citingPaper, citedPaperMap[conferenceName], Citation())
                            totalCitationCount[authorName] += 1

        if not uneven:
            return graph, authorMap, conferenceMap, totalCitationCount

        # If this flag is set, add three papers per author in data mining, and citations from all other authors
        for authorNamesList, conferenceNamesList in \
                [(dmAuthorNames, dmConferenceNames), (dbAuthorNames, dbConferenceNames)]:

            extraPapers = []

            # Add publications
            for authorName in authorNamesList:
                for conferenceName in conferenceNamesList:

                    # Add paper to be cited for author
                    citedPaper = Paper(SampleGraphUtility.__getNextId(), '%sPaperIn%s' % (authorName, conferenceName))
                    graph.addNode(citedPaper)
                    graph.addBothEdges(citedPaper, conferenceMap[conferenceName], Publication())
                    graph.addBothEdges(citedPaper, authorMap[authorName], Authorship())
                    extraPapers.append((authorName, citedPaper))

            random.seed()

            # Add randomized citations from authors to these papers
            for citingAuthorName in authorNamesList:
                for conferenceName in conferenceNamesList:
                    for citedAuthorName, citedPaper in extraPapers:

                        # Skip papers authored by this author
                        if citedAuthorName == citingAuthorName:
                            continue

                        # Randomly add a number of citations to this paper
                        for i in xrange(0, random.randint(0, 3)):

                            # Add fake paper for citing the other author
                            citingPaper = Paper(SampleGraphUtility.__getNextId(), 'Citation%d%sPaperIn%s' % (
                                i, citingAuthorName, conferenceName
                            ))
                            graph.addNode(citingPaper)
                            graph.addBothEdges(authorMap[citingAuthorName], citingPaper, Authorship())
                            graph.addBothEdges(citingPaper, conferenceMap[conferenceName], Publication())

                            # Add citation
                            graph.addEdge(citingPaper, citedPaper, Citation())
                            totalCitationCount[citedAuthorName] += 1



        return graph, authorMap, conferenceMap, totalCitationCount


    @staticmethod
    def __addSimilarAuthorsPapers(graph, author, firstConference, secondConference, authorConferencePaperMap):
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
        authorConferencePaperMap[author][firstConference].append(paper1)
        authorConferencePaperMap[author][firstConference].append(paper2)

        paper3 = Paper(SampleGraphUtility.__getNextId(), 'Paper 3')
        graph.addNode(paper3)
        graph.addBothEdges(author, paper3, Authorship())
        graph.addBothEdges(paper3, secondConference, Publication())
        authorConferencePaperMap[author][secondConference].append(paper3)


    @staticmethod
    def __getNextId():
        """
          Increment (or initialize) nextId field, and return previous value (equivalent to ++ operator)
        """

        nextId = SampleGraphUtility.__nextId
        SampleGraphUtility.__nextId += 1
        return nextId