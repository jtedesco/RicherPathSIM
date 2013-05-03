import cPickle
import os
import texttable
from experiment.Experiment import Experiment
from experiment.real.four_area.helper.ShapeSimHelper import getShapeSimScore
from experiment.real.four_area.helper.MetaPathHelper import findMostSimilarNodes, getMetaPathAdjacencyTensorData, \
    testConferences

__author__ = 'jontedesco'


class ConferencesShapeSimTPPCExperiment(Experiment):
    """
      Runs some experiments with ShapeSim on conference similarity for the 'four area' dataset
    """

    def runFor(self, conference, adjTensor, extraData):
        print("Running for %s..." % conference)

        # Find the top 10 most similar nodes to some given node
        mostSimilar, similarityScores = findMostSimilarNodes(
            adjTensor, conference, extraData, method=getShapeSimScore, alpha=1.0, omit=[]
        )
        self.output('Most Similar to "%s":' % conference)
        mostSimilarTable = texttable.Texttable()
        rows = [['Conference', 'Score']]
        rows += [[name, score] for name, score in mostSimilar]
        mostSimilarTable.add_rows(rows)
        self.output(mostSimilarTable.draw())

        # Output all similarity scores
        outputPath = os.path.join(
            '../results', 'conferences', 'intermediate', '%s-shapesim-tppc' % conference.replace(' ', '')
        )
        cPickle.dump(similarityScores, open(outputPath, 'wb'))


def run():
    experiment = ConferencesShapeSimTPPCExperiment(
        None,
        'Most Similar TPPC ShapeSim Conferences',
        outputFilePath=os.path.join('../results', 'conferences', 'tppcShapeSim')
    )

    # Compute once, since these never change
    graph, nodeIndex = cPickle.load(open(os.path.join('../data', 'graphWithCitations')))
    cppaAdjTensor, extraData = getMetaPathAdjacencyTensorData(
        graph, nodeIndex, ['term', 'paper', 'paper', 'conference']
    )
    extraData['fromNodes'] = extraData['toNodes']
    extraData['fromNodesIndex'] = extraData['toNodesIndex']

    # Actually run the similarity experiments
    for testConference in testConferences:
        experiment.runFor(testConference, cppaAdjTensor, extraData)

if __name__ == '__main__': run()