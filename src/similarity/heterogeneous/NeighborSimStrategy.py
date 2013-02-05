from src.similarity.MetaPathSimilarityStrategy import MetaPathSimilarityStrategy

__author__ = 'jontedesco'

class NeighborSimStrategy(MetaPathSimilarityStrategy):
    """
      Class that implements a meta-neighbor based similarity strategy, that counts half-paths, not necessarily connecting
      the two nodes, but connecting to shared neighbors.
    """

    def __init__(self, graph, metaPath=None, symmetric=False, reversed=False):
        super(NeighborSimStrategy, self).__init__(graph, metaPath, symmetric)
        self.reversed = reversed

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



        if self.reversed:

            # Find the shared out-neighbors of these nodes in the projected graph, and calculate the numerator
            sharedOutNeighbors = set(projectedGraph.getSuccessors(source)).intersection(projectedGraph.getSuccessors(destination))
            total = 1
            for sharedN in sharedOutNeighbors:
                total += (projectedGraph.getNumberOfEdges(source, sharedN) * projectedGraph.getNumberOfEdges(destination, sharedN))

            # Accumulate normalizations
            sourceNormalization = 1
            for sourceNeighbor in projectedGraph.getSuccessors(source):
                sourceNormalization += projectedGraph.getNumberOfEdges(source, sourceNeighbor)**2
            destNormalization = 1
            for destNeighbor in projectedGraph.getSuccessors(destination):
                destNormalization += projectedGraph.getNumberOfEdges(destination, destNeighbor)**2

        else:

            # Find the shared in-neighbors of these nodes in the projected graph, and calculate the numerator
            sharedInNeighbors = set(projectedGraph.getPredecessors(source)).intersection(projectedGraph.getPredecessors(destination))
            total = 1
            for sharedN in sharedInNeighbors:
                total += (projectedGraph.getNumberOfEdges(sharedN, source) * projectedGraph.getNumberOfEdges(sharedN, destination))

            # Accumulate normalizations
            sourceNormalization = 1
            for sourceNeighbor in projectedGraph.getPredecessors(source):
                sourceNormalization += projectedGraph.getNumberOfEdges(sourceNeighbor, source)**2
            destNormalization = 1
            for destNeighbor in projectedGraph.getPredecessors(destination):
                destNormalization += projectedGraph.getNumberOfEdges(destNeighbor, destination)**2

        similarityScore = total
        if total > 0:
            similarityScore = 2 * total / float(sourceNormalization + destNormalization)

        self.addToCache(source, destination, similarityScore)

        return similarityScore