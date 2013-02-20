from Stemmer import Stemmer
import json
import os
import re
import cPickle
from networkx import MultiDiGraph

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

def parseArnetminerDataset():
    """
      Parse the four area dataset, and use only barebones structures to keep everything efficient
    """

    inputFile = open(os.path.join(projectRoot, 'data','DBLP-citation-Feb21.txt'))
    graph = MultiDiGraph()

    # Sets for authors, papers, conferences, and terms found so far
    paperTitleIndex = {}
    citationCountMap = {}
    indexSet = set()

    def papersFromFile(file):
        """
          Generator function over papers (gets the next set of title, terms, author, and conference)
        """

        title = None
        authors = None
        conference = None
        index = None
        citationCount = None
        terms = None

        titleToken = '#*'
        authorToken = '#@'
        confToken = '#conf'
        indexToken = '#index'
        citationToken = '#citation'

        skipped = 0
        ignored = 0
        invalid = 0
        processed = 0
        totalPapers = 0

        # Predicates for error checking
        noneNone = lambda *items: all([item is not None for item in items])
        allNone = lambda *items: all([item is None for item in items])

        for line in file:
            line = line.strip() # Throw an exception on non-ascii text

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

            elif line.startswith(citationToken):
                assert noneNone(title, terms, authors, conference) and allNone(citationCount, index)
                citationCount = max(int(line[len(citationToken):]), 0)

            elif line.startswith(indexToken):
                assert noneNone(title, terms, authors, conference, citationCount) and allNone(index)
                index = max(int(line[len(indexToken):]), 0)

            # We've reached the end of the entry
            elif len(line) == 0:
                totalPapers += 1

                # Only output if all data is good (is not None)
                if all((title, authors, conference, terms, index, citationCount)):
                    processed += 1
                    yield title, authors, conference, terms, citationCount, index
                else:
                    if len(conference) == 0:
                        skipped += 1
                    elif len(title) >= 3 and len(terms) == 0:
                        ignored += 1
                    else:
                        invalid += 1

                title = None
                authors = None
                conference = None
                terms = None
                index = None
                citationCount = None

        # Basic statistics about Cleanliness of data
        print("Papers processed: %d (%2.2f%%)" % (processed, 100.0 * (float(processed) / totalPapers)))
        print("Papers ignored (bad titles): %d (%2.2f%%)" % (ignored, 100.0 * (float(ignored) / totalPapers)))
        print("Papers skipped: %d (%2.2f%%)" % (skipped, 100.0 * (float(skipped) / totalPapers)))
        print("Papers invalid: %d (%2.2f%%)" % (invalid, 100.0 * (float(invalid) / totalPapers)))


    # Add each paper to graph (adding missing associated terms, authors, and conferences)
    for paper, authors, conference, terms, citationCount, index in papersFromFile(inputFile):

        # Check that index & title are unique, and record their occurrence
        assert paper not in paperTitleIndex
        assert index not in indexSet
        paperTitleIndex[paper] = index
        indexSet.add(index)

        citationCountMap[paper] = citationCount

        # Add symmetric edges & nodes (if they don't already exist in the network)
        for author in authors:
            graph.add_edges_from([(author, paper), (paper, author)])
        graph.add_edges_from([(conference, paper), (paper, conference)])
        for term in terms:
            graph.add_edges_from([(term, paper), (paper, term)])

    return graph

def constructGraphAndDumpToFile():

    # Parse 4-area dataset graph & dump it to disk
    graph, nodeIndex = parseArnetminerDataset()

    cPickle.dump((graph, nodeIndex), open(os.path.join('data', 'graphWithoutCitations'), 'w'))

# When run as script, runs through pathsim papers example experiment
if __name__ == '__main__':
    constructGraphAndDumpToFile()
