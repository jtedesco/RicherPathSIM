import cPickle
import os
import texttable
from experiment.Experiment import Experiment
from experiment.real.four_area.helper.MetaPathHelper import findMostSimilarNodes, getMetaPathAdjacencyData, testAuthors
from experiment.real.four_area.helper.PathSimHelper import getNeighborSimScore

__author__ = 'jontedesco'


class AuthorsNeighborSimCPCPPAExperiment(Experiment):
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
        outputPath = os.path.join('../../results', 'authors', 'intermediate', '%s-neighborsim-cpcppa' % author.replace(' ', ''))
        cPickle.dump(similarityScores, open(outputPath, 'wb'))

def run(citationCounts, publicationCounts):
    experiment = AuthorsNeighborSimCPCPPAExperiment(
        None,
        'Most Similar CPCPPA NeighborSim Authors',
        outputFilePath = os.path.join('../../results','authors','cpcppaNeighborSim')
    )

    # Compute once, since these never change
    graph, nodeIndex = cPickle.load(open(os.path.join('../../data', 'graphWithCitations')))
    cpcAdjMatrix, extraData = getMetaPathAdjacencyData(graph, nodeIndex, ['conference', 'paper', 'conference'])
    cppaAdjMatrix, extraData = getMetaPathAdjacencyData(graph, nodeIndex, ['conference', 'paper', 'paper', 'author'])
    cpcppaAdjMatrix = cpcAdjMatrix * cppaAdjMatrix
    extraData['fromNodes'] = extraData['toNodes']
    extraData['fromNodesIndex'] = extraData['toNodesIndex']

    for testAuthor in testAuthors:
        experiment.runFor(testAuthor, cpcppaAdjMatrix, extraData, citationCounts, publicationCounts)
