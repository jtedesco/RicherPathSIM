from src.similarity.MetaPathSimilarityStrategy import MetaPathSimilarityStrategy

__author__ = 'jontedesco'

class NeighborSimPropagationStrategy(MetaPathSimilarityStrategy):
    """
      Class that computes NeighborSim propagation-based scores (abstractly)
    """

    def __init__(self, graph, metaPath = None, symmetric = False, reversed = False, smoothed = False, factor = 0.5, iterations = 10):
        super(NeighborSimPropagationStrategy, self).__init__(graph, metaPath, symmetric)
        self.reversed = reversed
        self.smoothed = smoothed
        self.factor = factor
        self.iterations = iterations


    def _getScoreFromProjection(self, x, y, adjacencyMatrix, nodesIndex):

        xI, yI = nodesIndex[x], nodesIndex[y]

        # Find the shared in-neighbors of these nodes in the projected graph
        xInNeighborIndices = set()
        yInNeighborIndices = set()
        for citingAuthorIndex in xrange(0, len(adjacencyMatrix)):
            if adjacencyMatrix[citingAuthorIndex][xI] != 0: xInNeighborIndices.add(citingAuthorIndex)
            if adjacencyMatrix[citingAuthorIndex][yI] != 0: yInNeighborIndices.add(citingAuthorIndex)
        sharedInNeighborIndices = xInNeighborIndices.intersection(yInNeighborIndices)

        # Calculate numerator
        total = 1 if self.smoothed else 0
        for sharedNIndex in sharedInNeighborIndices:
            total += (adjacencyMatrix[sharedNIndex][xI] * adjacencyMatrix[sharedNIndex][yI])

        # Accumulate normalizations
        sourceNormalization = 1 if self.smoothed else 0
        for sourceNeighborIndex in xInNeighborIndices:
            sourceNormalization += adjacencyMatrix[sourceNeighborIndex][xI] ** 2
        destNormalization = 1 if self.smoothed else 0
        for destNeighborIndex in yInNeighborIndices:
            destNormalization += adjacencyMatrix[destNeighborIndex][yI] ** 2

        similarityScore = total
        if total > 0:
            similarityScore = 2 * total / float(sourceNormalization + destNormalization)

        return similarityScore


    def findSimilarityScore(self, source, destination):
        """
          Find the similarity score between two nodes
        """

        raise NotImplementedError()