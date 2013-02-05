from src.similarity.heterogeneous.NeighborSimStrategy import NeighborSimStrategy
from src.similarity.heterogeneous.PathSimStrategy import PathSimStrategy
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

        # Get PathSim similarity scores
        pathSimStrategy = PathSimStrategy(self.graph, [Author, Paper, Conference, Paper, Author], True)
        self.outputSimilarityScores(authorMap, authors, pathSimStrategy, 'PathSim')

        # Get NeighborSim similarity scores
        neighborSimStrategy = NeighborSimStrategy(self.graph, [Author, Paper, Paper, Author])
        self.outputSimilarityScores(authorMap, authors, neighborSimStrategy, 'NeighborSim')

if __name__ == '__main__':
    experiment = LeaderFollowerAuthorsExampleExperiment(
        None,
        'Similarity on leader/follower author example'
    )
    experiment.start()