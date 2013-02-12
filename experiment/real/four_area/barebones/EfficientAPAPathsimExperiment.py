import numpy
from experiment.real.four_area.barebones.BareBonesHelper import parseFourAreaDataset, getMetaPathAdjacencyData

__author__ = 'jontedesco'

class EfficientAPAPathSimExperiment():
    """
      Runs some experiments with PathSim on author similarity for the 'four area' dataset
    """

    def run(self):

        # Parse 4-area dataset graph
        graph, nodeIndex = parseFourAreaDataset()

        # Compute APA adjacency matrix
        apAdjMatrix, p, n = getMetaPathAdjacencyData(graph, nodeIndex, ['author', 'paper'])
        paAdjMatrix, p, n = getMetaPathAdjacencyData(graph, nodeIndex, ['paper', 'author'])
        apaAdjMatrix = numpy.dot(apAdjMatrix, paAdjMatrix)

if __name__ == '__main__':
    experiment = EfficientAPAPathSimExperiment()
    experiment.run()
