import cPickle
import os
import texttable
from experiment.Experiment import Experiment
from experiment.real.four_area.barebones.Helper import  getMetaPathAdjacencyData, findMostSimilarNodes, getNeighborSimScore

__author__ = 'jontedesco'

class PapersNeighborSimAPPExperiment(Experiment):
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


if __name__ == '__main__':
    experiment = PapersNeighborSimAPPExperiment(
        None, 'Most Similar APP NeighborSim Authors', outputFilePath='results/appNeighborSim')

    # Compute once, since these never change
    graph, nodeIndex = cPickle.load(open(os.path.join('data', 'graphWithCitations')))
    appAdjMatrix, extraData = getMetaPathAdjacencyData(graph, nodeIndex, ['author', 'paper', 'paper'])
    extraData['fromNodes'] = extraData['toNodes']
    extraData['fromNodesIndex'] = extraData['toNodesIndex']

    # Very highly cited papers
    experiment.runFor('Mining Association Rules between Sets of Items in Large Databases.', appAdjMatrix, extraData) # 9000 citations
    experiment.runFor('R-Trees: A Dynamic Index Structure for Spatial Searching.', appAdjMatrix, extraData) # ~5000 citations

    # Medium papers
    experiment.runFor('Efficient Reasoning in Qualitative Probabilistic Networks.', appAdjMatrix, extraData) # ~120 citations

    # Medium-small papers (~50 citations)
    experiment.runFor('Self-Tuning Database Systems: A Decade of Progress.', appAdjMatrix, extraData)
    experiment.runFor('R-trees with Update Memos.', appAdjMatrix, extraData)
