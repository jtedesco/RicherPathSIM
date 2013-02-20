from Stemmer import Stemmer
import json
import os
import re
import cPickle
from networkx import MultiDiGraph
import sys

__author__ = 'jontedesco'

# Regex for stripping non-visible characters
controlChars = ''.join(map(unichr, list(range(0,32)) + list(range(127,160))))
controlCharactersRegex = re.compile('[%s]' % re.escape(controlChars))

# HACK: Get the absolute project root, assuming top-level dir is named 'RicherPathSIM'
projectRoot = str(os.getcwd())
projectRoot = projectRoot[:projectRoot.find('RicherPathSIM') + len('RicherPathSIM')]

# Get the stop words set & stemmer for text analysis
stopWords = None
with open(os.path.join(projectRoot, 'src', 'importer', 'stopWords.json')) as stopWordsFile:
    stopWords = set(json.load(stopWordsFile))
stemmer = Stemmer('english')
nonAsciiRegex = re.compile('\W')

def __getTermsFromString(string):

    def isTerm(token, string):
        if len(token) < 3 <= len(string): return False
        if token in stopWords: return False
        return True

    string = string.lower()
    tokens = nonAsciiRegex.sub(' ', string).strip().split()
    terms = [stemmer.stemWord(token) for token in tokens if isTerm(token, string)]

    return terms


def __removeControlCharacters(string):
    string = string.strip('\xef\xbb\xbf')
    return controlCharactersRegex.sub('', string)


def __papersFromFile(file, skippedPaperIndices, invalidPaperIndices):
    """
      Generator function over papers (gets data from the next entry)
    """

    # Tokens for parsing
    titleToken = '#*'
    authorToken = '#@'
    confToken = '#conf'
    indexToken = '#index'
    citationCountToken = '#citation'

    # Predicates for error checking
    noneNone = lambda *items: all([item is not None for item in items])
    allNone = lambda *items: all([item is None for item in items])

    # Basics stats for the number of papers processed
    skippedMissingConference = 0
    skippedBadTitle = 0
    invalid = 0
    successful = 0
    totalPapers = 0

    # Next entry data
    title = None
    authors = None
    conference = None
    index = None
    citationCount = None
    terms = None

    for line in file:
        line = line.strip()

        # Parse entry, asserting that entries appear in title -> authors -> conference order
        if line.startswith(titleToken):
            assert allNone(title, authors, conference, terms, index, citationCount)
            title = line[len(titleToken):].strip('.')
            terms = __getTermsFromString(title)

        elif line.startswith(authorToken):
            assert noneNone(title, terms) and allNone(authors, conference, index, citationCount)
            authors = [author.strip() for author in line[len(authorToken):].split(',')]

        elif line.startswith(confToken):
            assert noneNone(title, terms, authors) and allNone(conference, index, citationCount)
            conference = line[len(confToken):]

        elif line.startswith(citationCountToken):
            assert noneNone(title, terms, authors, conference) and allNone(citationCount, index)
            citationCount = max(int(line[len(citationCountToken):]), 0)

        elif line.startswith(indexToken):
            assert noneNone(title, terms, authors, conference, citationCount) and allNone(index)
            index = int(line[len(indexToken):])

        # We've reached the end of the entry
        elif len(line) == 0:
            totalPapers += 1

            # Only output if:
            #   (1) data is all not None
            #   (2) title, authors, and conference are valid (non-empty)
            #   (3) index are citation count were found
            if all((title, authors, conference)) and index is not None and citationCount is not None:
                successful += 1
                yield title, authors, conference, terms, citationCount, index
            else:
                if len(conference) == 0:
                    skippedMissingConference += 1
                    skippedPaperIndices.add(index)
                else:
                    invalid += 1
                    invalidPaperIndices.add(index)

            title = None
            authors = None
            conference = None
            terms = None
            index = None
            citationCount = None

    # Basic statistics about cleanliness of data
    successfulPercent = 100.0 * (float(successful) / totalPapers)
    skippedBadTitlePercent = 100.0 * (float(skippedBadTitle) / totalPapers)
    skippedMissingConferencePercent = 100.0 * (float(skippedMissingConference) / totalPapers)
    invalidPercent = 100.0 * (float(invalid) / totalPapers)
    print "\n\nTotal Papers: %d" % totalPapers
    print "  Added (Successful): %d (%2.2f%%)", (successful, successfulPercent)
    print "  Ignored (Bad Title): %d (%2.2f%%)" % (skippedBadTitle, skippedBadTitlePercent)
    print "  Skipped (Missing Conference): %d (%2.2f%%)" % (skippedMissingConference, skippedMissingConferencePercent)
    print "  Invalid (Unknown): %d (%2.2f%%)", (invalid, invalidPercent)


def __citationsFromFile(file):
    """
      Generator function that outputs the paper title, index, and citations for each entry
    """

    # Tokens for parsing
    titleToken = '#*'
    indexToken = '#index'
    citationToken = '#%'

    # Predicates for error checking
    noneNone = lambda *items: all([item is not None for item in items])
    allNone = lambda *items: all([item is None for item in items])

    # Next entry data
    title = None
    index = None
    citations = []

    # Basic stats
    withCitations = 0
    withoutCitations = 0
    totalPapers = 0

    for line in file:
        line = line.strip()

        # Parse entry, enforcing that data appears in title -> index -> citations order
        if line.startswith(titleToken):
            assert allNone(title, index) and len(citations) == 0
            title = line[len(titleToken):].strip('.')

        elif line.startswith(indexToken):
            assert noneNone(title) and allNone(index) and len(citations) == 0
            index = int(line[len(indexToken):])

        elif line.startswith(citationToken):
            assert noneNone(title, index)
            newCitationId = int(line[len(citationToken):])
            assert newCitationId >= 0
            citations.append(newCitationId)

        elif len(line) == 0:
            totalPapers += 1

            # Yield this entry if it has any citations,
            if noneNone(title, index):
                if len(citations) > 0:
                    withCitations += 1
                    yield title, index, citations
                else:
                    withoutCitations += 1

            title = None
            index = None
            citations = []

    # Output some basic statistics about papers with/without citations
    withCitationsPercent = 100.0 * (float(withCitations) / totalPapers)
    withoutCitationsPercent = 100.0 * (float(withoutCitations) / totalPapers)
    print "\n\nTotal Papers: %d" % totalPapers
    print "  With References: %d (%2.2f%%)\n  Without References: %d (%2.2f%%)" % (
        withCitations, withCitationsPercent, withoutCitations, withoutCitationsPercent
    )


def parseArnetminerDataset():
    """
      Parse the four area dataset, and use only barebones structures to keep everything efficient.

        Skips papers that:
            (1)

        The final parsed network
    """

    inputFile = open(os.path.join(projectRoot, 'data','DBLP-citation-Feb21.txt'))
    graph = MultiDiGraph()

    # Sets for authors, papers, conferences, and terms found so far
    indexToPaperIdMap = {}
    citationCountMap = {}
    indexSet = set()

    beginning = inputFile.tell()

    print "Parsing nodes for graph..."

    # Counts for statistics
    VALID_PAPERS = 1566322 # 99.62% of total papers in DBLP dataset
    papersProcessed = 0
    skippedPaperIndices = set()
    invalidPaperIndices = set()

    # Add each paper to graph (adding missing associated terms, authors, and conferences)
    for title, authors, conference, terms, citationCount, index in __papersFromFile(inputFile, skippedPaperIndices, invalidPaperIndices):

        # Check that index is unique, and record it
        assert index not in indexSet
        indexSet.add(index)

        # Create unique identifier with paper index & title
        paperId = '%d----%s' % (index, title)
        citationCountMap[paperId] = citationCount
        indexToPaperIdMap[index] = paperId

        # Add symmetric edges & nodes (if they don't already exist in the network)
        for author in authors:
            graph.add_edges_from([(author, paperId), (paperId, author)])
        graph.add_edges_from([(conference, paperId), (paperId, conference)])
        for term in terms:
            graph.add_edges_from([(term, paperId), (paperId, term)])

        # Output progress
        papersProcessed += 1
        sys.stdout.write("\r Processed %d / %d papers..." % (papersProcessed, VALID_PAPERS))

    # Rewind file
    inputFile.seek(beginning)

    print "Parsing citations for graph..."

    # Counts for statistics
    papersProcessed = 0
    successfulCitations = 0
    omittedPaperCitations = 0
    invalidPaperCitations = 0
    invalidCitations = 0

    # Add citations to the graph
    for title, index, citations in __citationsFromFile(inputFile):
        citingId = '%d----%s' % (index, title)
        for citationIndex in citations:

            # Add citation edge if it was found
            if citationIndex in indexToPaperIdMap:
                successfulCitations += 1
                graph.add_edge(citingId, indexToPaperIdMap[citationIndex])

            # Tally missing citation appropriately
            elif citationIndex in skippedPaperIndices:
                omittedPaperCitations += 1
            elif citationIndex in invalidPaperIndices:
                invalidPaperCitations += 1
            else:
                print "\nCitation '%d' not found for '%s'" % (citationIndex, title)
                invalidCitations += 1

        # Output progress
        papersProcessed += 1
        sys.stdout.write("\r Processed Citations for %d / %d papers..." % (papersProcessed, VALID_PAPERS))

    # Basic statistics about cleanliness of citations
    totalCitations = invalidCitations + successfulCitations
    successfulCitationsPercent = 100 * float(successfulCitations) / totalCitations
    omittedPaperCitationsPercent = 100 * float(omittedPaperCitations) / totalCitations
    invalidPaperCitationsPercent = 100 * float(invalidPaperCitations) / totalCitations
    invalidCitationsPercent = 100 * float(invalidCitations) / totalCitations
    print "\n\nTotal Citations: %d", totalCitations
    print "  Citations Added (Successful): %d (%2.2f%%)" % (successfulCitations, successfulCitationsPercent)
    print "  Citations Skipped (Skipped Paper): %d (%2.2f%%)" % (omittedPaperCitations, omittedPaperCitationsPercent)
    print "  Citations Skipped (Invalid Paper): %d (%2.2f%%)" % (invalidPaperCitations, invalidPaperCitationsPercent)
    print "  Citations Invalid (Unknown): %d (%2.2f%%)" % (invalidCitations, invalidCitationsPercent)

    return graph


def constructGraphAndDumpToFile():

    # Parse 4-area dataset graph & dump it to disk
    graph = parseArnetminerDataset()

    cPickle.dump(graph, open(os.path.join('data', 'arnetminerWithCitations'), 'w'))

# When run as script, runs through pathsim papers example experiment
if __name__ == '__main__':
    constructGraphAndDumpToFile()
