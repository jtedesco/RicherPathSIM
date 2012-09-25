import json
import logging
import os
import Stemmer
import cPickle
from threading import Thread
from copy import deepcopy
from src.graph.GraphFacade import GraphFacade
from src.importer.error.ArnetParseError import ArnetParseError
from src.logger.ColoredLogger import ColoredLogger
from src.model.edge.dblp.Authorship import Authorship
from src.model.edge.dblp.Citation import Citation
from src.model.edge.dblp.Mention import Mention
from src.model.edge.dblp.Publication import Publication
from src.model.node.dblp.Author import Author
from src.model.node.dblp.Paper import Paper
from src.model.node.dblp.Topic import Topic
from src.model.node.dblp.Conference import Conference

__author__ = 'jon'


class ArnetMinerDataImporter(Thread):
    """
      Imports the DBLP citation data set (V5 format) into a python graph structure stored in NetworkX.
    """

    def __init__(self, inputPath, outputPath):

        self.inputPath = inputPath
        self.outputPath = outputPath

        logging.setLoggerClass(ColoredLogger)
        self.logger = logging.getLogger('ArnetMinerDataImporter')

        # Get the stop words set & stemmer for text analysis
        self.stopWords = None
        with open(os.getcwd() + '/src/importer/stopWords.json') as stopWordsFile:
            self.stopWords = set(json.load(stopWordsFile))
        self.stemmer = Stemmer.Stemmer('english')

        super(ArnetMinerDataImporter, self).__init__()


    def run(self):

        try:

            self.logger.info("Reading ArnetMiner input file '%s'" % self.inputPath)
            with open(self.inputPath) as inputFile:
                inputContent = inputFile.read()

            self.logger.info("Parsing ArnetMiner input content")
            parsedData = self.parseInputContent(inputContent)

            self.logger.info("Building ArnetMiner graph data")
            graph = self.buildGraph(parsedData)

            self.logger.info("Pickling ArnetMiner graph data to file")
            with open(self.outputPath, 'w') as outputFile:
                cPickle.dump(graph, outputFile)

        except Exception, error:

            self.logger.error(error.__class__.__name__ + ": " + error.message)


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

            except KeyError, error:
                raise ArnetParseError('Failed to parse data, missing paper attribute "%s"' % error.message)

        # Check that all citations are valid
        if referencedPaperIds.difference(paperIds) != set():
            raise ArnetParseError('Failed to parse data, invalid references in found')

        outputData[currentPaper['id']] = currentPaper

        return outputData


    def buildGraph(self, parsedData):
        """
          Form the DBLP graph structure from the parsed data
        """

        graph = GraphFacade.getInstance()

        # First, build the nodes for the graph
        authors = {} # Indexed by name
        papers = {} # Indexed by paper id
        topics = {} # Indexed by keyword
        conferences = {} # Indexed by name
        citationMap = {} # Map of paper id to referenced paper ids

        # Construct everything except reference edges
        for paperId in parsedData:
            paperData = parsedData[paperId]

            paper = Paper(paperId, paperData['title'])
            citationMap[paperId] = paperData['references']

            # Create or get conference for this paper
            conferenceName = paperData['conference']
            if conferenceName not in conferences:
                conference = Conference(len(conferences), conferenceName)
                conferences[conferenceName] = conference
                graph.addNode(conference)
            else:
                conference = conferences[conferenceName]

            # Create or get authors for this paper
            paperAuthors = []
            for authorName in paperData['authors']:
                if authorName not in authors:
                    author = Author(len(authors), authorName)
                    authors[authorName] = author
                    graph.addNode(author)
                else:
                    author = authors[authorName]
                paperAuthors.append(author)

            # Extract keywords from title, and use as topics
            keywords = self.__extractKeywords(paperData['title'])
            for keyword in keywords:
                if keyword not in topics:
                    topic = Topic(len(topics), [keyword])
                    topics[keyword] = topic
                    graph.addNode(topic)
                else:
                    topic = topics[keyword]
                graph.addEdge(topic, paper, Mention())
                graph.addEdge(paper, topic, Mention())

            # Add new paper to the graph
            papers[paperId] = paper
            graph.addNode(paper)

            # Add corresponding edges in the graph
            for author in paperAuthors:
                graph.addEdge(paper, author, Authorship())
                graph.addEdge(author, paper, Authorship())
            graph.addEdge(paper, conference, Publication())
            graph.addEdge(conference, paper, Publication())

        # Add citations to the graph
        for paperId in citationMap:
            references = citationMap[paperId]
            paper = papers[paperId]
            for citedPaperId in references:
                citedPaper = papers[citedPaperId]
                graph.addEdge(paper, citedPaper, Citation())

        return graph


    def __extractKeywords(self, text):
        """
          Extracts topic keywords using lowercase, stemming, and a stop word list
        """

        keywords = set()
        words = self.stemmer.stemWords(text.lower().split(' '))
        for word in words:
            if word not in self.stopWords:
                keywords.add(word)

        return keywords
