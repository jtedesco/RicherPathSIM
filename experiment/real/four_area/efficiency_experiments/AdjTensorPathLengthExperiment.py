import cPickle
import cProfile
import os
from collections import defaultdict

from experiment.real.four_area.helper.MetaPathHelper import getMetaPathAdjacencyTensorData
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
                isSharedNeighbor = (tensor1[newRow, i, 0] > 0) and (tensor2[i, newCol, 0] > 0)
                if not isSharedNeighbor:
                    continue

                # Otherwise, add up the vectors for both
                for j in xrange(tensor1.shape[2]):
                    nextEntry = tensor1[newRow, i, j]
                    if nextEntry > 0:
                        newTensor[newRow, newCol, j] += nextEntry
                for j in xrange(tensor2.shape[2]):
                    nextEntry = tensor2[i, newCol, j]
                    if nextEntry > 0:
                        newTensor[newRow, newCol, (j + tensor1.shape[2])] += nextEntry

    return newTensor


def run():

    # Experiments to run with meta path lengths (map of length to trial paths)
    p, a, t, c = 'paper', 'author', 'term', 'conference'
    metaPathLengthExperiments = {
        # 3: [
        #    [c, p, c],
        # ],
        5: [
           [c, p, c, p, c],
        ],
        # 7: [
        #    [c, p, c, p, c, p, c],
        # ],
        # 9: [
        #    [c, p, c, p, c, p, c, p, c],
        # ],
    }

    graph, nodeIndex = cPickle.load(open(os.path.join('..', 'data', 'graphWithCitations')))

    # Map of experiment length to experiment, which contains a tuple of average times
    metaPathLengthExperimentResults = defaultdict(list)

    trials = 1

    for pathLength in sorted(metaPathLengthExperiments.keys()):
        for metaPath in metaPathLengthExperiments[pathLength]:

            # Time getting adjacency tensor directly
            # fullTime = timeit.timeit(lambda: getMetaPathAdjacencyTensorData(graph, nodeIndex, metaPath), number=trials)
            # fullTime /= float(trials)

            metaPathPart = [c, p, c] if metaPath[0] == c else [a, p, a]
            repetitions = ((len(metaPath) - 1) / 2)

            # Find the partial meta path adjacency list
            adjTensors, adjTensor = getPartialMetaPath(graph, metaPathPart, nodeIndex, repetitions)
            # partialTime = timeit.timeit(
            #     lambda: getPartialMetaPath(graph, metaPathPart, nodeIndex, repetitions), number=trials
            # )
            # partialTime /= float(trials)

            # Multiply for full adj tensor
            # multiplyTime = timeit.timeit(lambda: multiplyFullAdjTensor(adjTensors, repetitions), number=trials)
            # multiplyTime /= float(trials)

            # print "Getting full tensor"
            directFullTensor, extraData = getMetaPathAdjacencyTensorData(graph, nodeIndex, metaPath)
            print "Multiplying partial tensor"
            profiler = cProfile.Profile()
            multipliedFullTensor = profiler.runcall(multiplyFullAdjTensor, adjTensors, repetitions)
            profiler.print_stats()
            equal = multipliedFullTensor == directFullTensor
            print equal
            if not equal:
                with open('directcomp', 'w') as f:
                    f.write(formatTensorString(directFullTensor))
                with open('multcomp', 'w') as f:
                    f.write(formatTensorString(multipliedFullTensor))
                with open('partialcomp', 'w') as f:
                    f.write(formatTensorString(adjTensor))

            # Output results
            # metaPathLengthExperimentResults[pathLength].append((fullTime, partialTime, multiplyTime))
            # print "Full Path: %.3f seconds, Partial Paths: %.3f seconds, Multiplication Only: %.3f, [%s]" % (
            #     fullTime, partialTime, multiplyTime, ', '.join(metaPath)
            # )

    cPickle.dump(metaPathLengthExperimentResults, open('results', 'w'))


def formatTensorString(tensor):

    tensorOutput = []
    for i in xrange(tensor.shape[0]):
        tensorRow = []
        for j in xrange(tensor.shape[1]):
            partialString = '(%s)' % (','.join([str(tensor[i, j, k]) for k in xrange(tensor.shape[2])]))
            partialString += ' ' * (20 - len(partialString))
            tensorRow.append(partialString)
        tensorOutput.append(' '.join(tensorRow))
    return '\n'.join(tensorOutput)


def runTest():
    """
      Run a simple multiplication example to check the correctness of tensor multiplication
    """

    inputTensor = SparseArray((4, 4, 2))
    inputTensor[0, 1, 0] = 10
    inputTensor[0, 1, 1] = 10
    inputTensor[1, 0, 0] = 10
    inputTensor[1, 0, 1] = 10
    inputTensor[1, 2, 0] = 5
    inputTensor[1, 2, 1] = 5
    inputTensor[2, 1, 0] = 5
    inputTensor[2, 1, 1] = 5
    inputTensor[3, 0, 0] = 100
    inputTensor[3, 0, 1] = 100
    inputTensor[0, 3, 0] = 100
    inputTensor[0, 3, 1] = 100

    print "Input:"
    print formatTensorString(inputTensor)
    print '\n'
    print formatTensorString(multiplyAdjTensors(inputTensor, inputTensor))

if __name__ == '__main__':
    run()
    # runTest()
