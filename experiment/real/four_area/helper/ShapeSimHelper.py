from collections import defaultdict
import itertools
from networkx import MultiDiGraph
import texttable
from experiment.real.four_area.helper.MetaPathHelper import getMetaPathAdjacencyData
from experiment.real.four_area.helper.PathSimHelper import getNeighborSimScore, findMostSimilarNodes

__author__ = 'jontedesco'


def imbalancedCitationsPublicationsExample():
    """
      Illustrative example of imbalanced citations / publications to verify ShapeSim is working correctly
    """

    graph = MultiDiGraph()
    authors = ['Alice', 'Bob', 'Carol', 'Dave', 'Ed', 'Frank']
    conference = 'KDD'

    # Citation & publication count configuration
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

    # Helper for getting the next id
    def __getNextId():
        global nextId
        oldId = nextId
        nextId += 1
        return oldId

    def addPublicationPaper(author):
        """
          Helper method to add a 'publication' paper, connected to both an author and a conference
        """
        paper = "%s's Paper %d" % (author, (__getNextId()))
        graph.add_node(paper)
        graph.add_edges_from([(author, paper), (paper, author), (paper, conference), (conference, paper)])

        citationCount, publicationCount = actualCitationsPublications[author]
        actualCitationsPublications[author] = (citationCount, publicationCount + 1)

        return paper

    def addCitationPaper(citedPaper, citedAuthor):
        """
          Helper method to add a 'citation' paper, which is only connected to the conference and the paper it cites
        """
        citingPaper = "Citing Paper %d" % __getNextId()
        graph.add_node(citingPaper)
        graph.add_edges_from([(conference, citingPaper), (citingPaper, conference), (citingPaper, citedPaper)])

        citationCount, publicationCount = actualCitationsPublications[citedAuthor]
        actualCitationsPublications[citedAuthor] = (citationCount + 1, publicationCount)

        return citingPaper

    allPapers = []

    # Construct the graph
    graph.add_nodes_from(authors + [conference])
    for authorName in citationsPublications:
        citationCount, publicationCount = citationsPublications[authorName]

        # Add citations & publications to author
        authorPapers = addPapersToAuthor(publicationCount, authorName)
        allPapers.extend(authorPapers)
        citationsPerPaper = citationCount / publicationCount
        for paper in authorPapers:
            citingPapers = addCitationsToPaper(citationsPerPaper, paper, authorName)
            allPapers.extend(citingPapers)

    # Test PathSim / NeighborSim
    nodeIndex = {
        'paper': {i: allPapers[i] for i in xrange(0, len(allPapers))},
        'conference': {0: 'KDD'},
        'author': {0: 'Alice', 1: 'Bob', 2: 'Carol', 3: 'Dave', 4: 'Ed', 5: 'Frank'}
    }
    cpaAdjMatrix, extraData = getMetaPathAdjacencyData(graph, nodeIndex, ['conference', 'paper', 'author'])
    extraData['fromNodes'] = extraData['toNodes']
    extraData['fromNodesIndex'] = extraData['toNodesIndex']
    neighborSimMostSimilar, similarityScores = findMostSimilarNodes(
        cpaAdjMatrix, 'Alice', extraData, method=getNeighborSimScore
    )

    # TODO: Test ShapeSim on this example

    # Output similarity scores
    for name, mostSimilar in [('NeighborSim', neighborSimMostSimilar)]:
        print('\n%s Most Similar to "%s":' % (name, 'Alice'))
        mostSimilarTable = texttable.Texttable()
        rows = [['Author', 'Score']]
        rows += [[name, score] for name, score in mostSimilar]
        mostSimilarTable.add_rows(rows)
        print(mostSimilarTable.draw())

nextId = 1

if __name__ == '__main__':
    imbalancedCitationsPublicationsExample()