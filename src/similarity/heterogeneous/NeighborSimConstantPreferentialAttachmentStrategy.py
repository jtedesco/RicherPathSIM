import numpy

__author__ = 'jontedesco'

from src.similarity.heterogeneous.NeighborSimPropagationStrategy import NeighborSimPropagationStrategy

__author__ = 'jontedesco'

class NeighborSimConstantPreferentialAttachmentStrategy(NeighborSimPropagationStrategy):
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
        score = self.similarityScore
        for i in xrange(1, self.iterations):
            adjMatrix = numpy.dot(adjMatrix, extendAdjMatrix)
            lastScore = score
            score = self._getScoreFromProjection(source, destination, adjMatrix, nodesIndex)
            normalization = (self.factor ** i) * (lastScore if lastScore != 0 else 1)
            self.similarityScore += normalization * score

        return self.similarityScore

