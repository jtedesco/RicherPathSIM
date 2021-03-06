import cPickle
import os
import texttable
from experiment.Experiment import Experiment
from experiment.real.four_area.helper.ShapeSimHelper import getShapeSimScore
from experiment.real.four_area.helper.MetaPathHelper import findMostSimilarNodes, testAuthors, \
    getMetaPathAdjacencyTensorData

__author__ = 'jontedesco'


class AuthorsShapeSimCPPARelativePartialExperiment(Experiment):
    """
      Runs some experiments with ShapeSim on author similarity for the 'four area' dataset, using relative weights
    """

    def runFor(self, author, adjTensor, extraData, citationCounts, publicationCounts):
        print("Running for %s..." % author)

        # Find the top 10 most similar nodes to some given node
        mostSimilar, similarityScores = findMostSimilarNodes(
            adjTensor, author, extraData, method=getShapeSimScore, alpha=0.5, omit=[0]
        )
        self.output('Most Similar to "%s":' % author)
        mostSimilarTable = texttable.Texttable()
        rows = [['Author', 'Score', 'Citations', 'Publications']]
        rows += [[name, score, citationCounts[name], publicationCounts[name]] for name, score in mostSimilar]
        mostSimilarTable.add_rows(rows)
        self.output(mostSimilarTable.draw())

        # Output all similarity scores
        outputPath = os.path.join(
            '../results', 'authors', 'intermediate', '%s-shapesim-cppa-relativepartial' % author.replace(' ', '')
        )
        cPickle.dump(similarityScores, open(outputPath, 'wb'))


def run(citationCounts, publicationCounts):
    experiment = AuthorsShapeSimCPPARelativePartialExperiment(
        None,
        'Most Similar CPPA ShapeSim Authors lambda=0.5',
        outputFilePath=os.path.join('../results', 'authors', 'cppaShapeSim-RelativePartial')
    )

    # Compute once, since these never change
    graph, nodeIndex = cPickle.load(open(os.path.join('../data', 'graphWithCitations')))
    cppaAdjTensor, extraData = getMetaPathAdjacencyTensorData(
        graph, nodeIndex, ['conference', 'paper', 'paper', 'author']
    )
    extraData['fromNodes'] = extraData['toNodes']
    extraData['fromNodesIndex'] = extraData['toNodesIndex']

    for testAuthor in testAuthors:
        experiment.runFor(testAuthor, cppaAdjTensor, extraData, citationCounts, publicationCounts)