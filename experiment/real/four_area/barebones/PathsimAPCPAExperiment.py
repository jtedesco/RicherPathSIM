import cPickle
import os
from scipy.sparse import lil_matrix
import texttable
from experiment.Experiment import Experiment
from experiment.real.four_area.barebones.BareBonesHelper import  getMetaPathAdjacencyData, findMostSimilarNodes

__author__ = 'jontedesco'

class PathSimAPCPAExperiment(Experiment):
    """
      Runs some experiments with PathSim on author similarity for the 'four area' dataset
    """

    def runFor(self, author, adjMatrix, extraData):

        # Find the top 10 most similar nodes to some given node
        mostSimilar, similarityScores = findMostSimilarNodes(adjMatrix, author, extraData)
        self.output('\nMost Similar to "%s":' % author)
        mostSimilarTable = texttable.Texttable()
        rows = [['Author', 'Score']]
        rows += [[name, score] for name, score in mostSimilar]
        mostSimilarTable.add_rows(rows)
        self.output(mostSimilarTable.draw())

if __name__ == '__main__':
    experiment = PathSimAPCPAExperiment(
        None, 'Most Similar APCPA PathSim Authors', outputFilePath='results/apcpaPathSim')

    # Compute once, since these never change
    graph, nodeIndex = cPickle.load(open(os.path.join('data', 'graphWithHalfCitations')))

    # Compute APCPA adjacency matrix
    apcAdjMatrix, extraData = getMetaPathAdjacencyData(graph, nodeIndex, ['author', 'paper', 'conference'], rows=True)
    cpaAdjMatrix, data = getMetaPathAdjacencyData(graph, nodeIndex, ['conference', 'paper', 'author'])
    apcpaAdjMatrix = lil_matrix(apcAdjMatrix * cpaAdjMatrix)

    # Correct the toNodes content in extraData
    extraData['toNodes'] = data['toNodes']
    extraData['toNodesIndex'] = data['toNodesIndex']

    experiment.runFor('Christos Faloutsos', apcpaAdjMatrix, extraData)
    experiment.runFor('Jiawei Han', apcpaAdjMatrix, extraData)
    experiment.runFor('Sergey Brin', apcpaAdjMatrix, extraData)
    experiment.runFor('Sanjay Ghemawat', apcpaAdjMatrix, extraData)
