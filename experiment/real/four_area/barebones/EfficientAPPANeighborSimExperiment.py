import texttable
from experiment.Experiment import Experiment
from experiment.real.four_area.barebones.BareBonesHelper import parseFourAreaDataset, getMetaPathAdjacencyData, findMostSimilarNodes, getNeighborSimScore

__author__ = 'jontedesco'

class EfficientAPPANeighborSimExperiment(Experiment):
    """
      Runs some experiments with NeighborSim on author similarity for the 'four area' dataset
    """

    def runFor(self, author):

        # Parse 4-area dataset graph
        graph, nodeIndex = parseFourAreaDataset()

        # Compute APPA adjacency matrix
        appaAdjMatrix, extraData = getMetaPathAdjacencyData(graph, nodeIndex, ['author', 'paper', 'paper', 'author'])

        print(max([max(appaAdjMatrix[i]) for i in xrange(0, len(appaAdjMatrix))]))

        # Find the top 10 most similar nodes to some given node
        mostSimilar = findMostSimilarNodes(appaAdjMatrix, author, extraData, method = getNeighborSimScore)
        self.output('Most Similar to "%s":' % author)
        mostSimilarTable = texttable.Texttable()
        rows = [['Author', 'Score']]
        rows += [[name, score] for name, score in mostSimilar]
        mostSimilarTable.add_rows(rows)
        self.output(mostSimilarTable.draw())


if __name__ == '__main__':
    experiment = EfficientAPPANeighborSimExperiment(
        None, 'Most Similar APPA NeighborSim Authors', outputFilePath='experiment/real/four_area/barebones/results/appaNeighborSim')
    experiment.runFor('Christos Faloutsos')
    experiment.runFor('Jiawei Han')
    experiment.runFor('Sergey Brin')
    experiment.runFor('Sanjay Ghemawat')
