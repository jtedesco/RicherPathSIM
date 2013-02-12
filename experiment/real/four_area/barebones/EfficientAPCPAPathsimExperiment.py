import numpy
import texttable
from experiment.real.four_area.barebones.BareBonesHelper import parseFourAreaDataset, getMetaPathAdjacencyData, findMostSimilarNodesPathSim

__author__ = 'jontedesco'

class EfficientAPCPAPathSimExperiment():
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
        mostSimilar = findMostSimilarNodesPathSim(apcpaAdjMatrix, author, extraData)
        print('Most Similar to "%s":' % author)
        mostSimilarTable = texttable.Texttable()
        rows = [['Author', 'Score']]
        rows += [[name, score] for name, score in mostSimilar]
        mostSimilarTable.add_rows(rows)
        print(mostSimilarTable.draw())


if __name__ == '__main__':
    experiment = EfficientAPCPAPathSimExperiment()
    experiment.runFor('Christos Faloutsos')
