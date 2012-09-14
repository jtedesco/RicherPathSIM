from copy import deepcopy
from threading import Thread
from src.importer.error.ArnetParseError import ArnetParseError

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
        citationPrefix = '#%'
        conferencePrefix = '#conf'
        indexPrefix = '#index'
        titlePrefix = '#*'
        yearPrefix = '#year'

        templatePaper = {
            'references': []
        }
        currentPaper = deepcopy(templatePaper)
        outputData = {}

        referencedPaperIds = set()
        paperIds = set()

        for inputLine in inputContent.split('\n'):
            inputLine = inputLine.strip()

            try:
                if inputLine.startswith(titlePrefix):
                    if currentPaper != templatePaper:
                        outputData[currentPaper['id']] = currentPaper
                        paperIds.add(currentPaper['id'])
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
                elif inputLine.startswith(citationPrefix):
                    referencedPaperId = int(inputLine[len(citationPrefix):])
                    referencedPaperIds.add(referencedPaperId)
                    currentPaper['references'].append(referencedPaperId)

                # Ignore other input lines

            except KeyError, e:
                raise ArnetParseError('Failed to parse data, missing paper attribute "%s"' % e.message)

        # Check that all citations are valid
        if referencedPaperIds.difference(paperIds) != set():
            raise ArnetParseError('Failed to parse data, invalid references in found')

        outputData[currentPaper['id']] = currentPaper

        return outputData


    def buildGraph(self, parsedData):
        """
          Form the DBLP graph structure from the parsed data
        """
        pass
