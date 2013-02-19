from src.similarity.heterogeneous.NeighborSimConstantPropagationStrategy import NeighborSimConstantPropagationStrategy
from src.similarity.heterogeneous.NeighborSimConstantPreferentialAttachmentStrategy import NeighborSimConstantPreferentialAttachmentStrategy
from src.similarity.heterogeneous.NeighborSimStrategy import NeighborSimStrategy
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
            [author.name for author in authors],
            ['%1.2f' % strategy.findSimilarityScore(authorMap['D'], author) for author in authors]
        ]
        pathSimTable = texttable.Texttable()
        pathSimTable.add_rows(rows)
        self.output(pathSimTable.draw())


    def run(self):

        self.graph, authorMap, conferenceMap, totalCitationCount = SampleGraphUtility.constructMultiDisciplinaryAuthorExample(indirectAuthor = True)

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
            authorMap['J'],
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

        # Output the PathSim similarity scores
        pathsimStretegy = PathSimStrategy(self.graph, [Author, Paper, Conference, Paper, Author], True)
        self.outputSimilarityScores(authorMap, authors, pathsimStretegy, "PathSim")

        # Output the NeighborSim similarity scores
        neighborsimStrategy = NeighborSimStrategy(self.graph, [Author, Paper, Paper, Author])
        self.outputSimilarityScores(authorMap, authors, neighborsimStrategy, "NeighborSim")

        # Constant weight propagation strategy
        propagatedNeighborsimStrategy = NeighborSimConstantPropagationStrategy(self.graph, [Author, Paper, Paper, Author], iterations = 2)
        self.outputSimilarityScores(authorMap, authors, propagatedNeighborsimStrategy, "NeighborSim-ConstantPropagation-2")
        propagatedNeighborsimStrategy = NeighborSimConstantPropagationStrategy(self.graph, [Author, Paper, Paper, Author], iterations = 3)
        self.outputSimilarityScores(authorMap, authors, propagatedNeighborsimStrategy, "NeighborSim-ConstantPropagation-3")
        propagatedNeighborsimStrategy = NeighborSimConstantPropagationStrategy(self.graph, [Author, Paper, Paper, Author], iterations = 4)
        self.outputSimilarityScores(authorMap, authors, propagatedNeighborsimStrategy, "NeighborSim-ConstantPropagation-4")
        propagatedNeighborsimStrategy = NeighborSimConstantPropagationStrategy(self.graph, [Author, Paper, Paper, Author], iterations = 50)
        self.outputSimilarityScores(authorMap, authors, propagatedNeighborsimStrategy, "NeighborSim-ConstantPropagation-50")

        # Preferential attachment propagation strategy
        propagatedNeighborsimStrategy = NeighborSimConstantPreferentialAttachmentStrategy(self.graph, [Author, Paper, Paper, Author], iterations = 2)
        self.outputSimilarityScores(authorMap, authors, propagatedNeighborsimStrategy, "NeighborSim-WeightedPropagation-2")
        propagatedNeighborsimStrategy = NeighborSimConstantPreferentialAttachmentStrategy(self.graph, [Author, Paper, Paper, Author], iterations = 3)
        self.outputSimilarityScores(authorMap, authors, propagatedNeighborsimStrategy, "NeighborSim-WeightedPropagation-3")
        propagatedNeighborsimStrategy = NeighborSimConstantPreferentialAttachmentStrategy(self.graph, [Author, Paper, Paper, Author], iterations = 4)
        self.outputSimilarityScores(authorMap, authors, propagatedNeighborsimStrategy, "NeighborSim-WeightedPropagation-4")
        propagatedNeighborsimStrategy = NeighborSimConstantPreferentialAttachmentStrategy(self.graph, [Author, Paper, Paper, Author], iterations = 50)
        self.outputSimilarityScores(authorMap, authors, propagatedNeighborsimStrategy, "NeighborSim-WeightedPropagation-50")



if __name__ == '__main__':
    experiment = MultiDisciplinaryAuthorsExampleExperiment(
        None,
        'Similarity on multidisciplinary author example'
    )
    experiment.start()