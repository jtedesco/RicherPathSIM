import cPickle
import os
import texttable
from experiment.Experiment import Experiment
from experiment.real.four_area.barebones.Helper import  getMetaPathAdjacencyData, findMostSimilarNodes, getNeighborSimScore, testPapers

__author__ = 'jontedesco'

class PapersNeighborSimCPPExperiment(Experiment):
    """
      Runs some experiments with NeighborSim on paper similarity for the 'four area' dataset
    """

    def runFor(self, paper, adjMatrix, extraData):
        print("Running for %s..." % paper)

        # Find the top 10 most similar nodes to some given node
        mostSimilar, similarityScores = findMostSimilarNodes(adjMatrix, paper, extraData, method = getNeighborSimScore)
        self.output('Most Similar to "%s":' % paper)
        mostSimilarTable = texttable.Texttable()
        rows = [['Paper', 'Score']]
        rows += [[name, score] for name, score in mostSimilar]
        mostSimilarTable.add_rows(rows)
        self.output(mostSimilarTable.draw())


def run():
    experiment = PapersNeighborSimCPPExperiment(
        None, 'Most Similar CPP NeighborSim Authors', outputFilePath='results/papers/cppNeighborSim')

    # Compute once, since these never change
    graph, nodeIndex = cPickle.load(open(os.path.join('data', 'graphWithCitations')))
    cppAdjMatrix, extraData = getMetaPathAdjacencyData(graph, nodeIndex, ['conference', 'paper', 'paper'])
    extraData['fromNodes'] = extraData['toNodes']
    extraData['fromNodesIndex'] = extraData['toNodesIndex']

    for testPaper in testPapers:
        experiment.runFor(testPaper, cppAdjMatrix, extraData)

if __name__ == '__main__': run()