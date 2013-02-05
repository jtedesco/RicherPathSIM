from src.similarity.heterogeneous.HITSDistanceStrategy import HITSDistanceStrategy
from src.similarity.heterogeneous.NeighborSimStrategy import NeighborSimStrategy
from src.similarity.heterogeneous.PageRankDistanceStrategy import PageRankDistanceStrategy
from src.similarity.heterogeneous.SimRankStrategy import SimRankStrategy
from src.util.EdgeBasedMetaPathUtility import EdgeBasedMetaPathUtility

__author__ = 'jontedesco'

import texttable
from experiment.Experiment import Experiment
from src.model.node.dblp.Author import Author
from src.model.node.dblp.Conference import Conference
from src.model.node.dblp.Paper import Paper
from src.similarity.heterogeneous.PathSimStrategy import PathSimStrategy
from src.util.SampleGraphUtility import SampleGraphUtility

__author__ = 'jontedesco'

class MultiDisciplinaryAuthorsExampleExperiment(Experiment):

    def outputSimilarityScores(self, authorMap, authors, strategy, strategyName):
        self.output('\n%s Scores (compared to D):' % strategyName)
        rows = [
            [author.name for author in authors[1:]],
            ['%1.2f' % strategy.findSimilarityScore(authorMap['D'], author) for author in authors[1:]]
        ]
        pathSimTable = texttable.Texttable()
        pathSimTable.add_rows(rows)
        self.output(pathSimTable.draw())


    def run(self):

        self.graph, authorMap, conferenceMap, totalCitationCount = SampleGraphUtility.constructMultiDisciplinaryAuthorExample()

        # Get the nodes we care about
        conferences = [
            conferenceMap['VLDB'],
            conferenceMap['KDD']
        ]
        authors = [
            authorMap['A'],
            authorMap['B'],
            authorMap['C'],
            authorMap['D'],
            authorMap['E'],
            authorMap['F'],
            authorMap['G'],
            authorMap['H'],
            authorMap['I'],
        ]
        self.metaPathUtility = EdgeBasedMetaPathUtility()

        # Build homogeneous projection of network (authors, with edges for times authors cite each other)
        projectedGraph = self.metaPathUtility.createHomogeneousProjection(self.graph, [Author, Paper, Paper, Author])
        authorCitationCounts = {}
        for author in projectedGraph.getNodes():
            authorCitationCounts[author] = {}
            for otherAuthor in projectedGraph.getNodes():
                authorCitationCounts[author][otherAuthor] = projectedGraph.getNumberOfEdges(author, otherAuthor)

        # Output the adjacency matrix for authors-authors in the graph
        self.output('\nCitation Matrix:')
        adjMatrixTable = texttable.Texttable()
        rows = [['Author'] + [author.name for author in authors]]
        rows += [[author.name] + [authorCitationCounts[author][otherAuthor] for otherAuthor in authors] for author in authors]
        adjMatrixTable.add_rows(rows)
        self.output(adjMatrixTable.draw())

        # Output the adjacency matrix for authors & conferences in the graph
        self.output('\nAdjacency Matrix:')
        adjMatrixTable = texttable.Texttable()
        projectedGraph = self.metaPathUtility.createHeterogeneousProjection(self.graph, [Author, Paper, Conference])
        rows = [[''] + [conference.name for conference in conferences]]
        rows += [[author.name] + [projectedGraph.getNumberOfEdges(author, conference) for conference in conferences] for author in authors]
        adjMatrixTable.add_rows(rows)
        self.output(adjMatrixTable.draw())

        # Output total citation counts
        self.output('\nTotal Citation Counts:')
        rows = [[author.name for author in authors],['%d' % totalCitationCount[author.name] for author in authors]]
        citationCountTable = texttable.Texttable()
        citationCountTable.add_rows(rows)
        self.output(citationCountTable.draw())


        # Output the NeighborSim similarity scores
        strategy = NeighborSimStrategy(self.graph, [Author, Paper, Paper, Author])
        self.outputSimilarityScores(authorMap, authors, strategy, "NeighborSim")

        # Output the PathSim similarity scores
        strategy = PathSimStrategy(self.graph, [Author, Paper, Conference, Paper, Author], True)
        self.outputSimilarityScores(authorMap, authors, strategy, "PathSim")

        # Output SimRank-related scores
        strategy = SimRankStrategy(self.graph, [Author, Paper, Paper, Author], symmetric=True)
        self.outputSimilarityScores(authorMap, authors, strategy, "SimRank")

        # Output the projected PageRank/HITS similarity scores
        for name, algorithm in zip(['PageRank', 'HITS'], [PageRankDistanceStrategy, HITSDistanceStrategy]):
            researchAreas = {
                (authorMap['A'], authorMap['B'], authorMap['C'], authorMap['D'], authorMap['E'], authorMap['I']),
                (authorMap['F'], authorMap['G'], authorMap['H'], authorMap['D'], authorMap['E'], authorMap['I']),
            }
            strategy = algorithm(self.graph, [Author, Paper, Paper, Author], nodeSets=researchAreas, symmetric=True)
            self.outputSimilarityScores(authorMap, authors, strategy, "%s-Distance" % name)


if __name__ == '__main__':
    experiment = MultiDisciplinaryAuthorsExampleExperiment(
        None,
        'Similarity on multidisciplinary author example'
    )
    experiment.start()