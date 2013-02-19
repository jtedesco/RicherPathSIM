import cPickle
import os
import operator
import texttable
from experiment.Experiment import Experiment
from experiment.real.four_area.barebones.Helper import   testAuthors

__author__ = 'jontedesco'

class AuthorsNeighborSimAPPAAPCPAExperiment(Experiment):
    """
      Runs some experiments with NeighborSim on author similarity for the 'four area' dataset
    """

    def runFor(self, author, citationCounts = None, weights = (0.5, 0.5)):
        print("Running for %s..." % author)

        # Read similarity scores for this author for both measures
        appaPath = os.path.join('results', 'authors', 'intermediate', '%s-neighborsim-appa' % author.replace(' ', ''))
        appaSimilarityScores = cPickle.load(open(appaPath))
        apcpaPath = os.path.join('results', 'authors', 'intermediate', '%s-pathsim-apcpa' % author.replace(' ', ''))
        apcpaSimilarityScores = cPickle.load(open(apcpaPath))

        # Combine similarity scores (NOTE: Assumes we only care about nodes in both similarity score dicts)
        similarityScores = {}
        for node in apcpaSimilarityScores:
            if node in appaSimilarityScores:
                similarityScores[node] =  weights[0] * appaSimilarityScores[node] + weights[1] * apcpaSimilarityScores[node]

        # Get the most similar nodes
        k = 10
        mostSimilar = sorted(similarityScores.iteritems(), key=operator.itemgetter(1))
        mostSimilar.reverse()
        number = min([k, len(mostSimilar)])
        mostSimilar = mostSimilar[:number]

        # Output most similar nodes
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


def run(citationCounts = None, weights = (0.5, 0.5)):
    experiment = AuthorsNeighborSimAPPAAPCPAExperiment(
        None,
        'Most Similar APPA-APCPA NeighborSim Authors',
        outputFilePath = os.path.join('results','authors','appa-apcpaNeighborSim-%1.1f-%1.1f' % weights)
    )

    for testAuthor in testAuthors:
        experiment.runFor(testAuthor, citationCounts = citationCounts, weights = weights)

if __name__ == '__main__': run()