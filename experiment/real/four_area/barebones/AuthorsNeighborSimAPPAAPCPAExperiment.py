import cPickle
from collections import defaultdict
import os
import operator
from scipy.sparse import lil_matrix
import texttable
from experiment.Experiment import Experiment
from experiment.real.four_area.barebones.Helper import getMetaPathAdjacencyData, findMostSimilarNodes, getNeighborSimScore, testAuthors

__author__ = 'jontedesco'

class AuthorsNeighborSimAPPAAPCPAExperiment(Experiment):
    """
      Runs some experiments with NeighborSim on author similarity for the 'four area' dataset
    """

    def runFor(self, author, adjMatrix1, adjMatrix2, extraData1, extraData2, citationCounts = None):
        print("Running for %s..." % author)

        # Find most similar along two paths & weight evenly together
        mostSimilar, similarityScores1 = findMostSimilarNodes(adjMatrix1, author, extraData1, method = getNeighborSimScore)
        mostSimilar, similarityScores2 = findMostSimilarNodes(adjMatrix2, author, extraData2, method = getNeighborSimScore)

        # Weight the similarity scores together
        finalSimilarityScores = defaultdict(int)
        allAuthors = set(similarityScores1.keys()).union(set(similarityScores2.keys()))
        for otherAuthor in allAuthors:
            score1 = similarityScores1[otherAuthor] if otherAuthor in similarityScores1 else 0
            score2 = similarityScores2[otherAuthor] if otherAuthor in similarityScores2 else 0
            finalSimilarityScores[otherAuthor] = (float(score1) + float(score2)) / 2.0
        k = 10
        finalSimilarNodes = sorted(finalSimilarityScores.iteritems(), key=operator.itemgetter(1))
        finalSimilarNodes.reverse()
        number = min([k, len(finalSimilarNodes)])
        finalSimilarNodes = finalSimilarNodes[:number]

        self.output('Most Similar to "%s":' % author)
        mostSimilarTable = texttable.Texttable()
        if citationCounts is None:
            rows = [['Author', 'Score']]
            rows += [[name, score] for name, score in finalSimilarNodes]
        else:
            rows = [['Author', 'Score', 'Citations']]
            rows += [[name, score, citationCounts[name]] for name, score in finalSimilarNodes]
        mostSimilarTable.add_rows(rows)
        self.output(mostSimilarTable.draw())


def run(citationCounts = None):
    experiment = AuthorsNeighborSimAPPAAPCPAExperiment(
        None, 'Most Similar APPA-APCPA NeighborSim Authors', outputFilePath='results/appa-apcpaNeighborSim')

    graph, nodeIndex = cPickle.load(open(os.path.join('data', 'graphWithCitations')))

    # APPA path data
    appaAdjMatrix, extraData1 = getMetaPathAdjacencyData(graph, nodeIndex, ['author', 'paper', 'paper', 'author'])

    # APCPA path data
    apcAdjMatrix, extraData2 = getMetaPathAdjacencyData(graph, nodeIndex, ['author', 'paper', 'conference'], rows=True)
    cpaAdjMatrix, data = getMetaPathAdjacencyData(graph, nodeIndex, ['conference', 'paper', 'author'])
    apcpaAdjMatrix = lil_matrix(apcAdjMatrix * cpaAdjMatrix)
    extraData2['toNodes'] = data['toNodes']
    extraData2['toNodesIndex'] = data['toNodesIndex']

    for testAuthor in testAuthors:
        experiment.runFor(testAuthor, appaAdjMatrix, apcpaAdjMatrix, extraData1, extraData2, citationCounts=citationCounts)

if __name__ == '__main__': run()