import numpy
from src.similarity.heterogeneous.path_shape_count.PathShapeStrategy import PathShapeStrategy

__author__ = 'jontedesco'


class FlattenedMatrixStrategy(PathShapeStrategy):
    """
      Shape similarity strategy by flattening matrices for source and destination into two vectors
    """

    def getSimilarityScoreFromMatrices(self, sourceMatrix, destinationMatrix,
                                       normalizedSourceMatrix, normalizedDestinationMatrix):
        """
          Flatten the source and destination matrices into single vectors, and compare them
        """

        sourceVector = numpy.hstack(sourceMatrix)
        destinationVector = numpy.hstack(destinationMatrix)
        normalizedSourceVector = numpy.hstack(normalizedSourceMatrix)
        normalizedDestinationVector = numpy.hstack(normalizedDestinationMatrix)

        absSim = self.vectorSimilarity(self.graph, sourceVector, destinationVector)
        relSim = self.vectorSimilarity(self.graph, normalizedSourceVector, normalizedDestinationVector)

        return (self.weight * absSim) + ((1 - self.weight) * relSim)

