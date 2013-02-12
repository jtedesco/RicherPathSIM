import numpy
import texttable
from experiment.Experiment import Experiment
from experiment.real.four_area.barebones.BareBonesHelper import parseFourAreaDataset, getMetaPathAdjacencyData, findMostSimilarNodes

__author__ = 'jontedesco'

class EfficientAPCPAPathSimExperiment(Experiment):
    """
      Runs some experiments with PathSim on author similarity for the 'four area' dataset
    """

    def runFor(self, author):

        # Parse 4-area dataset graph
        graph, nodeIndex = parseFourAreaDataset()

        # Compute APCPA adjacency matrix
        apcAdjMatrix, extraData = getMetaPathAdjacencyData(graph, nodeIndex, ['author', 'paper', 'conference'])
        cpaAdjMatrix, data = getMetaPathAdjacencyData(graph, nodeIndex, ['conference', 'paper', 'author'])
        apcpaAdjMatrix = numpy.dot(apcAdjMatrix, cpaAdjMatrix)

        # Correct the toNodes content in extraData
        extraData['toNodes'] = data['toNodes']
        extraData['toNodesIndex'] = data['toNodesIndex']

        # Find the top 10 most similar nodes to some given node
        mostSimilar = findMostSimilarNodes(apcpaAdjMatrix, author, extraData)
        self.output('\nMost Similar to "%s":' % author)
        mostSimilarTable = texttable.Texttable()
        rows = [['Author', 'Score']]
        rows += [[name, score] for name, score in mostSimilar]
        mostSimilarTable.add_rows(rows)
        self.output(mostSimilarTable.draw())


if __name__ == '__main__':
    experiment = EfficientAPCPAPathSimExperiment(
        None, 'Most Similar APCPA PathSim Authors', outputFilePath='experiment/real/four_area/barebones/results/apcpaPathSim')
    experiment.runFor('Christos Faloutsos')
    experiment.runFor('Jiawei Han')
    experiment.runFor('Sergey Brin')
    experiment.runFor('Sanjay Ghemawat')
