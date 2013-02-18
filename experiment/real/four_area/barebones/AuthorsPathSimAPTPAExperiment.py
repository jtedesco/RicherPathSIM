import cPickle
import os
from scipy.sparse import lil_matrix
import texttable
from experiment.Experiment import Experiment
from experiment.real.four_area.barebones.Helper import  getMetaPathAdjacencyData, findMostSimilarNodes, testAuthors

__author__ = 'jontedesco'

class AuthorsPathSimAPTPAExperiment(Experiment):
    """
      Runs some experiments with PathSim on author similarity for the 'four area' dataset
    """

    def runFor(self, author, adjMatrix, extraData, citationCounts):
        print("Running for %s..." % author)

        # Find the top 10 most similar nodes to some given node
        mostSimilar, similarityScores = findMostSimilarNodes(adjMatrix, author, extraData)
        self.output('\nMost Similar to "%s":' % author)
        mostSimilarTable = texttable.Texttable()
        if citationCounts is None:
            rows = [['Author', 'Score']]
            rows += [[name, score] for name, score in mostSimilar]
        else:
            rows = [['Author', 'Score', 'Citations']]
            rows += [[name, score, citationCounts[name]] for name, score in mostSimilar]
        mostSimilarTable.add_rows(rows)
        self.output(mostSimilarTable.draw())

def run(citationCounts = None):
    experiment = AuthorsPathSimAPTPAExperiment(
        None, 'Most Similar APCPA PathSim Authors', outputFilePath='results/authors/aptpaPathSim')

    # Compute once, since these never change
    graph, nodeIndex = cPickle.load(open(os.path.join('data', 'graphWithCitations')))

    # Compute APCPA adjacency matrix
    aptAdjMatrix, extraData = getMetaPathAdjacencyData(graph, nodeIndex, ['author', 'paper', 'term'], rows=True)
    tpaAdjMatrix, data = getMetaPathAdjacencyData(graph, nodeIndex, ['term', 'paper', 'author'])
    aptpaAdjMatrix = lil_matrix(aptAdjMatrix * tpaAdjMatrix)

    # Correct the toNodes content in extraData
    extraData['toNodes'] = data['toNodes']
    extraData['toNodesIndex'] = data['toNodesIndex']

    for testAuthor in testAuthors:
        experiment.runFor(testAuthor, aptpaAdjMatrix, extraData, citationCounts)

if __name__ == '__main__': run()