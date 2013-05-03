import cPickle
import os
import texttable
from experiment.Experiment import Experiment
from experiment.real.four_area.helper.PathSimHelper import getNeighborSimScore
from experiment.real.four_area.helper.MetaPathHelper import findMostSimilarNodes, testConferences, getMetaPathAdjacencyData

__author__ = 'jontedesco'


class ConferencesPathSimTPPCExperiment(Experiment):
    """
      Runs some experiments with NeighborSim on conference similarity for the 'four area' dataset
    """

    def runFor(self, conference, adjTensor, extraData, confPublications, confCitations):
        print("Running for %s..." % conference)

        # Find the top 10 most similar nodes to some given node
        mostSimilar, similarityScores = findMostSimilarNodes(
            adjTensor, conference, extraData, method=getNeighborSimScore
        )
        self.output('Most Similar to "%s":' % conference)
        mostSimilarTable = texttable.Texttable()
        rows = [['Conference', 'Score', 'Publications', 'Citations', 'Average Citation Per Paper']]
        rows += [[name, score, confPublications[name], confCitations[name],
                  (float(confCitations[name]) / confPublications[name])] for name, score in mostSimilar]
        mostSimilarTable.add_rows(rows)
        self.output(mostSimilarTable.draw())

        # Output all similarity scores
        outputPath = os.path.join(
            '..', '..', 'results', 'conferences', 'intermediate', '%s-neighborsim-tppc' % conference.replace(' ', '')
        )
        cPickle.dump(similarityScores, open(outputPath, 'wb'))


def run():
    experiment = ConferencesPathSimTPPCExperiment(
        None,
        'Most Similar TPPC NeighborSim Conferences',
        outputFilePath=os.path.join('..', '..', 'results', 'conferences', 'tppcNeighborSim')
    )

    # Compute once, since these never change
    graph, nodeIndex = cPickle.load(open(os.path.join('..', '..', 'data', 'graphWithCitations')))
    cppaAdjMatrix, extraData = getMetaPathAdjacencyData(
        graph, nodeIndex, ['term', 'paper', 'paper', 'conference']
    )
    extraData['fromNodes'] = extraData['toNodes']
    extraData['fromNodesIndex'] = extraData['toNodesIndex']

    confPublications, confCitations = cPickle.load(open(os.path.join('..', '..', 'data', 'conferenceStats')))

    # Actually run the similarity experiments
    for testConference in testConferences:
        experiment.runFor(testConference, cppaAdjMatrix, extraData, confPublications, confCitations)

if __name__ == '__main__': run()