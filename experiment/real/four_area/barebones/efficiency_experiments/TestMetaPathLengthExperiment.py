import cPickle
import os
import sys
import timeit
from collections import defaultdict

import texttable

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


def getPartialMetaPath(graph, metaPathPart, nodeIndex, repetitions):
    adjMatrix, extraData = getMetaPathAdjacencyData(graph, nodeIndex, metaPathPart)
    if metaPathPart[0] == metaPathPart[-1]:
        adjMatrices = [adjMatrix] * repetitions
    else:
        otherAdjMatrix, extraData = getMetaPathAdjacencyData(graph, nodeIndex, list(reversed(metaPathPart)))
        adjMatrices = [adjMatrix, otherAdjMatrix]
    return adjMatrices, adjMatrix


def getFullData(graph, nodeIndex, metaPath):
    return getMetaPathAdjacencyData(graph, nodeIndex, metaPath)


def multiplyFullAdjMatrix(adjMatrices, repetitions):
    fullAdjMatrix = adjMatrices[0]
    for i in xrange(1, repetitions):
        fullAdjMatrix = fullAdjMatrix * adjMatrices[i]


def run():

    # Experiments to run with meta path lengths (map of length to trial paths)
    p, a, t, c = 'paper', 'author', 'term', 'conference'
    metaPathLengthExperiments = {
        3: [
            [a, p, a],
        ],
        4: [
            [a, p, p, a]
        ],
        5: [
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

            # Time getting adjacency matrix directly
            fullTime = timeit.timeit('getFullData(graph, nodeIndex, metaPath)', number=10)

            # Split meta path
            if pathLength in {3, 5}:
                metaPathPart = [p, a, p] if metaPath[0] == p else [a, p, a]
                repetitions = ((len(metaPath) - 1) / 2)
            else: # 4, 7 -- only repeat twice
                metaPathPart = metaPath[:(len(metaPath)/2 + 1)]
                print metaPathPart
                repetitions = 2

            # Find the partial meta path adjacency list
            adjMatrices, adjMatrix = getPartialMetaPath(graph, metaPathPart, nodeIndex, repetitions)
            partialTime = timeit.timeit('getPartialMetaPath(graph, metaPathPart, nodeIndex, repetitions)', number=10)

            # Get the number of bytes to store partial adj matrices
            bytesForMatrices = sys.getsizeof(adjMatrix)

            # Multiply for full adj matrix
            multiplyTime = timeit.timeit('multiplyFullAdjMatrix(adjMatrices, repetitions)', number=10)

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
