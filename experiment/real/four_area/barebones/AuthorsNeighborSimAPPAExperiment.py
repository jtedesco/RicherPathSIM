import cPickle
import os
import operator
import texttable
from experiment.Experiment import Experiment
from experiment.real.four_area.barebones.Helper import getMetaPathAdjacencyData, findMostSimilarNodes, getNeighborSimScore, testAuthors

__author__ = 'jontedesco'

class AuthorsNeighborSimAPPAExperiment(Experiment):
    """
      Runs some experiments with NeighborSim on author similarity for the 'four area' dataset
    """

    def runFor(self, author, adjMatrix, extraData, citationCounts = None):
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
        outputPath = os.path.join('results', 'authors', 'intermediate', '%s-neighborsim-appa' % author.replace(' ', ''))
        cPickle.dump(similarityScores, open(outputPath, 'wb'))


def run():
    experiment = AuthorsNeighborSimAPPAExperiment(
        None,
        'Most Similar APPA NeighborSim Authors',
        outputFilePath = os.path.join('results', 'authors', 'appaNeighborSim')
    )

    # Compute once, since these never change
    graph, nodeIndex = cPickle.load(open(os.path.join('data', 'graphWithCitations')))
    appaAdjMatrix, extraData = getMetaPathAdjacencyData(graph, nodeIndex, ['author', 'paper', 'paper', 'author'])

    # Compute author citation counts
    citationCounts = {}
    for author in extraData['toNodes']:
        i = extraData['toNodesIndex'][author]
        citationCounts[author] = sum(appaAdjMatrix.getcol(i).data)
    citationCountsList = sorted(citationCounts.iteritems(), key=operator.itemgetter(1))
    citationCountsList.reverse()

    # Output author citation counts
    with open(os.path.join('data', 'authorCitationCounts'), 'w') as file:
        map(lambda (author, count): file.write('%d: %s\n' % (int(count), author)), citationCountsList)

    for testAuthor in testAuthors:
        experiment.runFor(testAuthor, appaAdjMatrix, extraData, citationCounts)

    return citationCounts

if __name__ == '__main__': run()