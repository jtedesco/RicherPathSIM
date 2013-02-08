import itertools
import numpy

__author__ = 'jontedesco'

class MetaPathUtility(object):
    """
      Contains helper methods for dealing with meta paths. Note that this utility only handles meta paths that start and
      end at different nodes, and that never repeat nodes in the path (repeating meta path types is fine).
    """

    def findMetaPathNeighbors(self, graph, node, metaPath, symmetric = False, checkLoops = True):
        """
          Finds the neighbors of some node along the given meta path, i.e. nodes that are reachable from the given node
          along the given meta path.

            @param  graph       The graph in which to find meta path neighbors
            @param  node        The starting node for which to find neighbors
            @param  metaPath
        """

        # Verify that the given node is a valid starting node for the given meta path
        assert(node.__class__ == metaPath[0])

        # Get the paths & neighbors, then add this node if necessary
        (metaPathNeighbors, paths) = self._findMetaPathsHelper(graph, node, metaPath[1:], symmetric = symmetric)
        if checkLoops:
            selfLoops = self.__findLoopMetaPaths(graph, node, metaPath, symmetric)
            if len(selfLoops) > 0:
                metaPathNeighbors.add(node)
        return set(metaPathNeighbors)


    def _findMetaPathsHelper(self, graph, node, metaPath, symmetric):
        raise NotImplementedError("Implement a concrete subclass to find meta paths!")


    def findMetaPaths(self, graph, startingNode, endingNode, metaPath, symmetric = False):
        """
          Finds all paths that match the metaPath connecting the given nodes
        """

        # Check that the endpoints are of the correct types
        assert(startingNode.__class__ == metaPath[0])
        assert(endingNode.__class__ == metaPath[-1])

        # Split logic based on whether or not the path should be a cycle
        if startingNode == endingNode:
            return self.__findLoopMetaPaths(graph, startingNode, metaPath, symmetric)
        else:
            return self.__findNonLoopMetaPaths(graph, startingNode, endingNode, metaPath, symmetric)


    def expandPartialMetaPath(self, partialMetaPath, repeatLastType = False):
        """
          Expands a partial meta path into a full one (i.e. ABC into ABCBA or ABCCBA)

            @param  partialMetaPath The partial meta path to expand
            @param  repeatLastType  Whether or not to repeat the last type in meta path expansion
                                    (i.e. should the final meta path be even length?)
        """

        reversedMetaPath = list(partialMetaPath)
        reversedMetaPath.reverse()
        metaPath = partialMetaPath if repeatLastType else partialMetaPath[:-1] # Don't repeat the middle entry
        modifiedMetaPath = metaPath + reversedMetaPath

        return modifiedMetaPath


    def createHomogeneousProjection(self, graph, metaPath, symmetric = False):
        """
          Create a homogeneous graph projection of some meta path
        """

        # Check that the endpoints are of the correct types
        assert(metaPath[0] == metaPath[-1])
        return self.__projectionHelper(graph, metaPath, symmetric = symmetric)


    def createHeterogeneousProjection(self, graph, metaPath, symmetric = False):
        """
          Create a homogeneous graph projection of some meta path
        """

        # Check that the endpoints are of the correct types
        assert(metaPath[0] != metaPath[-1])
        return self.__projectionHelper(graph, metaPath, symmetric = symmetric, heterogeneous = True)


    def getAdjacencyMatrixFromGraph(self, graph, metaPath = None, symmetric = False):
        """
          Computes a graph projection (if meta path is provided), and the adjacency matrix
        """

        if metaPath is not None:
            projFunction = self.createHomogeneousProjection if metaPath[0] == metaPath[-1] else self.createHeterogeneousProjection
            projectedGraph = projFunction(graph, metaPath, symmetric)
        else:
            projectedGraph = graph

        nodes, n = projectedGraph.getNodes(), len(projectedGraph.getNodes())
        nodesIndex = {nodes[i]: i for i in xrange(0, n)}

        adjacencyMatrix = numpy.zeros((n, n))
        for x, y in itertools.product(nodes, nodes):
            adjacencyMatrix[nodesIndex[x]][nodesIndex[y]] = projectedGraph.getNumberOfEdges(x, y)

        return adjacencyMatrix, nodesIndex


    def __projectionHelper(self, graph, metaPath, symmetric = False, heterogeneous = False):
        """
          Helper method to assist in creating a projection over a graph using some meta path
        """

        newGraph = graph.cloneEmpty()

        # Get the nodes of the projected graph
        for node in graph.getNodes():
            if isinstance(node, metaPath[0]) or (heterogeneous and isinstance(node, metaPath[-1])):
                newGraph.addNode(node)

        # Add the edges for this graph
        for node in newGraph.getNodes():
            if not isinstance(node, metaPath[0]): continue
            neighbors = self.findMetaPathNeighbors(graph, node, metaPath)
            for neighbor in neighbors:
                if not isinstance(neighbor, metaPath[-1]): continue
                numPaths = len(self.findMetaPaths(graph, node, neighbor, metaPath))
                for i in xrange(0, numPaths):
                    newGraph.addEdge(node, neighbor)
                    if symmetric: newGraph.addEdge(neighbor, node)

        return newGraph


    def __findLoopMetaPaths(self, graph, startingNode, metaPath, symmetric):
        """
          Helper function to find meta paths, given that we know the start and end nodes are the same
        """

        # Find reachable nodes on this shorter meta path
        reachableNodes, paths = self._findMetaPathsHelper(graph, startingNode, metaPath[1:-1], symmetric = symmetric)

        returnPaths = []
        pathsFound = set()

        for path in paths:

            # Sanity check
            if startingNode.__class__ != metaPath[-1]:
                continue

            endingNode = path[-1]
            if not graph.hasEdge(endingNode, startingNode):
                continue
            if symmetric and not graph.hasEdge(startingNode, endingNode):
                continue

            thisPath = list(path) + [startingNode]

            # Check to see if we've already recorded this path
            if tuple(thisPath) in pathsFound:
                continue

            pathsFound.add(tuple(thisPath))
            returnPaths.append(thisPath)

        return returnPaths


    def __findNonLoopMetaPaths(self, graph, startingNode, endingNode, metaPath, symmetric):
        """
          Helper function to find meta paths, given that we know the start and end nodes are not the same
        """

        (metaPathNeighbors, paths) = self._findMetaPathsHelper(graph, startingNode, metaPath[1:], symmetric = symmetric)
        return [list(path) for path in paths if path[-1] is endingNode]
