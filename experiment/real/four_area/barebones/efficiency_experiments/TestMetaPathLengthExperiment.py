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
        4: [
            [a, p, p, a]
        ],
        5: [
            [p, a, p, a, p],
            [a, p, a, p, a],
        ],
        7: [
            [a, p, p, a, p, p, a]
        ],
    }

    graph, nodeIndex = cPickle.load(open(os.path.join('..', 'data', 'graphWithCitations')))

    # Map of experiment length to experiment, which contains a tuple of average time
    # without and with saving adj matrix
    metaPathLengthExperimentResults = defaultdict(list)

    for pathLength in sorted(metaPathLengthExperiments.keys()):
        for metaPath in metaPathLengthExperiments[pathLength]:

            print "Running for [%s] ..." % ', '.join(metaPath)

            # Get adjacency matrix directly
            print "Running with full path..."
            fullPathStartTime = datetime.now()
            adjMatrix, extraData = getMetaPathAdjacencyData(graph, nodeIndex, metaPath)
            fullPathEndTime = datetime.now()
            fullTime = fullPathEndTime - fullPathStartTime

            # Split meta path
            if pathLength in {3, 5}:
                metaPathPart = [p, a, p] if metaPath[0] == p else [a, p, a]
                repetitions = ((len(metaPath) - 1) / 2)
            else: # 4, 7 -- only repeat twice
                metaPathPart = metaPath[:(len(metaPath)/2 + 1)]
                repetitions = 2

            # Find the partial meta path adjacency list
            print "Finding partial path..."
            partialPathsStartTime = datetime.now()
            adjMatrix, extraData = getMetaPathAdjacencyData(graph, nodeIndex, metaPathPart)
            partialPathsEndTime = datetime.now()
            partialTime = partialPathsEndTime - partialPathsStartTime

            # Get the number of bytes to store partial adj matrices
            bytesForMatrices = sys.getsizeof(adjMatrix)

            # Multiply for full adj matrix
            print "Multiplying partial path for full adjacency..."
            multiplyStartTime = datetime.now()
            fullAdjMatrix = adjMatrix
            for i in xrange(0, repetitions):
                fullAdjMatrix = fullAdjMatrix * adjMatrix
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
