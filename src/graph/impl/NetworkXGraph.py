import networkx
from src.graph.Graph import Graph

__author__ = 'jontedesco'

class NetworkXGraph(Graph):
    """
      Interface to a networkx graph instance
    """

    def __init__(self):
        """
          Construct the new graph instance
        """

        self.graph = networkx.DiGraph()

    def addEdge(self, source, destination, attribute = None):
        attributeDictionary = None if attribute is None else attribute.toDict()
        self.graph.add_edge(source, destination, attr_dict = attributeDictionary)

    def addNode(self, node, attribute = None):
        attributeDictionary = None if attribute is None else attribute.toDict()
        self.graph.add_node(node, attr_dict = attributeDictionary)

    def getEdges(self):
        return self.graph.edges()

    def getNodes(self):
        return self.graph.nodes()

    def removeEdge(self, source, destination):
        return self.graph.has_edge(source, destination)

    def removeNode(self, node):
        return self.graph.remove_node(node)

    def hasNode(self, node):
        return self.graph.has_node(node)

    def hasEdge(self, source, destination):
        return self.graph.has_edge(source, destination)

    def getEdgeData(self, source, destination):
        return self.graph.get_edge_data(source, destination)

    def getSuccessors(self, node):
        return self.graph.successors(node)

    def getPredecessors(self, node):
        return self.graph.predecessors(node)

    def findAllPathsOfAtMostLength(self, source, destination, length):
        return networkx.all_simple_paths(self.graph, source, destination, length)

    def breadthFirstSearch(self, source):
        newGraph = NetworkXGraph()
        newGraph.graph = networkx.bfs_tree(self.graph, source)
        return newGraph

    def pageRank(self):
        return networkx.pagerank_numpy(self.graph)

