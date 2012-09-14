from copy import deepcopy
import re
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
          Parses the input file content into basic data structures as an intermediate form before inserting into the graph.
        """

        arnetIdPrefix = '#arnetid'
        authorPrefix = '#@'
        conferencePrefix = '#conf'
        indexPrefix = '#index'
        titlePrefix = '#*'
        yearPrefix = '#year'


        templatePaper = {
            'references': []
        }
        currentPaper = deepcopy(templatePaper)
        outputData = {}

        for inputLine in inputContent.split('\n'):
            inputLine = inputLine.strip()

            if inputLine.startswith(titlePrefix):
                if currentPaper != templatePaper:
                    outputData[currentPaper['id']] = currentPaper
                    currentPaper = deepcopy(templatePaper)
                currentPaper['title'] = inputLine[len(titlePrefix):]
            elif inputLine.startswith(authorPrefix):
                currentPaper['authors'] = inputLine[len(authorPrefix):].split(',')
            elif inputLine.startswith(yearPrefix):
                currentPaper['year'] = int(inputLine[len(yearPrefix):])
            elif inputLine.startswith(conferencePrefix):
                currentPaper['conference'] = inputLine[len(conferencePrefix):]
            elif inputLine.startswith(indexPrefix):
                currentPaper['id'] = int(inputLine[len(indexPrefix):])
            elif inputLine.startswith(arnetIdPrefix):
                currentPaper['arnetid'] = int(inputLine[len(arnetIdPrefix):])

        outputData[currentPaper['id']] = currentPaper

        return outputData


    def buildGraph(self, parsedData):
        """
          Form the DBLP graph structure from the parsed data
        """
        pass
