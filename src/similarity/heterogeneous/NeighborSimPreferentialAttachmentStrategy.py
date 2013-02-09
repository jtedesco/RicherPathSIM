__author__ = 'jontedesco'

from src.similarity.heterogeneous.NeighborSimPropagationStrategy import NeighborSimPropagationStrategy

__author__ = 'jontedesco'

class NeighborSimPreferentialAttachmentStrategy(NeighborSimPropagationStrategy):
    """
      Class that computes NeighborSim propagation scores, using a constant factor scaling each propagation step
    """

    def findSimilarityScore(self, source, destination):

        # Build adjacency matrix for this projected graph
        adjMatrix, nodesIndex = self.metaPathUtility.getAdjacencyMatrixFromGraph(self.graph, self.metaPath, project=True)
        if self.reversed: adjMatrix = adjMatrix.transpose()

        self.similarityScore = self._getScoreFromProjection(source, destination, adjMatrix, nodesIndex)

        # Expand meta paths for all additional iterations
        for i in xrange(1, self.iterations):
            adjMatrix = adjMatrix * adjMatrix # TODO: Correct this
            self.similarityScore += (self.factor ** i) * self.similarityScore * self._getScoreFromProjection(source, destination, adjMatrix, nodesIndex)

        return self.similarityScore

