import cPickle
import os
import texttable
from experiment.Experiment import Experiment
from experiment.real.four_area.barebones.Helper import getMetaPathAdjacencyData, findMostSimilarNodes, getNeighborSimScore, testAuthors

__author__ = 'jontedesco'

class AuthorsNeighborSimPPAExperiment(Experiment):
    """
      Runs some experiments with NeighborSim on author similarity for the 'four area' dataset
    """

    def runFor(self, author, adjMatrix, extraData, citationCounts):
        print("Running for %s..." % author)

        # Find the top 10 most similar nodes to some given node
        mostSimilar, similarityScores = findMostSimilarNodes(adjMatrix, author, extraData, method = getNeighborSimScore)
        self.output('Most Similar to "%s":' % author)
        mostSimilarTable = texttable.Texttable()
        if citationCounts is None:
            rows = [['Author', 'Score']]
            rows += [[name, score] for name, score in mostSimilar]
        else:
            rows = [['Author', 'Score', 'Citations']]
            rows += [[name, score, citationCounts[name]] for name, score in mostSimilar]
        mostSimilarTable.add_rows(rows)
        self.output(mostSimilarTable.draw())

        # Output all similarity scores
        outputPath = os.path.join('results', 'authors', 'intermediate', '%s-neighborsim-ppa' % author.replace(' ', ''))
        cPickle.dump(similarityScores, open(outputPath, 'wb'))

def run(citationCounts = None):
    experiment = AuthorsNeighborSimPPAExperiment(
        None,
        'Most Similar PPA NeighborSim Authors',
        outputFilePath = os.path.join('results','authors','ppaNeighborSim')
    )

    # Compute once, since these never change
    graph, nodeIndex = cPickle.load(open(os.path.join('data', 'graphWithCitations')))
    ppaAdjMatrix, extraData = getMetaPathAdjacencyData(graph, nodeIndex, ['paper', 'paper', 'author'])

    for testAuthor in testAuthors:
        experiment.runFor(testAuthor, ppaAdjMatrix, extraData, citationCounts)

if __name__ == '__main__': run()