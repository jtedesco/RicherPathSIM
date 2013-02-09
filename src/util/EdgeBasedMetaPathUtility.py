from src.util.MetaPathUtility import MetaPathUtility

__author__ = 'jontedesco'

class EdgeBasedMetaPathUtility(MetaPathUtility):
    """
      Edge-based implementation of meta path utility
    """

    def _findMetaPathsHelper(self, graph, node, metaPathTypes, symmetric = True):
        """
          Iterative helper function to find nodes not yet visited according to types in meta path. This helper
          function cannot handle loops back to the original node, but CAN handle multi-edges
        """

        # We initially start with a path of length 0, just the starting node included
        paths = [(node,)]
        pathCounts = [1]

        for metaPathType in metaPathTypes:
            nextPaths = []
            nextPathCounts = []

            # For each partial path, add any extensions of this path that are valid
            for path, pathEdgeCount in zip(paths, pathCounts):
                nodesVisited = path
                node = path[-1]
                neighbors = graph.getSuccessors(node)
                for neighbor in neighbors:

                    # Do not add this next partial path if (1) it's already been visited, (2) it's the wrong type, or
                    # (3) we require paths to be symmetric and this edge does not exist in both directions
                    if neighbor == nodesVisited[-1]:
                        continue
                    if neighbor.__class__ != metaPathType:
                        continue
                    if symmetric and not (graph.hasEdge(neighbor, node) and graph.hasEdge(node, neighbor)):
                        continue

                    nextPaths.append(path + (neighbor,))
                    nextPathCounts.append(pathEdgeCount * graph.getNumberOfEdges(node, neighbor))

            paths = nextPaths
            pathCounts = nextPathCounts

        metaPathNeighbors = set(path[-1] for path in paths)

        # Adjust the number of total meta paths based on the number of edges between each step
        countAdjustedPaths = []
        for path, pathCount in zip(paths, pathCounts):
            countAdjustedPaths.extend([path] * pathCount)

        return metaPathNeighbors, countAdjustedPaths
