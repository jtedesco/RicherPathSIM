import cPickle
import os
import sys
import timeit
from collections import defaultdict

from experiment.real.four_area.helper.MetaPathHelper import getMetaPathAdjacencyData, getMetaPathAdjacencyTensorData
from experiment.real.four_area.helper.SparseArray import SparseArray


__author__ = 'jontedesco'


def getPartialMetaPath(graph, metaPathPart, nodeIndex, repetitions):
    adjTensor, extraData = getMetaPathAdjacencyTensorData(graph, nodeIndex, metaPathPart)
    if metaPathPart[0] == metaPathPart[-1]:
        adjTensors = [adjTensor] * repetitions
    else:
        otherAdjTensor, extraData = getMetaPathAdjacencyTensorData(graph, nodeIndex, list(reversed(metaPathPart)))
        adjTensors = [adjTensor, otherAdjTensor]
    return adjTensors, adjTensor


def multiplyFullAdjTensor(adjTensors, repetitions):
    fullAdjTensor = adjTensors[0]
    for i in xrange(1, repetitions):
        fullAdjTensor = multiplyAdjTensors(fullAdjTensor, adjTensors[i])
    return fullAdjTensor


def multiplyAdjTensors(tensor1, tensor2):
    assert tensor1.shape[1] == tensor2.shape[0]

    # For (a x b x c) and (d x e x f), should be new size of (a x d x (c + f))
    newTensor = SparseArray((tensor1.shape[0], tensor2.shape[1], (tensor1.shape[2] + tensor2.shape[2])))

    for newRow in xrange(tensor1.shape[0]):
        for newCol in xrange(tensor2.shape[1]):
            for i in xrange(tensor1.shape[1]):

                # Skip if this entry is not a shared neighbor along the path
                isSharedNeighbor = tensor1[newRow, i, 0] > 0 and tensor2[i, newCol, 0] > 0
                if not isSharedNeighbor:
                    continue

                # Otherwise, add up the vectors for both
                for j in xrange(tensor1.shape[2]):
                    newTensor[newRow, newCol, j] += tensor1[newRow, i, j]
                for j in xrange(tensor2.shape[2]):
                    newTensor[newRow, newCol, (j + tensor1.shape[2])] += tensor2[i, newCol, j]

    return newTensor


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
    # without and with saving adj tensor
    metaPathLengthExperimentResults = defaultdict(list)

    for pathLength in sorted(metaPathLengthExperiments.keys()):
        for metaPath in metaPathLengthExperiments[pathLength]:

            # Time getting adjacency tensor directly
            # fullTime = timeit.timeit(lambda: getMetaPathAdjacencyTensorData(graph, nodeIndex, metaPath), number=10)

            # Split meta path
            if pathLength in {3, 5}:
                metaPathPart = [p, a, p] if metaPath[0] == p else [a, p, a]
                repetitions = ((len(metaPath) - 1) / 2)
            else:  # 4, 7 -- only repeat twice
                metaPathPart = metaPath[:(len(metaPath)/2 + 1)]
                print metaPathPart
                repetitions = 2

            # TODO: Change number back to 10

            # Find the partial meta path adjacency list
            adjTensors, adjTensor = getPartialMetaPath(graph, metaPathPart, nodeIndex, repetitions)
            partialTime = timeit.timeit(
                lambda: getPartialMetaPath(graph, metaPathPart, nodeIndex, repetitions),
                number=1
            )

            # Get the number of bytes to store partial adj tensor
            bytesForTensor = sys.getsizeof(adjTensor, None)

            # Multiply for full adj tensor
            multiplyTime = timeit.timeit(lambda: multiplyFullAdjTensor(adjTensors, repetitions), number=1)

            print "About to test equality"
            directFullTensor, extraData = getMetaPathAdjacencyTensorData(graph, nodeIndex, metaPath)
            multipliedFullTensor = multiplyFullAdjTensor(adjTensors, repetitions)
            print adjTensors[0] == directFullTensor
            print "meta path: %s, meta path part: %s, len of adj tensors: %s, repetitions: %d" % (
                metaPath, metaPathPart, len(adjTensors), repetitions
            )
            print directFullTensor == multipliedFullTensor

            # Output results
            # metaPathLengthExperimentResults[pathLength].append((
            #     fullTime, partialTime, multiplyTime, bytesForTensor
            # ))
            # print "Full Path: %.3f seconds, Partial Paths: %.3f seconds, Multiplication Only: %.3f, Bytes: %d  [%s]" % (
            #     fullTime, partialTime, multiplyTime, bytesForTensor, ', '.join(metaPath)
            # )

    cPickle.dump(metaPathLengthExperimentResults, open('results', 'w'))

if __name__ == '__main__':
    run()
