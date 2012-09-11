from threading import Thread

__author__ = 'jon'


class ArnetMinerDataImporter(Thread):
    """
      Imports the DBLP citation data set (V5 format) into a python graph structure stored in NetworkX.
    """

    def __init__(self, inputPath, outputPath):

        self.inputPath = inputPath
        self.outputPath = outputPath

        super(ArnetMinerDataImporter, self).__init__()


    def run(self):
        with open(self.inputPath) as f:
            inputContent = f.read()
        parsedData = self.parseInputContent(inputContent)
        graph = self.buildGraph(parsedData)


    def parseInputContent(self, inputContent):
        """
          Parses the input file contentinto basic data structures as an intermediate form before inserting into the graph.
        """
        pass


    def buildGraph(self, parsedData):
        """
          Form the DBLP graph structure from the parsed data
        """
        pass

