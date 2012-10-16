
__author__ = 'jontedesco'

class MetaPathUtility(object):
    """
      Contains helper methods for dealing with meta paths. Note that this utility only handles meta paths that start and
      end at different nodes, and that never repeat nodes in the path (repeating meta path types is fine).
    """

    # Parameter to control whether or not to try to read from cache (assume the graphs are never changed?)
    graphsImmutable = True

    # Dictionary indexed by initial arguments to __findMetaPathsHelper, containing the paths along a meta path from a node
    __metaPathsCache = {}

    @staticmethod
    def findMetaPathNeighbors(graph, node, metaPath, symmetric = False, checkLoops = True):
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
        (metaPathNeighbors, paths) = MetaPathUtility.__findMetaPathsHelper(graph, node, metaPath[1:], [], symmetric)
        if checkLoops:
            selfLoops = MetaPathUtility.__findLoopMetaPaths(graph, node, metaPath, symmetric)
            if len(selfLoops) > 0:
                metaPathNeighbors.add(node)
        return set(metaPathNeighbors)


    @staticmethod
    def findMetaPaths(graph, startingNode, endingNode, metaPath, symmetric = False):
        """
          Finds all paths that match the metaPath connecting the given nodes
        """

        # Check that the endpoints are of the correct types
        assert(startingNode.__class__ == metaPath[0])
        assert(endingNode.__class__ == metaPath[-1])

        # Split logic based on whether or not the path should be a cycle
        if startingNode == endingNode:
            return MetaPathUtility.__findLoopMetaPaths(graph, startingNode, metaPath, symmetric)
        else:
            return MetaPathUtility.__findNonLoopMetaPaths(graph, startingNode, endingNode, metaPath, symmetric)


    @staticmethod
    def expandPartialMetaPath(partialMetaPath, repeatLastType = False):
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


    @staticmethod
    def __findMetaPathsHelper(graph, node, metaPathTypes, previousNodes, symmetric):
        """
          Recursive helper function to recurse on nodes not yet visited according to types in meta path. This helper
          function cannot handle loops back to the original node, it assumes that we are only interested in paths that
          do not repeat any nodes, not even the start/end node.
        """

        # Prepare to use the cache if necessary
        shouldCacheResults = len(previousNodes) == 0 and MetaPathUtility.graphsImmutable
        cacheKey = (graph, node, tuple(metaPathTypes), symmetric)

        # Pull from cache if necessary
        if shouldCacheResults and cacheKey in MetaPathUtility.__metaPathsCache:
            return MetaPathUtility.__metaPathsCache[cacheKey]

        # Find the meta paths & meta path neighbors from this node
        metaPathNeighbors = set()
        paths = set()

        # Base case, we've reached the end of the meta path
        if len(metaPathTypes) == 0:
            return metaPathNeighbors, paths

        neighbors = graph.getSuccessors(node)
        for neighbor in neighbors:

            # Skip visited neighbors
            if neighbor in previousNodes:
                continue

            # Skip neighbors that don't match the next type in the meta path
            if neighbor.__class__ != metaPathTypes[0]:
                continue

            # If symmetry is enforced, skip neighbors that do not have both outgoing and incoming edges
            if symmetric and not (graph.hasEdge(neighbor, node) and graph.hasEdge(node, neighbor)):
                continue

            # If we're at the last node in the meta path, add it to the meta path neighbors
            if len(metaPathTypes) == 1:
                metaPathNeighbors.add(neighbor)
                paths.add(tuple(previousNodes + [node, neighbor]))
            else:

                # Otherwise, recurse & take union of all recursive calls
                neighborsFromThisNode, pathsFromThisNode = MetaPathUtility.__findMetaPathsHelper(
                    graph, neighbor, metaPathTypes[1:], previousNodes + [node], symmetric
                )
                paths = paths.union(pathsFromThisNode)
                metaPathNeighbors = metaPathNeighbors.union(neighborsFromThisNode)

        # Store in the cache if necessary
        if shouldCacheResults:
            MetaPathUtility.__metaPathsCache[cacheKey] = (metaPathNeighbors, paths)

        return metaPathNeighbors, paths


    @staticmethod
    def __findLoopMetaPaths(graph, startingNode, metaPath, symmetric):
        """
          Helper function to find meta paths, given that we know the start and end nodes are the same
        """


        # Create a meta path one entry shorter
        modifiedMetaPath = metaPath[:-1]

        # Find reachable nodes on this shorter meta path
        reachableNodes = MetaPathUtility.findMetaPathNeighbors(graph, startingNode, modifiedMetaPath, symmetric, False)

        paths = []
        pathsFound = set()

        for endingNode in reachableNodes:
            if not graph.hasEdge(endingNode, startingNode):
                continue
            correctPaths = MetaPathUtility.__findNonLoopMetaPaths(graph, startingNode, endingNode, modifiedMetaPath, symmetric)
            for path in correctPaths:
                if startingNode.__class__ != metaPath[-1]:
                    continue
                thisPath = path + [startingNode]

                # Check to see if we've already recorded this path or the reverse
                # (for paths A-B-C and C-B-A, only record one or the other)
                if tuple(thisPath) in pathsFound:
                    continue
                pathsFound.add(tuple(thisPath))
                paths.append(thisPath)

        return paths


    @staticmethod
    def __findNonLoopMetaPaths(graph, startingNode, endingNode, metaPath, symmetric):
        """
          Helper function to find meta paths, given that we know the start and end nodes are not the same
        """

        (metaPathNeighbors, paths) = MetaPathUtility.__findMetaPathsHelper(graph, startingNode, metaPath[1:], [], symmetric)
        return [list(path) for path in paths if path[-1] is endingNode]