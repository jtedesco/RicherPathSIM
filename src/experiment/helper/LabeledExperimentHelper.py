import os
from src.experiment.helper import ExperimentHelper

__author__ = 'jontedesco'

class LabeledExperimentHelper(ExperimentHelper):
    """
      Helper class for experiments with relevance labels
    """

    def __init__(self, labelFolderPath):
        """
          Constructs a labeled experiment helper object, given the path to the root folder containing the query labels

            @param  labelFolderPath  The path to the folder containing relevance labels
        """

        super(LabeledExperimentHelper, self).__init__()

        # Dictionary of query node attribute, other node attribute tuples to relevance scores
        self.labelDictionary = {}

        for fileName in os.listdir(labelFolderPath):
            with open(os.path.join(labelFolderPath, fileName)) as f:

                # We assume the first result node to be the query node
                line = f.readline().strip().split()
                queryNodeAttribute = ' '.join(line[1:-1])
                selfRelevance = int(line[-1])

                self.labelDictionary[(queryNodeAttribute, queryNodeAttribute)] = selfRelevance

                for line in f.readlines():
                    line = line.strip().split()
                    if len(line) > 0:
                        nodeAttribute = ' '.join(line[1:-1])
                        nodeRelevance = int(line[-1])

                        # Only insert this relevance data if it's nonzero, otherwise, we will assume it's zero
                        if nodeRelevance > 0:
                            self.labelDictionary[(queryNodeAttribute, nodeAttribute)] = nodeRelevance


    def getLabelForNode(self, queryNode, resultNode, attribute = 'name'):
        """
          Return the relevance label from least relevant (0) to most relevant (2). If no relevance data is available for
          the given node & query node, non-relevance (0) is assumed.
        """

        key = (queryNode.toDict()[attribute], resultNode.toDict()[attribute])
        return self.labelDictionary[key] if key in self.labelDictionary else 0