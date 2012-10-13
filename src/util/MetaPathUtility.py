
__author__ = 'jontedesco'

class MetaPathUtility(object):
    """
      Contains helper methods for dealing with meta paths. Note that this utility only handles meta paths that start and
      end at different nodes, and that never repeat nodes in the path (repeating meta path types is fine).
    """

    # Parameter to control whether or not to try to read from cache (assume the graphs are never changed?)
    graphsImmutable = True

    # Dictionary indexed by arguments to findMetaPathNeighbors, containing the meta paths between two nodes
    __metaPathsCache = {}

    # Dictionary indexed by arguments to findMetaPathNeighbors, containing the meta path neighbors for a node
    __metaPathNeighborsCache = {}


    @staticmethod
    def findMetaPathNeighbors(graph, node, metaPath, symmetric = False):
        """
          Finds the neighbors of some node along the given meta path, i.e. nodes that are reachable from the given node
          along the given meta path.

            @param  graph       The graph in which to find meta path neighbors
            @param  node        The starting node for which to find neighbors
            @param  metaPath
        """

        # Verify that the given node is a valid starting node for the given meta path
        assert(node.__class__ == metaPath[0])

        # Attempt to read from cache first
        cacheKey = (graph, node, tuple(metaPath), symmetric)
        if cacheKey in MetaPathUtility.__metaPathNeighborsCache:
            return MetaPathUtility.__metaPathNeighborsCache[cacheKey]

        # Cache & return the value
        cacheData = MetaPathUtility.__findMetaPathNeighborsHelper(graph, node, metaPath[1:], set(), symmetric)
        MetaPathUtility.__metaPathNeighborsCache[cacheKey] = cacheData
        return cacheData


    @staticmethod
    def findMetaPaths(graph, startingNode, endingNode, metaPath, symmetric = False):
        """
          Finds all paths that match the metaPath connecting the given nodes
        """

        # Check that the endpoints are of the correct types
        assert(startingNode.__class__ == metaPath[0])
        assert(endingNode.__class__ == metaPath[-1])

        # Attempt to read from cache first
        cacheKey = (graph, startingNode, endingNode, tuple(metaPath), symmetric)
        if cacheKey in MetaPathUtility.__metaPathsCache:
            return MetaPathUtility.__metaPathsCache[cacheKey]

        # Split logic based on whether or not the path should be a cycle, and add to cache
        if startingNode == endingNode:
            cacheData = MetaPathUtility.__findLoopMetaPaths(graph, startingNode, metaPath, symmetric)
        else:
            cacheData = MetaPathUtility.__findNonLoopMetaPaths(graph, startingNode, endingNode, metaPath, symmetric)
        MetaPathUtility.__metaPathsCache[cacheKey] = cacheData
        return cacheData


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
    def __findMetaPathNeighborsHelper(graph, node, metaPathTypes, visitedNodes, symmetric):
        """
          Recursive helper function to recurse on nodes not yet visited according to types in meta path
        """

        metaPathNeighbors = set()

        # Base case, we've reached the end of the meta path
        if len(metaPathTypes) == 0:
            return metaPathNeighbors

        neighbors = graph.getSuccessors(node)
        for neighbor in neighbors:

            # Skip visited neighbors
            if neighbor in visitedNodes:
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
            else:

                # Otherwise, recurse & take union of all recursive calls
                neighborsFromThisNode = MetaPathUtility.__findMetaPathNeighborsHelper(
                    graph, neighbor, metaPathTypes[1:], visitedNodes.union({neighbor}), symmetric
                )
                metaPathNeighbors = metaPathNeighbors.union(neighborsFromThisNode)

        return metaPathNeighbors


    @staticmethod
    def __findLoopMetaPaths(graph, startingNode, metaPath, symmetric):
        """
          Helper function to find meta paths, given that we know the start and end nodes are the same
        """


        # Create a meta path one entry shorter
        modifiedMetaPath = metaPath[:-1]

        # Find reachable nodes on this shorter meta path
        reachableNodes = MetaPathUtility.findMetaPathNeighbors(graph, startingNode, modifiedMetaPath)

        paths = []
        pathsFound = set()

        for endingNode in reachableNodes:
            if graph.hasEdge(endingNode, startingNode):
                correctPaths = MetaPathUtility.__findNonLoopMetaPaths(graph, startingNode, endingNode, modifiedMetaPath, symmetric)
                for path in correctPaths:
                    thisPath = path + [startingNode]

                    # Check to see if we've already recorded this path or the reverse
                    # (for paths A-B-C and C-B-A, only record one or the other)
                    if tuple(thisPath) not in pathsFound:
                        pathsFound.add(tuple(thisPath))
                        paths.append(thisPath)

        return paths


    @staticmethod
    def __findNonLoopMetaPaths(graph, startingNode, endingNode, metaPath, symmetric):
        """
          Helper function to find meta paths, given that we know the start and end nodes are not the same
        """

        paths = []

        # Find all paths of the right length, then filter by the node types in the path
        allPathsOfCorrectLength = graph.findAllPathsOfLength(startingNode, endingNode, len(metaPath))

        for path in allPathsOfCorrectLength:
            pathMatchesMetaPath = True
            for node, type in zip(path, metaPath):
                if node.__class__ != type:
                    pathMatchesMetaPath = False
                    break

            if pathMatchesMetaPath:
                paths.append(path)

        # If these meta paths must be symmetric, skip any meta paths where edges don't go in both directions
        return MetaPathUtility.__filterPathsForSymmetry(graph, paths) if symmetric else paths


    @staticmethod
    def __filterPathsForSymmetry(graph, paths):
        """
          Remove any paths that are asymmetrical
        """

        newMetaPaths = list(paths)
        for path in paths:
            for i in xrange(0, len(path) - 1):
                if not graph.hasEdge(path[i + 1], path[i]):
                    newMetaPaths.remove(path)
        return newMetaPaths