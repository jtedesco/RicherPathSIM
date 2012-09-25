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


    def addBothEdges(self, source, destination, attribute = None):
        """
          Add edges in both directions in graph
        """
        self.addEdge(source, destination, attribute)
        self.addEdge(destination, source, attribute)


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


    def hasNode(self, node):
        """
          Quickly checks if the graph contains a node
        """
        raise NotImplementedError()


    def hasEdge(self, source, destination):
        """
          Quickly checks if the graph contains an edge
        """
        raise NotImplementedError()


    def getPredecessors(self, node):
        """
          Get nodes preceding a node
        """
        raise NotImplementedError()


    def getSuccessors(self, node):
        """
          Get edges appearing on outgoing edges from a node
        """
        raise NotImplementedError()


    def getEdgeData(self, source, destination):
        """
          Gets the data associated with an edge of the graph
        """
        raise NotImplementedError()


    def removeNode(self, node):
        """
          Remove a node from the graph
        """
        raise NotImplementedError()


    def removeEdge(self, source, destination):
        """
          Remove an edge from the graph
        """
        raise NotImplementedError()