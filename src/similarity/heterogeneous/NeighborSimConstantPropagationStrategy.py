import numpy
from src.similarity.heterogeneous.NeighborSimPropagationStrategy import NeighborSimPropagationStrategy

__author__ = 'jontedesco'

class NeighborSimConstantPropagationStrategy(NeighborSimPropagationStrategy):
    """
      Class that computes NeighborSim propagation scores, using a constant factor scaling each propagation step
    """

    def findSimilarityScore(self, source, destination):

        # Build adjacency matrix for this projected graph
        adjMatrix, nodesIndex = self.metaPathUtility.getAdjacencyMatrixFromGraph(self.graph, self.metaPath, project=True)
        if self.reversed: adjMatrix = adjMatrix.transpose()

        self.similarityScore = self._getScoreFromProjection(source, destination, adjMatrix, nodesIndex)

        # Build the adjacency matrix for extending to further lengths
        if self.metaPath[0] == self.metaPath[-1]:
            extendAdjMatrix = adjMatrix
        else:
            extendMetaPath = self.metaPath + reversed(self.metaPath)[1:] + self.metaPath[1:]
            extendAdjMatrix, extendNodesIndex = self.metaPathUtility.getAdjacencyMatrixFromGraph(self.graph, extendMetaPath, project=True)

        # Expand meta paths for all additional iterations
        totalNormalization = 1.0
        for i in xrange(1, self.iterations):
            adjMatrix = numpy.dot(adjMatrix, extendAdjMatrix)
            normalization = (self.factor ** i)
            totalNormalization += normalization
            self.similarityScore += normalization * self._getScoreFromProjection(source, destination, adjMatrix, nodesIndex)

        return self.similarityScore / totalNormalization
