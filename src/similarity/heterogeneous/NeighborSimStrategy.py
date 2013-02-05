from src.similarity.MetaPathSimilarityStrategy import MetaPathSimilarityStrategy

__author__ = 'jontedesco'

class NeighborSimStrategy(MetaPathSimilarityStrategy):
    """
      Class that implements a meta-neighbor based similarity strategy, that counts half-paths, not necessarily connecting
      the two nodes, but connecting to shared neighbors.
    """

    def findSimilarityScore(self, source, destination):
        """
          Find the similarity score between two nodes
        """

        if self.getFromCache(source, destination) is not None:
            return self.getFromCache(source, destination)

        # Project graph
        if self.metaPath[0] == self.metaPath[-1]: # Homogeneous projection?
            projectedGraph = self.metaPathUtility.createHomogeneousProjection(
                self.graph, self.metaPath, symmetric=self.symmetric
            )
        else:
            projectedGraph = self.metaPathUtility.createHeterogeneousProjection(
                self.graph, self.metaPath, symmetric=self.symmetric
            )

        # Find the shared in-neighbors of these nodes in the projected graph, and calculate the numerator
        sharedInNeighbors = set(projectedGraph.getPredecessors(source)).intersection(projectedGraph.getPredecessors(destination))
        total = 0
        for sharedN in sharedInNeighbors:
            total += (projectedGraph.getNumberOfEdges(sharedN, source) * projectedGraph.getNumberOfEdges(sharedN, destination))

        # Accumulate normalizations
        sourceNormalization = 0
        for sourceNeighbor in projectedGraph.getPredecessors(source):
            sourceNormalization += projectedGraph.getNumberOfEdges(sourceNeighbor, source)**2
        destNormalization = 0
        for destNeighbor in projectedGraph.getPredecessors(destination):
            destNormalization += projectedGraph.getNumberOfEdges(destNeighbor, destination)**2

        similarityScore = total
        if total > 0:
            similarityScore = 2 * total / float(sourceNormalization + destNormalization)

        self.addToCache(source, destination, similarityScore)

        return similarityScore