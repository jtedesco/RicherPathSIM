import cPickle
from collections import defaultdict
from datetime import datetime
import os
from scipy.sparse import lil_matrix
import texttable
from experiment.real.four_area.barebones.Helper import getMetaPathAdjacencyData, findMostSimilarNodes, \
    getNeighborSimScore, testPapers

__author__ = 'jontedesco'


def runFor(author, adjMatrix, extraData):

    print "Running for %s..." % author
    mostSimilar, similarityScores = findMostSimilarNodes(adjMatrix, author, extraData, method=getNeighborSimScore)
    print 'Most Similar to "%s":' % author
    mostSimilarTable = texttable.Texttable()
    mostSimilarTable.add_rows([['Author', 'Score']] + [[name, score] for name, score in mostSimilar])
    print mostSimilarTable.draw()


def run():

    # Experiments to run with meta path lengths (map of length to trial paths)
    p, a, t, c = 'paper', 'author', 'term', 'conference'
    metaPathLengthExperiments = {
        3: [
            [p, a, p],
            [p, c, p],
            [p, t, p],
            [a, p, a],
            [c, p, c],
            [t, p, t],
        ],
        5: [
            [p, a, p, a, p],
            [p, c, p, c, p],
            [p, t, p, t, p],
            [a, p, a, p, a],
            [c, p, c, p, c],
            [t, p, t, p, t],
        ],
        7: [
            [p, a, p, a, p, a, p],
            [p, c, p, c, p, c, p],
            [p, t, p, t, p, t, p],
            [a, p, a, p, a, p, a],
            [c, p, c, p, c, p, c],
            [t, p, t, p, t, p, t],
        ],
        9: [
            [p, a, p, a, p, a, p, a, p],
            [p, c, p, c, p, c, p, c, p],
            [p, t, p, t, p, t, p, t, p],
            [a, p, a, p, a, p, a, p, a],
            [c, p, c, p, c, p, c, p, c],
            [t, p, t, p, t, p, t, p, t],
        ]
    }

    # Map of experiment length to experiment, which contains a tuple of average time
    # without and with saving adj matrix
    metaPathLengthExperimentResults = defaultdict(list)

    for pathLength in sorted(metaPathLengthExperiments.keys()):
        for metaPath in metaPathLengthExperiments[pathLength]:

            print "Running for [%s] ..." % ', '.join(metaPath)

            # Get adjacency matrix directly
            fullPathStartTime = datetime.now()
            graph, nodeIndex = cPickle.load(open(os.path.join('..', 'data', 'graphWithCitations')))
            adjMatrix, extraData = getMetaPathAdjacencyData(graph, nodeIndex, metaPath)
            fullPathEndTime = datetime.now()
            fullTime = fullPathEndTime - fullPathStartTime

            # Split meta path
            partialPathsStartTime = datetime.now()
            metaPath1, metaPath2 = metaPath[:(pathLength / 2) + 1], metaPath[(pathLength / 2):]
            adjMatrix1, extraData = getMetaPathAdjacencyData(graph, nodeIndex, metaPath1, rows=True)
            adjMatrix2, data = getMetaPathAdjacencyData(graph, nodeIndex, metaPath2)
            extraData['toNodes'] = data['toNodes']
            extraData['toNodesIndex'] = data['toNodesIndex']
            partialPathsEndTime = datetime.now()
            partialTime = partialPathsEndTime - partialPathsStartTime

            # Multiply for full adj matrix
            multiplyStartTime = datetime.now()
            fullAdjMatrix = lil_matrix(adjMatrix1 * adjMatrix2)
            multiplyEndTime = datetime.now()
            multiplyTime = multiplyEndTime - multiplyStartTime

            # Get seconds from time deltas
            secondsForFullPath = fullTime.seconds + (fullTime.microseconds / 1000000.0)
            secondsForPartial = partialTime.seconds + (partialTime.microseconds / 1000000.0)
            secondsForMultiplication = multiplyTime.seconds + (multiplyTime.microseconds / 1000000.0)

            # Output results
            metaPathLengthExperimentResults[pathLength].append((
                secondsForFullPath, secondsForPartial, secondsForMultiplication
            ))
            print "Full Path: %.3f seconds, Partial Paths: %.3f seconds, Multiplication Only: %.3f  [%s]" % (
                secondsForFullPath, secondsForPartial, secondsForMultiplication, ', '.join(metaPath)
            )

    cPickle.dump(metaPathLengthExperimentResults, open('results', 'w'))

if __name__ == '__main__': run()
