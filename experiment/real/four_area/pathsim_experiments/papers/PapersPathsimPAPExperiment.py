import cPickle
import os
from scipy.sparse import lil_matrix
import texttable
from experiment.Experiment import Experiment
from experiment.real.four_area.helper.Helper import  getMetaPathAdjacencyData, findMostSimilarNodes, testPapers

__author__ = 'jontedesco'

class PapersPathSimPAPExperiment(Experiment):
    """
      Runs some experiments with PathSim on paper similarity for the 'four area' dataset
    """

    def runFor(self, paper, adjMatrix, extraData):
        print("Running for %s..." % paper)

        # Find the top 10 most similar nodes to some given node
        mostSimilar, similarityScores = findMostSimilarNodes(adjMatrix, paper, extraData)
        self.output('\nMost Similar to "%s":' % paper)
        mostSimilarTable = texttable.Texttable()
        rows = [['Paper', 'Score']]
        rows += [[name, score] for name, score in mostSimilar]
        mostSimilarTable.add_rows(rows)
        self.output(mostSimilarTable.draw())

def run():
    experiment = PapersPathSimPAPExperiment(
        None, 'Most Similar PAP PathSim Papers', outputFilePath='results/papers/papPathSim')

    # Compute once, since these never change
    graph, nodeIndex = cPickle.load(open(os.path.join('../../data', 'graphWithCitations')))

    # Compute APCPA adjacency matrix
    paAdjMatrix, extraData = getMetaPathAdjacencyData(graph, nodeIndex, ['paper', 'author'], rows=True)
    apAdjMatrix, data = getMetaPathAdjacencyData(graph, nodeIndex, ['author', 'paper'])
    papAdjMatrix = lil_matrix(paAdjMatrix * apAdjMatrix)

    # Correct the toNodes content in extraData
    extraData['toNodes'] = data['toNodes']
    extraData['toNodesIndex'] = data['toNodesIndex']

    for testPaper in testPapers:
        experiment.runFor(testPaper, papAdjMatrix, extraData)

if __name__ == '__main__': run()