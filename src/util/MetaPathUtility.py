import networkx

__author__ = 'jontedesco'

class MetaPathUtility(object):
    """
      Contains helper methods for dealing with meta paths. Note that this utility only handles meta paths that start and
      end at different nodes, and that never repeat nodes in the path (repeating meta path types is fine).
    """

    @staticmethod
    def findMetaPathNeighbors(graph, node, metaPath):
        """
          Finds the neighbors of some node along the given meta path, i.e. nodes that are reachable from the given node
          along the given meta path.

            @param  graph       The graph in which to find meta path neighbors
            @param  node        The starting node for which to find neighbors
            @param  metaPath
        """

        # Verify that the given node is a valid starting node for the given meta path
        assert(node.__class__ == metaPath.classes[0])

        # Recursively traverse the graph using this type information
        return MetaPathUtility.__findMetaPathNeighborsHelper(graph, node, metaPath.classes[1:], set())


    @staticmethod
    def findMetaPaths(graph, startingNode, endingNode, metaPath):
        """
          Finds all paths that match the metaPath connecting the given nodes
        """

        # Verify that the given nodes are valid endpoints node for the given meta path
        assert(startingNode.__class__ == metaPath.classes[0])
        assert(endingNode.__class__ == metaPath.classes[-1])

        # Find all paths matching the given meta paths
        metaPaths = []

        # Find all paths of the right length, then filter by the node types in the path
        allPathsOfCorrectLength = networkx.all_simple_paths(graph, startingNode, endingNode, len(metaPath.classes) - 1)
        for path in allPathsOfCorrectLength:
            pathMatchesMetaPath = True
            for node, type in zip(path, metaPath.classes):
                if node.__class__ != type:
                    pathMatchesMetaPath = False
                    break
            if pathMatchesMetaPath:
                metaPaths.append(path)

        return metaPaths


    @staticmethod
    def __findMetaPathNeighborsHelper(graph, node, metaPathTypes, visitedNodes):
        """
          Recursive helper function to recurse on nodes not yet visited according to types in meta path
        """

        metaPathNeighbors = set()

        # Base case, we've reached the end of the meta path
        if len(metaPathTypes) == 0:
            return metaPathNeighbors

        neighbors = graph.neighbors(node)
        for neighbor in neighbors:

            # Skip visited neighbors
            if neighbor in visitedNodes:
                continue

            # Skip neighbors that don't match the next type in the meta path
            if neighbor.__class__ != metaPathTypes[0]:
                continue

            # If we're at the last node in the meta path, add it to the meta path neighbors
            if len(metaPathTypes) == 1:
                metaPathNeighbors.add(neighbor)
            else:

                # Otherwise, recurse & take union of all recursive calls
                neighborsFromThisNode = MetaPathUtility.__findMetaPathNeighborsHelper(
                    graph, neighbor, metaPathTypes[1:], visitedNodes.union({neighbor})
                )
                metaPathNeighbors = metaPathNeighbors.union(neighborsFromThisNode)

        return metaPathNeighbors
