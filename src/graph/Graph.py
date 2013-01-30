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


    def getEdges(self, nodes = list()):
        """
          Get the edges of the graph, optionally with some specified set of starting nodes
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


    def getNumberOfEdges(self, source, destination):
        """
          Get the number of edges between the given pair of nodes
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


    def getPredecessorsOfType(self, node, type):
        """
          Get nodes preceding a node of a certain type only
        """

        predecessorsOfType = set()
        predecessors = self.getPredecessors(node)
        for predecessor in predecessors:
            if isinstance(predecessor, type):
                predecessorsOfType.add(node)

        return predecessorsOfType


    def getSuccessorsOfType(self, node, type):
        """
          Get successors of a node of a certain type only
        """

        successorsOfType = set()
        successors = self.getSuccessors(node)
        for successor in successors:
            if isinstance(successor, type):
                successorsOfType.add(successor)

        return successorsOfType


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


    def breadthFirstSearch(self, source):
        """
          Returns the tree found performing BFS from the given root
        """
        raise NotImplementedError()


    def pageRank(self, alpha=0.85, personalization=None):
        """
          Computes and returns PageRank scores for the this graph
        """
        raise NotImplementedError()


    def cloneEmpty(self):
        """
          Creates an empty copy of this graph and returns it (new graph of same implementation
        """
        raise NotImplementedError()