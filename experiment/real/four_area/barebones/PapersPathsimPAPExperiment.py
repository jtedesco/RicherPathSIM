import cPickle
import os
from scipy.sparse import lil_matrix
import texttable
from experiment.Experiment import Experiment
from experiment.real.four_area.barebones.Helper import  getMetaPathAdjacencyData, findMostSimilarNodes

__author__ = 'jontedesco'

class PapersPathSimPAPExperiment(Experiment):
    """
      Runs some experiments with PathSim on paper similarity for the 'four area' dataset
    """

    def runFor(self, author, adjMatrix, extraData):

        # Find the top 10 most similar nodes to some given node
        mostSimilar, similarityScores = findMostSimilarNodes(adjMatrix, author, extraData)
        self.output('\nMost Similar to "%s":' % author)
        mostSimilarTable = texttable.Texttable()
        rows = [['Paper', 'Score']]
        rows += [[name, score] for name, score in mostSimilar]
        mostSimilarTable.add_rows(rows)
        self.output(mostSimilarTable.draw())

if __name__ == '__main__':
    experiment = PapersPathSimPAPExperiment(
        None, 'Most Similar PAP PathSim Papers', outputFilePath='results/papPathSim')

    # Compute once, since these never change
    graph, nodeIndex = cPickle.load(open(os.path.join('data', 'graphWithHalfCitations')))

    # Compute APCPA adjacency matrix
    paAdjMatrix, extraData = getMetaPathAdjacencyData(graph, nodeIndex, ['paper', 'author'], rows=True)
    apAdjMatrix, data = getMetaPathAdjacencyData(graph, nodeIndex, ['author', 'paper'])
    papAdjMatrix = lil_matrix(paAdjMatrix * apAdjMatrix)

    # Correct the toNodes content in extraData
    extraData['toNodes'] = data['fromNodes']
    extraData['toNodesIndex'] = data['fromNodesIndex']

    # Very highly cited papers
    experiment.runFor('Mining Association Rules between Sets of Items in Large Databases.', papAdjMatrix, extraData) # 9000 citations
    experiment.runFor('R-Trees: A Dynamic Index Structure for Spatial Searching.', papAdjMatrix, extraData) # ~5000 citations

    # Medium papers
    experiment.runFor('Efficient Reasoning in Qualitative Probabilistic Networks.', papAdjMatrix, extraData) # ~120 citations

    # Medium-small papers (~50 citations)
    experiment.runFor('Self-Tuning Database Systems: A Decade of Progress.', papAdjMatrix, extraData)
    experiment.runFor('R-trees with Update Memos.', papAdjMatrix, extraData)
