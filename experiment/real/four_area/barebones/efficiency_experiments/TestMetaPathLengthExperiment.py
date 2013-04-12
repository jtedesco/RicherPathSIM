import cPickle
import os
import sys
import texttable
from datetime import datetime
from collections import defaultdict
from scipy.sparse import lil_matrix
from experiment.real.four_area.barebones.Helper import getMetaPathAdjacencyData, findMostSimilarNodes, \
    getNeighborSimScore

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
            [a, p, a],
        ],
        5: [
            [p, a, p, a, p],
            [a, p, a, p, a],
        ],
        7: [
            [p, a, p, a, p, a, p],
            [a, p, a, p, a, p, a],
        ],
        9: [
            [p, a, p, a, p, a, p, a, p],
            [a, p, a, p, a, p, a, p, a],
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
            metaPathPart = [p, a, p] if metaPath[0] == p else [a, p, a]
            repititions = (len(metaPath) - 1) / 2
            adjMatrices = []
            adjMatrix1, extraData = getMetaPathAdjacencyData(graph, nodeIndex, metaPathPart, rows=True)
            adjMatrices.append(adjMatrix1)
            for i in repititions:
                adjMatrices.append(adjMatrix1)
            partialPathsEndTime = datetime.now()
            partialTime = partialPathsEndTime - partialPathsStartTime

            # Get the number of bytes to store partial adj matrices
            bytesForMatrices = sys.getsizeof(adjMatrix)

            # Multiply for full adj matrix
            multiplyStartTime = datetime.now()
            fullAdjMatrix = adjMatrix
            for i in repititions:
                fullAdjMatrix = fullAdjMatrix * fullAdjMatrix
            fullAdjMatrix = lil_matrix(fullAdjMatrix)
            multiplyEndTime = datetime.now()
            multiplyTime = multiplyEndTime - multiplyStartTime

            # Get seconds from time deltas
            secondsForFullPath = fullTime.seconds + (fullTime.microseconds / 1000000.0)
            secondsForPartial = partialTime.seconds + (partialTime.microseconds / 1000000.0)
            secondsForMultiplication = multiplyTime.seconds + (multiplyTime.microseconds / 1000000.0)

            # Output results
            metaPathLengthExperimentResults[pathLength].append((
                secondsForFullPath, secondsForPartial, secondsForMultiplication, bytesForMatrices
            ))
            print "Full Path: %.3f seconds, Partial Paths: %.3f seconds, Multiplication Only: %.3f, Bytes: %d  [%s]" % (
                secondsForFullPath, secondsForPartial, secondsForMultiplication, bytesForMatrices, ', '.join(metaPath)
            )

    cPickle.dump(metaPathLengthExperimentResults, open('results', 'w'))

if __name__ == '__main__': run()