__author__ = 'jontedesco'

class ExperimentHelper(object):
    """
      Helper class for general experiments on graphs
    """

    def __init__(self):

        # Two - level index of attribute name & value to nodes in the graph, built lazily
        self.attributeNodeMap = {}

        # Indexed by node type (class), built lazily, contains sets of nodes according to type
        self.typeNodeMap = {}


    def getNodesByAttribute(self, graph, attributeName, attributeValue, attributeType = None):
        """
          Find a node (efficiently as possible) from the graph with the given attribute. Computes the index for all nodes
          containing the given attribute
        """

        # Build the attribute index if it does not already exist
        if attributeName not in self.attributeNodeMap:
            self.attributeNodeMap[attributeName] = {}

            for node in graph.getNodes():

                # Skip nodes of the wrong type entirely
                if attributeType is not None and not isinstance(node, attributeType):
                    continue

                nodeData = node.toDict()
                if attributeName in nodeData:

                    nodeValue = nodeData[attributeName]
                    if type(nodeValue) is type([]):
                        continue

                    if nodeValue not in self.attributeNodeMap[attributeName]:
                        self.attributeNodeMap[attributeName][nodeValue] = set()

                    self.attributeNodeMap[attributeName][nodeValue].add(node)

        # Return the nodes that have this value for this particular attribute
        attributeMap = self.attributeNodeMap[attributeName]
        return set() if attributeValue not in attributeMap else attributeMap[attributeValue]


    def getNodesByType(self, graph, targetType):
        """
          Find all nodes (efficiently as possible) with the given type. This will compute the index for all types
        """

        if targetType not in self.typeNodeMap:
            for node in graph.getNodes():

                nodeType = type(node)
                if nodeType not in self.typeNodeMap:
                    self.typeNodeMap[nodeType] = set()

                self.typeNodeMap[nodeType].add(node)

        return set() if targetType not in self.typeNodeMap else self.typeNodeMap[targetType]