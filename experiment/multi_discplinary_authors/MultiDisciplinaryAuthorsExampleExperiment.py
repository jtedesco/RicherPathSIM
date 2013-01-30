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

        # Output the adjacency matrix for authors & conferences in the graph
        self.output('\nCitation Matrix:')
        adjMatrixTable = texttable.Texttable()
        rows = [['Author'] + [author.name for author in authors]]
        for author in authors:
            row = [author.name]
            for otherAuthor in authors:
                row.append(authorCitationCounts[author][otherAuthor])
            rows.append(row)
        adjMatrixTable.add_rows(rows)
        self.output(adjMatrixTable.draw())

        # Output the adjacency matrix for authors & conferences in the graph
        self.output('\nAdjacency Matrix:')
        adjMatrixTable = texttable.Texttable()
        rows = [[''] + [conference.name for conference in conferences]]
        projectedGraph = self.metaPathUtility.createHeterogeneousProjection(self.graph, [Author, Paper, Conference])
        for author in authors:
            row = [author.name]
            for conference in conferences:
                row.append(projectedGraph.getNumberOfEdges(author, conference))
            rows.append(row)
        adjMatrixTable.add_rows(rows)
        self.output(adjMatrixTable.draw())

        # Output total citation counts
        self.output('\nTotal Citation Counts:')
        rows = [[author.name for author in authors],['%d' % totalCitationCount[author.name] for author in authors]]
        citationCountTable = texttable.Texttable()
        citationCountTable.add_rows(rows)
        self.output(citationCountTable.draw())

        # Output the PathSim similarity scores
        strategy = PathSimStrategy(self.graph, [Author, Paper, Conference, Paper, Author], True)
        self.output('\nPathsim Scores (compared to D):')
        rows = [
            [author.name for author in authors[1:]],
            ['%1.2f' % strategy.findSimilarityScore(authorMap['D'], author) for author in authors[1:]]
        ]
        pathSimTable = texttable.Texttable()
        pathSimTable.add_rows(rows)
        self.output(pathSimTable.draw())

if __name__ == '__main__':
    experiment = MultiDisciplinaryAuthorsExampleExperiment(
        None,
        'PathSim Similarity on paper examples'
    )
    experiment.start()