import math
import networkx
from src.model.metapath.MetaPath import MetaPath

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
    def findMetaPaths(graph, startingNode, endingNode, metaPath, symmetricMetaPath = False):
        """
          Finds all paths that match the metaPath connecting the given nodes
        """

        # Verify that the given nodes are valid endpoints node for the given meta path if symmetric is not turned on
        assert(startingNode.__class__ == metaPath.classes[0])
        if not symmetricMetaPath:
            assert(endingNode.__class__ == metaPath.classes[-1])

        # Split logic based on whether or not the path should be a cycle
        if startingNode == endingNode:
            return MetaPathUtility.__findReflexiveMetaPaths(graph, startingNode, metaPath, symmetricMetaPath)
        else:
            return MetaPathUtility.__findNonReflexiveMetaPaths(graph, startingNode, endingNode, metaPath, symmetricMetaPath)


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


    @staticmethod
    def __findReflexiveMetaPaths(graph, startingNode, metaPath, symmetricMetaPath):
        """
          Helper function to find meta paths, given that we know the start and end nodes are the same
        """

        # First, find all neighbors reachable from the node on the half meta path (do nothing if we were only given half)
        midpointIndex = int(math.ceil(len(metaPath.classes)/2.0))
        metaPathToSearch =  metaPath if symmetricMetaPath else MetaPath(metaPath.classes[:midpointIndex+1], metaPath.weight)
        newClassesList = list(metaPathToSearch.classes)
        newClassesList.reverse()
        reversedMetaPathToSearch = MetaPath(newClassesList, metaPathToSearch.weight)

        # Find reachable nodes on this (possibly) partial meta path
        reachableNodes = MetaPathUtility.findMetaPathNeighbors(graph, startingNode, metaPathToSearch)

        metaPaths = []

        for endingNode in reachableNodes:
            pathsToNode = MetaPathUtility.findMetaPaths(graph, startingNode, endingNode, metaPathToSearch)
            for pathToNode in pathsToNode:
                pathsFromNode = MetaPathUtility.findMetaPaths(graph, endingNode, startingNode, reversedMetaPathToSearch)
                for pathFromNode in pathsFromNode:
                    concatenatedPath = pathToNode + pathFromNode[1:]
                    if concatenatedPath not in metaPaths:
                        metaPaths.append(concatenatedPath)

        return list(metaPaths)


    @staticmethod
    def __findNonReflexiveMetaPaths(graph, startingNode, endingNode, metaPath, symmetricMetaPath):
        """
          Helper function to find meta paths, given that we know the start and end nodes are not the same
        """

        metaPaths = []

        # Find all paths of the right length, then filter by the node types in the path
        allPathsOfCorrectOrLesserLength =\
            networkx.all_simple_paths(graph, startingNode, endingNode, len(metaPath.classes) - 1)

        for path in allPathsOfCorrectOrLesserLength:

            if len(path) < len(metaPath.classes):
                continue

            pathMatchesMetaPath = True
            for node, type in zip(path, metaPath.classes):
                if node.__class__ != type:
                    pathMatchesMetaPath = False
                    break

            if pathMatchesMetaPath:
                metaPaths.append(path)

        # If these meta paths must be symmetric, skip any meta paths where edges don't go in both directions
        return MetaPathUtility.__filterPathsForSymmetry(graph, metaPaths, symmetricMetaPath)


    @staticmethod
    def __filterPathsForSymmetry(graph, metaPaths, symmetricMetaPath):
        """
          Remove any paths that or asymmetrical, if that is required
        """

        if symmetricMetaPath:
            newMetaPaths = []
            for metaPath in metaPaths:
                for i in xrange(0, len(metaPath) - 1):
                    if graph.has_edge(metaPath[i + 1], metaPath[i]):
                        newMetaPaths.append(metaPath)
            metaPaths = newMetaPaths
        return metaPaths

