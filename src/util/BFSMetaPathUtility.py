from src.util.MetaPathUtility import MetaPathUtility

__author__ = 'jontedesco'

class BFSMetaPathUtility(MetaPathUtility):
    """
      Iterative implementation of meta path utility interface
    """

    def _findMetaPathsHelper(self, graph, node, metaPathTypes, previousNodes, symmetric):
        """
          Iterative helper function to find nodes not yet visited according to types in meta path. This helper
          function cannot handle loops back to the original node, it assumes that we are only interested in paths that
          do not repeat any nodes, not even the start/end node.
        """

        # Prepare to use the cache if possible
        shouldCacheResults = len(previousNodes) == 0 and hasattr(graph, 'inputPath')

        # Pull from cache if possible
        try:
            cacheData = self._readFromCache(graph, node, metaPathTypes, symmetric)
            if shouldCacheResults and cacheData is not None:
                return cacheData
        except ValueError:
            print "Error reading from cache..."

        # We initially start with a path of length 0, just the starting node included
        paths = {(node,)}

        for metaPathType in metaPathTypes:
            nextPaths = set()

            # For each partial path, add any extensions of this path that are valid
            for path in paths:
                nodesVisited = set(path)
                node = path[-1]
                neighbors = graph.getSuccessors(node)
                for neighbor in neighbors:

                    # Do not add this next partial path if (1) it's already been visited, (2) it's the wrong type, or
                    # (3) we require paths to be symmetric and this edge does not exist in both directions
                    if neighbor in nodesVisited:
                        continue
                    if neighbor.__class__ != metaPathType:
                        continue
                    if symmetric and not (graph.hasEdge(neighbor, node) and graph.hasEdge(node, neighbor)):
                        continue

                    nextPaths.add(path + (neighbor,))

            paths = nextPaths

        metaPathNeighbors = set(path[-1] for path in paths)

        # Store in the cache if possible
        if shouldCacheResults:
            try:
                self._addToCache(graph, node, metaPathTypes, symmetric, metaPathNeighbors, paths)
            except UnicodeDecodeError:
                print "Skipping adding data to cache..."

        return metaPathNeighbors, paths
