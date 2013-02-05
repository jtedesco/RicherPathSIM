import networkx
from src.graph.Graph import Graph

__author__ = 'jontedesco'

class NetworkXGraph(Graph):
    """
      Interface to a networkx graph instance
    """

    def __init__(self, graph = None):
        """
          Construct the new graph instance
        """
        super(NetworkXGraph, self).__init__()

        self.graph = networkx.MultiDiGraph() if graph is None else graph

    def addEdge(self, source, destination, attribute = None):
        attributeDictionary = None if attribute is None else attribute.toDict()
        self.graph.add_edge(source, destination, attr_dict = attributeDictionary)

    def addNode(self, node, attribute = None):
        attributeDictionary = None if attribute is None else attribute.toDict()
        self.graph.add_node(node, attr_dict = attributeDictionary)

    def getEdges(self, nodes = list()):
        return self.graph.edges(nodes)

    def getNodes(self):
        return self.graph.nodes()

    def removeEdge(self, source, destination):
        return self.graph.remove_edge(source, destination)

    def removeNode(self, node):
        return self.graph.remove_node(node)

    def hasNode(self, node):
        return self.graph.has_node(node)

    def hasEdge(self, source, destination):
        return self.graph.has_edge(source, destination)

    def getEdgeData(self, source, destination):
        return self.graph.get_edge_data(source, destination)

    def getNumberOfEdges(self, source, destination):
        return self.graph.number_of_edges(source, destination)

    def getSuccessors(self, node):
        return self.graph.successors(node)

    def getPredecessors(self, node):
        return self.graph.predecessors(node)

    def breadthFirstSearch(self, source):
        return NetworkXGraph(networkx.bfs_tree(self.graph, source))

    def hits(self):
        return networkx.hits_numpy(self.graph)

    def pageRank(self, alpha=0.85, personalization=None):
        return networkx.pagerank_numpy(self.graph, alpha, personalization)

    def reverse(self):
        return NetworkXGraph(self.graph.reverse())

    def subGraph(self, nodes):
        return NetworkXGraph(self.graph.subgraph(nodes))

    def cloneEmpty(self):
        return NetworkXGraph()
