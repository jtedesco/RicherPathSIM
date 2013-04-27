import numpy
import texttable
from experiment.Experiment import Experiment
from src.model.node.dblp.Author import Author
from src.model.node.dblp.Conference import Conference
from src.model.node.dblp.Paper import Paper
from src.util.EdgeBasedMetaPathUtility import EdgeBasedMetaPathUtility
from src.util.SampleGraphUtility import SampleGraphUtility

__author__ = 'jontedesco'


class SkewedCitationPublicationExampleExperiment(Experiment):
    """
      Experiment to test results of PathSim on examples given in PathSim paper
    """

    def outputSimilarityScores(self, authorMap, authors, strategy, strategyName):
        self.output('\n\n%s Scores (compared to Alice):' % strategyName)
        rows = [
            [author.name for author in authors],
            ['%1.2f' % strategy.findSimilarityScore(authorMap['Alice'], author) for author in authors]
        ]
        pathSimTable = texttable.Texttable()
        pathSimTable.add_rows(rows)
        self.output(pathSimTable.draw())

    def run(self):

        self.graph, authorMap, conference, citationsPublications = \
            SampleGraphUtility.constructSkewedCitationPublicationExample(introduceRandomness=False)

        # Get the nodes we care about
        authors = [
            authorMap['Alice'],
            authorMap['Bob'],
            authorMap['Carol'],
            authorMap['Dave']
        ]
        metaPathUtility = EdgeBasedMetaPathUtility()

        # Output adjacency matrices
        self.output('\nCPA Adjacency Matrix:')
        cpaadjMatrix, nodesIndex = metaPathUtility.getAdjacencyMatrixFromGraph(
            self.graph, [Conference, Paper, Author], project=True
        )
        adjMatrixTable = texttable.Texttable()
        rows = [['Conference'] + [author.name for author in authors]]
        rows += [[conference.name] + [cpaadjMatrix[nodesIndex[conference]][nodesIndex[author]] for author in authors]]
        adjMatrixTable.add_rows(rows)
        self.output(adjMatrixTable.draw())

        self.output('\nCitation & Publication Counts')
        adjMatrixTable = texttable.Texttable()
        rows = [['Measure'] + [author.name for author in authors]]
        rows += [['Citations'] + [citationsPublications[author][0] for author in authors]]
        rows += [['Publications'] + [citationsPublications[author][1] for author in authors]]
        adjMatrixTable.add_rows(rows)
        self.output(adjMatrixTable.draw())


if __name__ == '__main__':
    experiment = SkewedCitationPublicationExampleExperiment(
        None,
        'Skewed citation publication count example'
    )
    experiment.start()