import networkx
from src.model.metapath.MetaPath import MetaPath

__author__ = 'jontedesco'

class MetaPathUtility(object):
    """
      Contains helper methods for dealing with meta paths. Note that this utility only handles meta paths that start and
      end at different nodes, and that never repeat nodes in the path (repeating meta path types is fine).
    """

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
        assert(node.__class__ == metaPath.classes[0])

        # Recursively traverse the graph using this type information
        return MetaPathUtility.__findMetaPathNeighborsHelper(graph, node, metaPath.classes[1:], set(), symmetric)


    @staticmethod
    def findMetaPaths(graph, startingNode, endingNode, metaPath, symmetric = False):
        """
          Finds all paths that match the metaPath connecting the given nodes
        """

        # Check that the endpoints are of the correct types
        assert(startingNode.__class__ == metaPath.classes[0])
        assert(endingNode.__class__ == metaPath.classes[-1])

        # Split logic based on whether or not the path should be a cycle
        if startingNode == endingNode:
            return MetaPathUtility.__findReflexiveMetaPaths(graph, startingNode, metaPath, symmetric)
        else:
            return MetaPathUtility.__findNonReflexiveMetaPaths(graph, startingNode, endingNode, metaPath, symmetric)


    @staticmethod
    def expandPartialMetaPath(partialMetaPath, repeatLastType = False):
        """
          Expands a partial meta path into a full one (i.e. ABC into ABCBA or ABCCBA)

            @param  partialMetaPath The partial meta path to expand
            @param  repeatLastType  Whether or not to repeat the last type in meta path expansion
                                    (i.e. should the final meta path be even length?)
        """

        metaPathClasses = partialMetaPath.classes
        reversedMetaPathClasses = list(metaPathClasses)
        reversedMetaPathClasses.reverse()
        metaPathClasses = partialMetaPath.classes if repeatLastType else partialMetaPath.classes[:-1] # Don't repeat the middle entry
        modifiedMetaPath = MetaPath(metaPathClasses + reversedMetaPathClasses, partialMetaPath.weight)

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

        neighbors = graph.neighbors(node)
        for neighbor in neighbors:

            # Skip visited neighbors
            if neighbor in visitedNodes:
                continue

            # Skip neighbors that don't match the next type in the meta path
            if neighbor.__class__ != metaPathTypes[0]:
                continue

            # If symmetry is enforced, skip neighbors that do not have both outgoing and incoming edges
            if symmetric and not (graph.has_edge(neighbor, node) and graph.has_edge(node, neighbor)):
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
    def __findReflexiveMetaPaths(graph, startingNode, metaPath, symmetric):
        """
          Helper function to find meta paths, given that we know the start and end nodes are the same
        """


        # Create a meta path one entry shorter
        modifiedMetaPath = MetaPath(metaPath.classes[:-1], metaPath.weight)

        # Find reachable nodes on this shorter meta path
        reachableNodes = MetaPathUtility.findMetaPathNeighbors(graph, startingNode, modifiedMetaPath)

        paths = []

        for endingNode in reachableNodes:
            if graph.has_edge(endingNode, startingNode):
                correctPaths = MetaPathUtility.__findNonReflexiveMetaPaths(graph, startingNode, endingNode, modifiedMetaPath, symmetric)
                for path in correctPaths:
                    paths.append(path + [startingNode])

        return paths


    @staticmethod
    def __findNonReflexiveMetaPaths(graph, startingNode, endingNode, metaPath, symmetric):
        """
          Helper function to find meta paths, given that we know the start and end nodes are not the same
        """

        paths = []

        # Find all paths of the right length, then filter by the node types in the path
        allPathsOfCorrectOrLesserLength = networkx.all_simple_paths(graph, startingNode, endingNode, len(metaPath.classes) - 1)

        for path in allPathsOfCorrectOrLesserLength:

            if len(path) < len(metaPath.classes):
                continue

            pathMatchesMetaPath = True
            for node, type in zip(path, metaPath.classes):
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
                if not graph.has_edge(path[i + 1], path[i]):
                    newMetaPaths.remove(path)
        return newMetaPaths

