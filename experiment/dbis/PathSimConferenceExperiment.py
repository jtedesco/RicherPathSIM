import os
import texttable
from experiment.Experiment import Experiment
from experiment.helper.LabeledExperimentHelper import LabeledExperimentHelper
from experiment.measure.CumulativeGainMeasures import CumulativeGainMeasures
from src.model.node.dblp.Author import Author
from src.model.node.dblp.Conference import Conference
from src.model.node.dblp.Paper import Paper
from src.similarity.heterogeneous.PathSimStrategy import PathSimStrategy

__author__ = 'jontedesco'

class PathSimConferenceExperiment(Experiment):
    """
      Experiment that tests the overall performance of PathSim using conference queries & relevance labels
    """

    def run(self):

        strategy = PathSimStrategy(self.graph, [Conference, Paper, Author, Paper, Conference], True)
        experimentHelper = LabeledExperimentHelper(os.path.join('data', 'dbis', 'query_label', 'PathSim'))
        conferenceQueryNames = [
            'SIGMOD Conference',
            'VLDB',
            'ICDE',
            'PODS',
            'EDBT',
            'DASFAA',
            'KDD',
            'ICDM',
            'PKDD',
            'SDM',
            'PAKDD',
            'WWW',
            'SIGIR',
            'TREC',
            'APWeb'
        ]

        for conferenceQueryName in conferenceQueryNames:
            conferences = experimentHelper.getNodesByAttribute(self.graph, 'name', conferenceQueryName)
            assert(len(conferences) == 1)
            target = list(conferences)[0]
            number = 10

            # Output the top ten most similar conferences on the CPAPC meta path
            self.output('\n\nTop Ten Similar Conferences to %s (CPAPC meta path):' % conferenceQueryName)
            mostSimilarNodes = strategy.findMostSimilarNodes(target, number)
            apaPathTable = texttable.Texttable()
            headerRow = [['Rank', 'Conference', 'Relevance']]
            dataRows = [[i + 1, mostSimilarNodes[i].name, experimentHelper.getLabelForNode(target, mostSimilarNodes[i])] for i in xrange(0, number)]
            apaPathTable.add_rows(headerRow + dataRows)
            self.output(apaPathTable.draw())

            # Output the nDCG for these results
            self.output('%1.3f' % CumulativeGainMeasures.normalizedDiscountedCumulativeGain(target, mostSimilarNodes, experimentHelper.labelDictionary))

if __name__ == '__main__':
    experiment = PathSimConferenceExperiment(
        os.path.join('graphs', 'dbis'),
        'Conference PathSim Similarity on DBIS dataset'
    )
    experiment.start()
