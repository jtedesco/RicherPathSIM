import cPickle
from collections import defaultdict
import os
import operator
import texttable
from experiment.Experiment import Experiment
from experiment.real.four_area.barebones.Helper import getMetaPathAdjacencyData, findMostSimilarNodes, getNeighborSimScore, testAuthors

__author__ = 'jontedesco'

class AuthorsNeighborSimPPAExperiment(Experiment):
    """
      Runs some experiments with NeighborSim on author similarity for the 'four area' dataset
    """

    def runFor(self, author, adjMatrix, extraData, citationCounts, publicationCounts):
        print("Running for %s..." % author)

        # Find the top 10 most similar nodes to some given node
        mostSimilar, similarityScores = findMostSimilarNodes(adjMatrix, author, extraData, method = getNeighborSimScore)
        self.output('Most Similar to "%s":' % author)
        mostSimilarTable = texttable.Texttable()
        rows = [['Author', 'Score', 'Citations', 'Publications']]
        rows += [[name, score, citationCounts[name], publicationCounts[name]] for name, score in mostSimilar]
        mostSimilarTable.add_rows(rows)
        self.output(mostSimilarTable.draw())

        # Output all similarity scores
        outputPath = os.path.join('results', 'authors', 'intermediate', '%s-neighborsim-ppa' % author.replace(' ', ''))
        cPickle.dump(similarityScores, open(outputPath, 'wb'))

def run():
    experiment = AuthorsNeighborSimPPAExperiment(
        None,
        'Most Similar PPA NeighborSim Authors',
        outputFilePath = os.path.join('results','authors','ppaNeighborSim')
    )

    # Compute once, since these never change
    graph, nodeIndex = cPickle.load(open(os.path.join('data', 'graphWithCitations')))
    ppaAdjMatrix, extraData = getMetaPathAdjacencyData(graph, nodeIndex, ['paper', 'paper', 'author'])
    extraData['fromNodes'] = extraData['toNodes']
    extraData['fromNodesIndex'] = extraData['toNodesIndex']

    # Read paper citation counts
    paperCitationsFile = open(os.path.join('data', 'paperCitationCounts'))
    paperCitationCounts = {}
    for line in paperCitationsFile:
        count, title = line[:-1].split(': ')
        paperCitationCounts[title] = int(count)

    # Compute author publication counts
    allPapers = set(nodeIndex['paper'].values())
    allAuthors = set(nodeIndex['author'].values())
    publicationCounts, citationCounts = defaultdict(int), defaultdict(int)
    for author in allAuthors:
        for node in graph.successors(author):
            if node in allPapers:
                publicationCounts[author] += 1
                citationCounts[author] += paperCitationCounts[node]

    # Output author citation counts
    citationCountsList = sorted(citationCounts.iteritems(), key=operator.itemgetter(1))
    citationCountsList.reverse()
    with open(os.path.join('data', 'authorCitationCounts'), 'w') as file:
        map(lambda (author, count): file.write('%d: %s\n' % (int(count), author)), citationCountsList)


    for testAuthor in testAuthors:
        experiment.runFor(testAuthor, ppaAdjMatrix, extraData, citationCounts, publicationCounts)

    return publicationCounts, citationCounts