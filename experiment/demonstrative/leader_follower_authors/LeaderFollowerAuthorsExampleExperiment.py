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

        citationMatrix = {
            'Mike':  {'Mike': 0, 'Jim': 0,  'Mary': 0,  'Bob': 0,  'Ann': 0,  'Joe': 0, 'Nancy': 0},
            'Jim':   {'Mike': 1, 'Jim': 0,  'Mary': 10, 'Bob': 10, 'Ann': 10, 'Joe': 1, 'Nancy': 1},
            'Mary':  {'Mike': 1, 'Jim': 10, 'Mary': 0,  'Bob': 5,  'Ann': 5,  'Joe': 1, 'Nancy': 1},
            'Bob':   {'Mike': 1, 'Jim': 10, 'Mary': 5,  'Bob': 0,  'Ann': 5,  'Joe': 1, 'Nancy': 1},
            'Ann':   {'Mike': 1, 'Jim': 10, 'Mary': 5,  'Bob': 5,  'Ann': 0,  'Joe': 1, 'Nancy': 1},
            'Joe':   {'Mike': 0, 'Jim': 0,  'Mary': 0,  'Bob': 0,  'Ann': 0,  'Joe': 0, 'Nancy': 1},
            'Nancy': {'Mike': 1, 'Jim': 0,  'Mary': 1,  'Bob': 1,  'Ann': 1,  'Joe': 1, 'Nancy': 0}
        }

        self.graph, authorMap, conferenceMap = SampleGraphUtility.constructPathSimExampleThree(extraAuthors=True, citationMatrix=citationMatrix)

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

        # Project a 2-typed heterogeneous graph over PathSim example
        self.output('\nAdjacency Matrix (Projected):')
        adjMatrixTable = texttable.Texttable()
        projectedGraph = metaPathUtility.createHeterogeneousProjection(self.graph, [Author, Paper, Conference], symmetric = True)
        rows = [['Author'] + [conference.name for conference in conferences]]
        rows += [[author.name] + [projectedGraph.getNumberOfEdges(author, conference) for conference in conferences] for author in authors]
        adjMatrixTable.add_rows(rows)
        self.output(adjMatrixTable.draw())


if __name__ == '__main__':
    experiment = LeaderFollowerAuthorsExampleExperiment(
        None,
        'Similarity on leader/follower author example'
    )
    experiment.start()