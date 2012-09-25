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

