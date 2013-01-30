import numpy
from src.similarity.MetaPathSimilarityStrategy import MetaPathSimilarityStrategy

__author__ = 'jontedesco'

class ProjectedPageRankStrategy(MetaPathSimilarityStrategy):
    """
      Class that computes the absolute difference between the PageRank of two nodes
    """

    def __init__(self, graph, metaPath, nodeSets = None, symmetric = False):
        """
          Constructs a meta path similarity strategy, storing the meta path data for this strategy.

            @param  graph       The graph
            @param  nodeSets    The set of tuples of nodes to use to project subgraphs
            @param  metaPath    Meta path object where the list of classes contains classes of nodes in the graph,
                                and weights in [0,1] containing the importance of the meta path

            @param  symmetric   Whether or not to enforce that meta paths must be symmetric

            For example, if 'symmetric' and 'evenLength' are both 'true', for meta path 'ABC', we will only count meta
            path 'ABCCBA', depending on, and if 'symmetric' is 'true' while 'evenLength' is 'false', we will only count
            meta paths 'ABCBA'
        """

        super(ProjectedPageRankStrategy, self).__init__(graph, metaPath, symmetric)
        if nodeSets is None:
            self.nodeSets = set()
            self.nodeSets.add(tuple(graph.getNodes()))
        else:
            self.nodeSets = nodeSets


    def findSimilarityScore(self, source, destination):
        """
          Find the similarity score between
        """

        if self.getFromCache(source, destination) is not None:
            return self.getFromCache(source, destination)

        sourceScoreVector = []
        destinationScoreVector = []
        for nodeSet in self.nodeSets:

            # Subgraph to use for projection
            subgraph = self.__induceHeterogeneousSubgraph(nodeSet)

            # Project graph
            if self.metaPath[0] == self.metaPath[-1]: # Homogeneous projection?
                projectedGraph = self.metaPathUtility.createHomogeneousProjection(subgraph, self.metaPath)
            else:
                projectedGraph = self.metaPathUtility.createHeterogeneousProjection(subgraph, self.metaPath)

            # Calculate PageRank in network (default alpha & no personalization)
            pageRanks = projectedGraph.pageRank()

            sourceScore = pageRanks[source] if source in pageRanks else 0
            destinationScore = pageRanks[destination] if destination in pageRanks else 0
            sourceScoreVector.append(sourceScore)
            destinationScoreVector.append(destinationScore)

        # Compute Euclidean norm
        similarityScore = 1 - (numpy.linalg.norm(numpy.array(sourceScoreVector) - numpy.array(destinationScoreVector)))

        self.addToCache(source, destination, similarityScore)

        return similarityScore


    def __induceHeterogeneousSubgraph(self, nodeSetOfOneType):

        givenType = list(nodeSetOfOneType)[0].__class__
        nodeSet = set()
        for node in self.graph.getNodes():
            if node.__class__ != givenType or node in nodeSetOfOneType:
                nodeSet.add(node)

        return self.graph.subGraph(nodeSet)
