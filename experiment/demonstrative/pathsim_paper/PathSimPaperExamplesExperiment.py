import texttable
from experiment.Experiment import Experiment
from src.model.node.dblp.Author import Author
from src.model.node.dblp.Conference import Conference
from src.model.node.dblp.Paper import Paper
from src.similarity.heterogeneous.NeighborSimStrategy import NeighborSimStrategy
from src.similarity.heterogeneous.PathSimStrategy import PathSimStrategy
from src.similarity.heterogeneous.SimRankStrategy import SimRankStrategy
from src.util.EdgeBasedMetaPathUtility import EdgeBasedMetaPathUtility
from src.util.SampleGraphUtility import SampleGraphUtility

__author__ = 'jontedesco'

class PathSimPaperExamplesExperiment(Experiment):
    """
      Experiment to test results of PathSim on examples given in PathSim paper
    """

    def outputSimilarityScores(self, authorMap, authors, strategy, strategyName):
        self.output('\n\n%s Scores (compared to Mike):' % strategyName)
        rows = [
            [author.name for author in authors],
            ['%1.2f' % strategy.findSimilarityScore(authorMap['Mike'], author) for author in authors]
        ]
        pathSimTable = texttable.Texttable()
        pathSimTable.add_rows(rows)
        self.output(pathSimTable.draw())

    def run(self):

        self.graph, authorMap, conferenceMap = SampleGraphUtility.constructPathSimExampleThree()

        # Get the nodes we care about
        conferences = [
            conferenceMap['SIGMOD'],
            conferenceMap['VLDB'],
            conferenceMap['ICDE'],
            conferenceMap['KDD']
        ]
        authors = [
            authorMap['Mike'],
            authorMap['Jim'],
            authorMap['Mary'],
            authorMap['Bob'],
            authorMap['Ann'],
        ]
        metaPathUtility = EdgeBasedMetaPathUtility()

        # Project a 2-typed heterogeneous graph over PathSim example
        self.output('\nAdjacency Matrix (Projected):')
        adjMatrixTable = texttable.Texttable()
        projectedGraph = metaPathUtility.createHeterogeneousProjection(self.graph, [Author, Paper, Conference], symmetric = True)

        rows = [['Author'] + [conference.name for conference in conferences]]
        rows += [[author.name] + [projectedGraph.getNumberOfEdges(author, conference) for conference in conferences] for author in authors]
        adjMatrixTable.add_rows(rows)
        self.output(adjMatrixTable.draw())

        # Output homogeneous simrank comparison
        homogeneousSimRankStrategy = SimRankStrategy(self.graph)
        self.outputSimilarityScores(authorMap, authors, homogeneousSimRankStrategy, 'Homogeneous SimRank')

        # Output heterogeneous simrank comparison
        heterogeneousSimRankStrategy = SimRankStrategy(projectedGraph)
        self.outputSimilarityScores(authorMap, authors, heterogeneousSimRankStrategy, 'APC Heterogeneous SimRank')

        # Output heterogeneous simrank w/ squared neighbors comparison
        def sqNeighborsNorm(graph, a, b, sim):
            aNeighbors, bNeighbors = graph.getPredecessors(a), graph.getPredecessors(b)
            return float(len(aNeighbors)**2 * len(bNeighbors)**2)
        heterogeneousSquaredSimRankStrategy = SimRankStrategy(projectedGraph, normalization=sqNeighborsNorm)
        self.outputSimilarityScores(authorMap, authors, heterogeneousSquaredSimRankStrategy, 'Squared Heterogeneous SimRank')

        # Output NeighborSim similarity scores
        neighborSimStrategy = NeighborSimStrategy(self.graph, [Author, Paper, Conference], symmetric=True)
        self.outputSimilarityScores(authorMap, authors, neighborSimStrategy, 'APC NeighborSim')

        # Output the PathSim similarity scores
        pathsimStrategy = PathSimStrategy(self.graph, [Author, Paper, Conference, Paper, Author], symmetric=True)
        self.outputSimilarityScores(authorMap, authors, pathsimStrategy, 'APCPA PathSim')


if __name__ == '__main__':
    experiment = PathSimPaperExamplesExperiment(
        None,
        'PathSim Similarity on paper examples'
    )
    experiment.start()