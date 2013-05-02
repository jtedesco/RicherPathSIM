import cPickle
import os
import texttable
from experiment.Experiment import Experiment
from experiment.real.four_area.helper.Helper import getMetaPathAdjacencyData, findMostSimilarNodes, testAuthors, getAbsNeighborSimScore

__author__ = 'jontedesco'

class AuthorsNeighborSimAbsPPAExperiment(Experiment):
    """
      Runs some experiments with NeighborSim on author similarity for the 'four area' dataset
    """

    def runFor(self, author, adjMatrix, extraData, citationCounts, publicationCounts):
        print("Running for %s..." % author)

        # Find the top 10 most similar nodes to some given node
        mostSimilar, similarityScores = findMostSimilarNodes(adjMatrix, author, extraData, method = getAbsNeighborSimScore)
        self.output('Most Similar to "%s":' % author)
        mostSimilarTable = texttable.Texttable()
        rows = [['Author', 'Score', 'Citations', 'Publications']]
        rows += [[name, score, citationCounts[name], publicationCounts[name]] for name, score in mostSimilar]
        mostSimilarTable.add_rows(rows)
        self.output(mostSimilarTable.draw())

        # Output all similarity scores
        outputPath = os.path.join('../../results', 'authors', 'intermediate', '%s-neighborsim-absppa' % author.replace(' ', ''))
        cPickle.dump(similarityScores, open(outputPath, 'wb'))

def run(citationCounts, publicationCounts):
    experiment = AuthorsNeighborSimAbsPPAExperiment(
        None,
        'Most Similar PPA NeighborSim (Absolute) Authors',
        outputFilePath = os.path.join('../../results','authors','absppaNeighborSim')
    )

    # Compute once, since these never change
    graph, nodeIndex = cPickle.load(open(os.path.join('../../data', 'graphWithCitations')))
    ppaAdjMatrix, extraData = getMetaPathAdjacencyData(graph, nodeIndex, ['term', 'paper', 'paper', 'author'])
    extraData['fromNodes'] = extraData['toNodes']
    extraData['fromNodesIndex'] = extraData['toNodesIndex']

    for testAuthor in testAuthors:
        experiment.runFor(testAuthor, ppaAdjMatrix, extraData, citationCounts, publicationCounts)
