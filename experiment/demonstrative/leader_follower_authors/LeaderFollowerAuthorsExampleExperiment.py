from src.similarity.AggregateSimilarityStrategy import AggregateSimilarityStrategy
from src.similarity.heterogeneous.HITSDistanceStrategy import HITSDistanceStrategy
from src.similarity.heterogeneous.NeighborSimStrategy import NeighborSimStrategy
from src.similarity.heterogeneous.PageRankDistanceStrategy import PageRankDistanceStrategy
from src.similarity.heterogeneous.PathSimStrategy import PathSimStrategy
from src.similarity.heterogeneous.SimRankStrategy import SimRankStrategy
from src.util.EdgeBasedMetaPathUtility import EdgeBasedMetaPathUtility

__author__ = 'jontedesco'

import texttable
from experiment.Experiment import Experiment
from src.model.node.dblp.Author import Author
from src.model.node.dblp.Conference import Conference
from src.model.node.dblp.Paper import Paper
from src.util.SampleGraphUtility import SampleGraphUtility

__author__ = 'jontedesco'

class LeaderFollowerAuthorsExampleExperiment(Experiment):

    def outputSimilarityScores(self, authorMap, authors, strategy, strategyName, nodeName = 'Mike'):
        self.output('\n%s Scores (compared to %s):' % (strategyName, nodeName))
        rows = [
            [author.name for author in authors[1:]],
            ['%1.2f' % strategy.findSimilarityScore(authorMap[nodeName], author) for author in authors[1:]]
        ]
        pathSimTable = texttable.Texttable()
        pathSimTable.add_rows(rows)
        self.output(pathSimTable.draw())


    def run(self):

        citationMap = {
            'Mike':  {'Mike': 0,  'Jim': 0,  'Mary': 0,  'Bob': 0,  'Ann': 0, 'Joe': 0,  'Nancy': 0},
            'Jim':   {'Mike': 20, 'Jim': 0,  'Mary': 20, 'Bob': 20, 'Ann': 0, 'Joe': 20, 'Nancy': 0},
            'Mary':  {'Mike': 1,  'Jim': 10, 'Mary': 0,  'Bob': 1,  'Ann': 0, 'Joe': 1,  'Nancy': 0},
            'Bob':   {'Mike': 1,  'Jim': 10, 'Mary': 1,  'Bob': 0,  'Ann': 0, 'Joe': 1,  'Nancy': 0},
            'Ann':   {'Mike': 0,  'Jim': 0,  'Mary': 0,  'Bob': 0,  'Ann': 0, 'Joe': 0,  'Nancy': 0},
            'Joe':   {'Mike': 0,  'Jim': 0,  'Mary': 0,  'Bob': 0,  'Ann': 0, 'Joe': 0,  'Nancy': 0},
            'Nancy': {'Mike': 1,  'Jim': 10, 'Mary': 1,  'Bob': 1,  'Ann': 0, 'Joe': 1,  'Nancy': 0}
        }

        self.graph, authorMap, conferenceMap =\
            SampleGraphUtility.constructPathSimExampleThree(extraAuthorsAndCitations=True, citationMap = citationMap)

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
            authorMap['Joe'],
            authorMap['Nancy'],
        ]
        metaPathUtility = EdgeBasedMetaPathUtility()

        # Project a 2-typed heterogeneous graph over adapted PathSim example
        publicationProjectedGraph = metaPathUtility.createHeterogeneousProjection(self.graph, [Author, Paper, Conference], symmetric = True)
        self.output('\nAdjacency Matrix (Projected):')
        adjMatrixTable = texttable.Texttable()
        rows = [['Author'] + [conference.name for conference in conferences]]
        rows += [[author.name] + [publicationProjectedGraph.getNumberOfEdges(author, conference) for conference in conferences] for author in authors]
        adjMatrixTable.add_rows(rows)
        self.output(adjMatrixTable.draw())

        # Project a homogeneous citation graph over adapted PathSim example
        citationProjectedGraph = metaPathUtility.createHomogeneousProjection(self.graph, [Author, Paper, Paper, Author])
        self.output('\nCitation Matrix:')
        adjMatrixTable = texttable.Texttable()
        rows = [['Author'] + [author.name for author in authors]]
        rows += [[author.name] + [citationProjectedGraph.getNumberOfEdges(author, otherAuthor) for otherAuthor in authors] for author in authors]
        adjMatrixTable.add_rows(rows)
        self.output(adjMatrixTable.draw())

        # Output total out/in citations
        self.output('\nCitations Total:')
        totalCitationsTable = texttable.Texttable()
        rows = [['Author', 'In', 'Out']]
        for author in authors:
            inCount = sum(citationProjectedGraph.getNumberOfEdges(otherAuthor, author) for otherAuthor in authors)
            outCount = sum(citationProjectedGraph.getNumberOfEdges(author, otherAuthor) for otherAuthor in authors)
            rows += [[author.name, inCount, outCount]]
        totalCitationsTable.add_rows(rows)
        self.output(totalCitationsTable.draw())

        # Get PathSim similarity scores
        pathSimStrategy = PathSimStrategy(self.graph, [Author, Paper, Conference, Paper, Author], True)
        self.outputSimilarityScores(authorMap, authors, pathSimStrategy, 'APCPA PathSim')

        # Output SimRank-related scores
        strategy = SimRankStrategy(self.graph, [Author, Paper, Paper, Author], symmetric=True)
        self.outputSimilarityScores(authorMap, authors, strategy, "SimRank")

        # Output the projected PageRank/HITS similarity scores
        for name, algorithm in zip(['PageRank', 'HITS'], [PageRankDistanceStrategy, HITSDistanceStrategy]):
            strategy = algorithm(self.graph, [Author, Paper, Paper, Author], symmetric=True)
            self.outputSimilarityScores(authorMap, authors, strategy, "%s-Distance" % name)

        # Get NeighborSim similarity scores
        inNeighborSimStrategy = NeighborSimStrategy(self.graph, [Author, Paper, Paper, Author])
        self.outputSimilarityScores(authorMap, authors, inNeighborSimStrategy, 'APPA NeighborSim-In')
        outNeighborSimStrategy = NeighborSimStrategy(self.graph, [Author, Paper, Paper, Author], reversed=True)
        self.outputSimilarityScores(authorMap, authors, outNeighborSimStrategy, 'APPA NeighborSim-Out')
        combinedNeighborSim = AggregateSimilarityStrategy(self.graph, [inNeighborSimStrategy, outNeighborSimStrategy], [0.8, 0.2])
        self.outputSimilarityScores(authorMap, authors, combinedNeighborSim, 'APPA NeighborSim-Combined')


if __name__ == '__main__':
    experiment = LeaderFollowerAuthorsExampleExperiment(
        None,
        'Similarity on leader/follower author example'
    )
    experiment.start()