import cPickle
import operator
import texttable
from experiment.Experiment import Experiment
from experiment.real.four_area.barebones.Helper import   testAuthors

__author__ = 'jontedesco'

class AggregateAuthorsExperiment(Experiment):

    def runFor(self, queryNode, citationCounts, publicationCounts, partialResultsPaths):
        print("Running for %s..." % queryNode)

        # Combine the partial results with the given weights
        firstSimilarityScores, firstWeight = cPickle.load(open(partialResultsPaths[0][0])), partialResultsPaths[0][1]
        similarityScores = {node: firstWeight * firstSimilarityScores[node] for node in firstSimilarityScores}
        for i in xrange(1, len(partialResultsPaths)):
            partialResultsPath, weight = partialResultsPaths[i]
            scores = cPickle.load(open(partialResultsPath))
            for node in similarityScores:
                similarityScores[node] += weight * scores[node]

        # Get the most similar nodes
        k = 10
        mostSimilar = sorted(similarityScores.iteritems(), key=operator.itemgetter(1))
        mostSimilar.reverse()
        number = min([k, len(mostSimilar)])
        mostSimilar = mostSimilar[:number]

        # Output most similar nodes
        self.output('\nMost Similar to "%s":' % queryNode)
        mostSimilarTable = texttable.Texttable()
        rows = [['Author', 'Score', 'Citations', 'Publications']]
        rows += [[name, score, citationCounts[name], publicationCounts[name]] for name, score in mostSimilar]
        mostSimilarTable.add_rows(rows)
        self.output(mostSimilarTable.draw())


def run(title, outputPath, citationCounts, publicationCounts, weights = (0.5, 0.5)):
    experiment = AggregateAuthorsExperiment(None, title, outputPath)
    for testAuthor in testAuthors:
        experiment.runFor(testAuthor, citationCounts, publicationCounts, weights)