from Stemmer import Stemmer
import json
import os
import re
import cPickle
from networkx import MultiDiGraph
import sys

__author__ = 'jontedesco'

# Regex for stripping non-visible characters
control_chars = ''.join(map(unichr, list(range(0, 32)) + list(range(127, 160))))
control_characters_regex = re.compile('[%s]' % re.escape(control_chars))

# HACK: Get the absolute project root, assuming top-level dir is named 'RicherPathSIM'
project_root = str(os.getcwd())
project_root = project_root[:project_root.find('RicherPathSIM') + len('RicherPathSIM')]

# Get the stop words set & stemmer for text analysis
stop_words = None
with open(os.path.join(project_root, 'src', 'importer', 'stopWords.json')) as stop_words_file:
    stop_words = set(json.load(stop_words_file))
stemmer = Stemmer('english')
non_ascii_regex = re.compile('\W')


def __get_terms_from_string(string):

    def is_term(token, string):
        if len(token) < 3 <= len(string):
            return False
        if token in stop_words:
            return False
        return True

    string = string.lower()
    tokens = non_ascii_regex.sub(' ', string).strip().split()
    terms = [stemmer.stemWord(token) for token in tokens if is_term(token, string)]

    return terms


def __remove_control_characters(string):
    string = string.strip('\xef\xbb\xbf')
    return control_characters_regex.sub('', string)


def __papers_from_file(input_file, skipped_paper_indices, invalid_paper_indices):
    """
      Generator function over papers (gets data from the next entry)
    """

    # Tokens for parsing
    title_token = '#*'
    author_token = '#@'
    conf_token = '#conf'
    index_token = '#index'
    citation_count_token = '#citation'

    # Predicates for error checking
    none_none = lambda *items: all([item is not None for item in items])
    all_none = lambda *items: all([item is None for item in items])

    # Basics stats for the number of papers processed
    skipped_missing_conference = 0
    skipped_bad_title = 0
    invalid = 0
    successful = 0
    total_papers = 0

    # Next entry data
    title = None
    authors = None
    conference = None
    index = None
    citation_count = None
    terms = None

    for line in input_file:
        line = line.strip()

        # Parse entry, asserting that entries appear in title -> authors -> conference order
        if line.startswith(title_token):
            assert all_none(title, authors, conference, terms, index, citation_count)
            title = line[len(title_token):].strip('.')
            terms = __get_terms_from_string(title)

        elif line.startswith(author_token):
            assert none_none(title, terms) and all_none(authors, conference, index, citation_count)
            authors = [author.strip() for author in line[len(author_token):].split(',')]

        elif line.startswith(conf_token):
            assert none_none(title, terms, authors) and all_none(conference, index, citation_count)
            conference = line[len(conf_token):]

        elif line.startswith(citation_count_token):
            assert none_none(title, terms, authors, conference) and all_none(citation_count, index)
            citation_count = max(int(line[len(citation_count_token):]), 0)

        elif line.startswith(index_token):
            assert none_none(title, terms, authors, conference, citation_count) and all_none(index)
            index = int(line[len(index_token):])

        # We've reached the end of the entry
        elif len(line) == 0:
            total_papers += 1

            # Only output if:
            #   (1) data is all not None
            #   (2) title, authors, and conference are valid (non-empty)
            #   (3) index are citation count were found
            if all((title, authors, conference)) and index is not None and citation_count is not None:
                successful += 1
                yield title, authors, conference, terms, citation_count, index
            else:
                if len(conference) == 0:
                    skipped_missing_conference += 1
                    skipped_paper_indices.add(index)
                else:
                    invalid += 1
                    invalid_paper_indices.add(index)

            title = None
            authors = None
            conference = None
            terms = None
            index = None
            citation_count = None

    # Basic statistics about cleanliness of data
    successful_percent = 100.0 * (float(successful) / total_papers)
    skipped_bad_title_percent = 100.0 * (float(skipped_bad_title) / total_papers)
    skipped_missing_conference_percent = 100.0 * (float(skipped_missing_conference) / total_papers)
    invalid_percent = 100.0 * (float(invalid) / total_papers)
    print "\n\nTotal Papers: %d" % total_papers
    print "  Added (Successful): %d (%2.2f%%)", (successful, successful_percent)
    print "  Ignored (Bad Title): %d (%2.2f%%)" % (skipped_bad_title, skipped_bad_title_percent)
    print "  Skipped (Missing Conference): %d (%2.2f%%)" % (
        skipped_missing_conference, skipped_missing_conference_percent
    )
    print "  Invalid (Unknown): %d (%2.2f%%)", (invalid, invalid_percent)


def __citations_from_file(input_file):
    """
      Generator function that outputs the paper title, index, and citations for each entry
    """

    # Tokens for parsing
    title_token = '#*'
    index_token = '#index'
    citation_token = '#%'

    # Predicates for error checking
    none_none = lambda *items: all([item is not None for item in items])
    all_none = lambda *items: all([item is None for item in items])

    # Next entry data
    title = None
    index = None
    citations = []

    # Basic stats
    with_citations = 0
    without_citations = 0
    total_papers = 0

    for line in input_file:
        line = line.strip()

        # Parse entry, enforcing that data appears in title -> index -> citations order
        if line.startswith(title_token):
            assert all_none(title, index) and len(citations) == 0
            title = line[len(title_token):].strip('.')

        elif line.startswith(index_token):
            assert none_none(title) and all_none(index) and len(citations) == 0
            index = int(line[len(index_token):])

        elif line.startswith(citation_token):
            assert none_none(title, index)
            new_citation_id = int(line[len(citation_token):])
            assert new_citation_id >= 0
            citations.append(new_citation_id)

        elif len(line) == 0:
            total_papers += 1

            # Yield this entry if it has any citations,
            if none_none(title, index):
                if len(citations) > 0:
                    with_citations += 1
                    yield title, index, citations
                else:
                    without_citations += 1

            title = None
            index = None
            citations = []

    # Output some basic statistics about papers with/without citations
    with_citations_percent = 100.0 * (float(with_citations) / total_papers)
    without_citations_percent = 100.0 * (float(without_citations) / total_papers)
    print "\n\nTotal Papers: %d" % total_papers
    print "  With References: %d (%2.2f%%)\n  Without References: %d (%2.2f%%)" % (
        with_citations, with_citations_percent, without_citations, without_citations_percent
    )


def parse_arnetminer_dataset():
    """
      Parse the four area dataset, and use only barebones structures to keep everything efficient.

        Skips papers that:
            (1)

        The final parsed network
    """

    input_file = open(os.path.join(project_root, 'data', 'DBLP-citation-Feb21.txt'))
    graph = MultiDiGraph()

    # Sets for authors, papers, conferences, and terms found so far
    # TODO: Reconsider more efficient approach
    index_to_paper_id_map = {}
    citation_count_map = {}
    index_set = set()

    beginning = input_file.tell()

    print "Parsing nodes for graph..."

    # Counts for statistics
    VALID_PAPERS = 1566322  # 99.62% of total papers in DBLP dataset
    papers_processed = 0
    skipped_paper_indices = set()
    invalid_paper_indices = set()

    # Add each paper to graph (adding missing associated terms, authors, and conferences)
    for title, authors, conference, terms, citation_count, index in \
            __papers_from_file(input_file, skipped_paper_indices, invalid_paper_indices):

        # Check that index is unique, and record it
        assert index not in index_set
        index_set.add(index)

        # Create unique identifier with paper index & title
        paper_id = '%d----%s' % (index, title)
        citation_count_map[paper_id] = citation_count
        index_to_paper_id_map[index] = paper_id

        # Add symmetric edges & nodes (if they don't already exist in the network)
        for author in authors:
            graph.add_edges_from([(author, paper_id), (paper_id, author)])
        graph.add_edges_from([(conference, paper_id), (paper_id, conference)])
        for term in terms:
            graph.add_edges_from([(term, paper_id), (paper_id, term)])

        # Output progress
        papers_processed += 1
        sys.stdout.write("\r Processed %d / %d papers..." % (papers_processed, VALID_PAPERS))

    # Rewind file
    input_file.seek(beginning)

    print "Parsing citations for graph..."

    # Counts for statistics
    papers_processed = 0
    successful_citations = 0
    omitted_paper_citations = 0
    invalid_paper_citations = 0
    invalid_citations = 0

    # Add citations to the graph
    for title, index, citations in __citations_from_file(input_file):
        citingId = '%d----%s' % (index, title)
        for citation_index in citations:

            # Add citation edge if it was found
            if citation_index in index_to_paper_id_map:
                successful_citations += 1
                graph.add_edge(citingId, index_to_paper_id_map[citation_index])

            # Tally missing citation appropriately
            elif citation_index in skipped_paper_indices:
                omitted_paper_citations += 1
            elif citation_index in invalid_paper_indices:
                invalid_paper_citations += 1
            else:
                print "\nCitation '%d' not found for '%s'" % (citation_index, title)
                invalid_citations += 1

        # Output progress
        papers_processed += 1
        sys.stdout.write("\r Processed Citations for %d / %d papers..." % (papers_processed, VALID_PAPERS))

    # Basic statistics about cleanliness of citations
    total_citations = invalid_citations + successful_citations
    successful_citations_percent = 100 * float(successful_citations) / total_citations
    omitted_paper_citations_percent = 100 * float(omitted_paper_citations) / total_citations
    invalid_paper_citations_percent = 100 * float(invalid_paper_citations) / total_citations
    invalid_citations_percent = 100 * float(invalid_citations) / total_citations
    print "\n\nTotal Citations: %d" % total_citations
    print "  Citations Added (Successful): %d (%2.2f%%)" % (successful_citations, successful_citations_percent)
    print "  Citations Skipped (Skipped Paper): %d (%2.2f%%)" % (
        omitted_paper_citations, omitted_paper_citations_percent
    )
    print "  Citations Skipped (Invalid Paper): %d (%2.2f%%)" % (
        invalid_paper_citations, invalid_paper_citations_percent
    )
    print "  Citations Invalid (Unknown): %d (%2.2f%%)" % (invalid_citations, invalid_citations_percent)

    return graph


def constructGraphAndDumpToFile():

    # Parse 4-area dataset graph & dump it to disk
    graph = parse_arnetminer_dataset()

    cPickle.dump(graph, open(os.path.join('data', 'arnetminerWithCitations'), 'w'))


# When run as script, runs through pathsim papers example experiment
if __name__ == '__main__':
    constructGraphAndDumpToFile()
