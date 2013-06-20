import texttable
from experiment.Experiment import Experiment
from src.model.node.dblp.Author import Author
from src.model.node.dblp.Conference import Conference
from src.model.node.dblp.Paper import Paper
from src.similarity.AggregateSimilarityStrategy import AggregateSimilarityStrategy
from src.similarity.heterogeneous.NeighborSimStrategy import NeighborSimStrategy
from src.similarity.heterogeneous.RecursivePathSimStrategy import RecursivePathSimStrategy
from src.similarity.heterogeneous.path_shape_count.FlattenedMatrixStrategy import FlattenedMatrixStrategy
from src.similarity.heterogeneous.path_shape_count.VectorProductStrategy import VectorProductStrategy
from src.util.EdgeBasedMetaPathUtility import EdgeBasedMetaPathUtility
from src.util.SampleGraphUtility import SampleGraphUtility

__author__ = 'jontedesco'


class SkewedCitationPublicationWeightedExampleExperiment(Experiment):
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

        citationsPublications = {
            'Alice': (100, 10),
            'Bob': (80, 10),
            'Carol': (100, 100),
            'Dave': (10, 10),
            'Ed': (20, 5)

        }

        self.graph, authorMap, conference, citationsPublications = \
            SampleGraphUtility.constructSkewedCitationPublicationExample(
                introduceRandomness=False, citationsPublicationsParameter=citationsPublications
            )

        # Get the nodes we care about
        authors = [
            authorMap['Alice'],
            authorMap['Bob'],
            authorMap['Carol'],
            authorMap['Dave'],
            authorMap['Ed']
        ]

        # Total citation & publication counts
        self.output('\nCitation & Publication Counts')
        adjMatrixTable = texttable.Texttable()
        rows = [['Measure'] + [author.name for author in authors]]
        rows += [['Citations'] + [citationsPublications[author][0] for author in authors]]
        rows += [['Publications'] + [citationsPublications[author][1] for author in authors]]
        adjMatrixTable.add_rows(rows)
        self.output(adjMatrixTable.draw())

        # Output PathSim similarity scores
        pathSimStrategyPubs = NeighborSimStrategy(self.graph, [Conference, Paper, Author], symmetric=True)
        self.outputSimilarityScores(authorMap, authors, pathSimStrategyPubs, 'APCPA PathSim')
        pathSimStrategyCits = NeighborSimStrategy(self.graph, [Conference, Paper, Paper, Author])
        self.outputSimilarityScores(authorMap, authors, pathSimStrategyCits, 'APPCPPA PathSim')
        for w1, w2 in [(0.5, 0.5), (0.6, 0.4), (0.4, 0.6)]:
            combinedPathSimStrategy = AggregateSimilarityStrategy(
                self.graph, [pathSimStrategyPubs, pathSimStrategyCits], [w1, w2]
            )
            self.outputSimilarityScores(
                authorMap, authors, combinedPathSimStrategy, 'APCPA-APPCPPAA Pathsim (%1.1f,%1.1f)' % (w1, w2)
            )

        # Output ShapeSim strategy
        w = 1.0
        neighborPathShapeStrategy = VectorProductStrategy(
            self.graph, weight=w, omit=[], metaPath=[Conference, Paper, Paper, Author], symmetric=True
        )
        strategyTitle = 'APPCPPA %s ShapeSim (%1.2f weight)' % ('VectorProduct', w)
        self.outputSimilarityScores(authorMap, authors, neighborPathShapeStrategy, strategyTitle)

if __name__ == '__main__':
    experiment = SkewedCitationPublicationWeightedExampleExperiment(
        None,
        'Skewed citation publication count example'
    )
    experiment.start()