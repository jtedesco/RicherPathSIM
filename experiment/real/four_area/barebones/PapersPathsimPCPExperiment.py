import cPickle
import os
from scipy.sparse import lil_matrix
import texttable
from experiment.Experiment import Experiment
from experiment.real.four_area.barebones.Helper import  getMetaPathAdjacencyData, findMostSimilarNodes

__author__ = 'jontedesco'

class PapersPathSimPCPExperiment(Experiment):
    """
      Runs some experiments with PathSim on author similarity for the 'four area' dataset
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

if __name__ == '__main__':
    experiment = PapersPathSimPCPExperiment(
        None, 'Most Similar PCP PathSim Papers', outputFilePath='results/pcpPathSim')

    # Compute once, since these never change
    graph, nodeIndex = cPickle.load(open(os.path.join('data', 'graphWithCitations')))

    # Compute APCPA adjacency matrix
    pcAdjMatrix, extraData = getMetaPathAdjacencyData(graph, nodeIndex, ['paper', 'conference'], rows=True)
    cpAdjMatrix, data = getMetaPathAdjacencyData(graph, nodeIndex, ['conference', 'paper'])
    pcpAdjMatrix = lil_matrix(pcAdjMatrix * cpAdjMatrix)

    # Correct the toNodes content in extraData
    extraData['toNodes'] = data['fromNodes']
    extraData['toNodesIndex'] = data['fromNodesIndex']

    # Very highly cited papers
    experiment.runFor('Mining Association Rules between Sets of Items in Large Databases.', pcpAdjMatrix, extraData) # 9000 citations
    experiment.runFor('R-Trees: A Dynamic Index Structure for Spatial Searching.', pcpAdjMatrix, extraData) # ~5000 citations

    # Medium papers
    experiment.runFor('Efficient Reasoning in Qualitative Probabilistic Networks.', pcpAdjMatrix, extraData) # ~120 citations

    # Medium-small papers (~50 citations)
    experiment.runFor('Self-Tuning Database Systems: A Decade of Progress.', pcpAdjMatrix, extraData)
    experiment.runFor('R-trees with Update Memos.', pcpAdjMatrix, extraData)
