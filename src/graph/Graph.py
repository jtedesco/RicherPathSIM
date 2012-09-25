__author__ = 'jontedesco'

class Graph(object):
    """
      Abstract interface for interacting with a graph instance (directed graph)
    """

    def addNode(self, node):
        """
          Add a node to this graph
        """
        raise NotImplementedError()


    def addNodes(self, nodes):
        for node in nodes:
            self.addNode(node)


    def addEdge(self, source, destination, attribute = None):
        """
          Add a (directed) edge to this graph
        """
        raise NotImplementedError()


    def addEdges(self, edges):
        for source, destination in edges:
            self.addEdge(source, destination)


    def getNodes(self):
        """
          Get the nodes of the graph
        """
        raise NotImplementedError()


    def getEdges(self):
        """
          Get the edges of the graph
        """
        raise NotImplementedError()
