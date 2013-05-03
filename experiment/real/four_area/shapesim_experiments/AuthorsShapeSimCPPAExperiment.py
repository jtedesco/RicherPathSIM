import cPickle
from collections import defaultdict
import os
import operator
import texttable
from experiment.Experiment import Experiment
from experiment.real.four_area.helper.ShapeSimHelper import getShapeSimScore
from experiment.real.four_area.helper.MetaPathHelper import findMostSimilarNodes, testAuthors, \
    getMetaPathAdjacencyTensorData

__author__ = 'jontedesco'


class AuthorsShapeSimCPPAExperiment(Experiment):
    """
      Runs some experiments with ShapeSim on author similarity for the 'four area' dataset
    """

    def runFor(self, author, adjTensor, extraData, citationCounts, publicationCounts):
        print("Running for %s..." % author)

        # Find the top 10 most similar nodes to some given node
        mostSimilar, similarityScores = findMostSimilarNodes(
            adjTensor, author, extraData, method=getShapeSimScore, alpha=1.0, omit=[]
        )
        self.output('Most Similar to "%s":' % author)
        mostSimilarTable = texttable.Texttable()
        rows = [['Author', 'Score', 'Citations', 'Publications']]
        rows += [[name, score, citationCounts[name], publicationCounts[name]] for name, score in mostSimilar]
        mostSimilarTable.add_rows(rows)
        self.output(mostSimilarTable.draw())

        # Output all similarity scores
        outputPath = os.path.join(
            '../results', 'authors', 'intermediate', '%s-shapesim-cppa' % author.replace(' ', '')
        )
        cPickle.dump(similarityScores, open(outputPath, 'wb'))


def run():
    experiment = AuthorsShapeSimCPPAExperiment(
        None,
        'Most Similar CPPA ShapeSim Authors',
        outputFilePath=os.path.join('../results', 'authors', 'cppaShapeSim')
    )

    # Compute once, since these never change
    graph, nodeIndex = cPickle.load(open(os.path.join('../data', 'graphWithCitations')))
    cppaAdjTensor, extraData = getMetaPathAdjacencyTensorData(
        graph, nodeIndex, ['conference', 'paper', 'paper', 'author']
    )
    extraData['fromNodes'] = extraData['toNodes']
    extraData['fromNodesIndex'] = extraData['toNodesIndex']

    # Read paper citation counts
    paperCitationsFile = open(os.path.join('../data', 'paperCitationCounts'))
    paperCitationCounts = {}
    for line in paperCitationsFile:
        splitIndex = line.find(': ')
        count, title = int(line[:splitIndex]), line[splitIndex+2:].strip()
        paperCitationCounts[title] = int(count)

    # Compute author publication counts
    allPapers = set(nodeIndex['paper'].values())
    allAuthors = set(nodeIndex['author'].values())
    publicationCounts, citationCounts = defaultdict(int), defaultdict(int)
    for author in allAuthors:
        for node in graph.successors(author):
            if node in allPapers:
                publicationCounts[author] += 1
                citationCounts[author] += paperCitationCounts[node] if node in paperCitationCounts else 0

    # Output author citation counts
    citationCountsList = sorted(citationCounts.iteritems(), key=operator.itemgetter(1))
    citationCountsList.reverse()
    with open(os.path.join('../data', 'authorCitationCounts'), 'w') as outputFile:
        map(lambda (author, count): outputFile.write('%d: %s\n' % (int(count), author)), citationCountsList)

    # Actually run the similarity experiments
    for testAuthor in testAuthors:
        experiment.runFor(testAuthor, cppaAdjTensor, extraData, citationCounts, publicationCounts)

    return citationCounts, publicationCounts

if __name__ == '__main__': run()