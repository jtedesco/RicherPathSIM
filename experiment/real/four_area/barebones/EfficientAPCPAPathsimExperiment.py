import numpy
from experiment.real.four_area.barebones.BareBonesHelper import parseFourAreaDataset, getMetaPathAdjacencyData

__author__ = 'jontedesco'

class EfficientAPCPAPathSimExperiment():
    """
      Runs some experiments with PathSim on author similarity for the 'four area' dataset
    """

    def run(self):

        # Parse 4-area dataset graph
        graph, nodeIndex = parseFourAreaDataset()

        # Compute APCPA adjacency matrix
        apcAdjMatrix, p, n = getMetaPathAdjacencyData(graph, nodeIndex, ['author', 'paper', 'conference'])
        cpaAdjMatrix, p, n = getMetaPathAdjacencyData(graph, nodeIndex, ['conference', 'paper', 'author'])
        apcpaAdjMatrix = numpy.dot(apcAdjMatrix, cpaAdjMatrix)

if __name__ == '__main__':
    experiment = EfficientAPCPAPathSimExperiment()
    experiment.run()
