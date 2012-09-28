import logging
import threading
import cPickle
from src.logger.ColoredLogger import ColoredLogger

__author__ = 'jontedesco'


class Experiment(threading.Thread):
    """
      Top-level class for running experiments, containing helper methods common code for experiments
    """

    def __init__(self, inputGraphPath, experimentTitle, outputFilePath=None):
        """
          Creates a new experiment to run, given the path to the serialized graph object to load
        """
        super(Experiment, self).__init__()

        # Load the graph from the file
        self.graph = cPickle.load(open(inputGraphPath)) if inputGraphPath is not None else None

        # Two - level index of attribute name & value to nodes in the graph, built lazily
        self.attributeNodeMap = {}

        # Indexed by node type (class), built lazily, contains sets of nodes according to type
        self.typeNodeMap = {}

        self.outputFilePath = outputFilePath

        logging.setLoggerClass(ColoredLogger)
        self.logger = logging.getLogger(experimentTitle)


    def output(self, text):
        """
          Output a line of text to the output file (if it exists), or otherwise, output to console
        """

        if self.outputFilePath is not None:
            with open(self.outputFilePath, 'a') as f:
                f.write(text + '\n')
        else:
            print(text)


    def getNodesByAttribute(self, attributeName, attributeValue, attributeType = None):
        """
          Find a node (efficiently as possible) from the graph with the given attribute. Computes the index for all nodes
          containing the given attribute
        """

        # Build the attribute index if it does not already exist
        if attributeName not in self.attributeNodeMap:
            self.attributeNodeMap[attributeName] = {}

            for node in self.graph.getNodes():

                # Skip nodes of the wrong type entirely
                if attributeType is not None and not isinstance(node, attributeType):
                    continue

                nodeData = node.toDict()
                if attributeName in nodeData:

                    nodeValue = nodeData[attributeName]
                    if nodeValue not in self.attributeNodeMap[attributeName]:
                        self.attributeNodeMap[attributeName][nodeValue] = set()

                    self.attributeNodeMap[attributeName][nodeValue].add(node)

        # Return the nodes that have this value for this particular attribute
        attributeMap = self.attributeNodeMap[attributeName]
        return set() if attributeValue not in attributeMap else attributeMap[attributeValue]


    def getNodesByType(self, targetType):
        """
          Find all nodes (efficiently as possible) with the given type. This will compute the index for all types
        """

        if targetType not in self.typeNodeMap:
            for node in self.graph.getNodes():

                nodeType = type(node)
                if nodeType not in self.typeNodeMap:
                    self.typeNodeMap[nodeType] = set()

                self.typeNodeMap[nodeType].add(node)

        return set() if targetType not in self.typeNodeMap else self.typeNodeMap[targetType]