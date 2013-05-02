import numpy
from src.similarity.heterogeneous.path_shape_count.PathShapeStrategy import PathShapeStrategy

__author__ = 'jontedesco'


class VectorProductStrategy(PathShapeStrategy):
    """
      Shape similarity strategy by flattening matrices for source and destination into two vectors
    """

    def getSimilarityScoreFromMatrices(self, sourceMatrix, destinationMatrix, nSourceMatrix, nDestinationMatrix):
        """
          Flatten the source and destination matrices into single vectors, and compare them
        """

        rows, cols = sourceMatrix.shape
        absSim, relSim = 1, 1

        # Compute the absolute & relative similarity using the product of similarity along each step
        for col in xrange(0, cols):
            absSim *= self.vectorSimilarity(self.graph, sourceMatrix[:, col], destinationMatrix[:, col])
            relSim *= self.vectorSimilarity(self.graph, nSourceMatrix[:, col], nDestinationMatrix[:, col])

        return (self.weight * absSim) + ((1 - self.weight) * relSim)