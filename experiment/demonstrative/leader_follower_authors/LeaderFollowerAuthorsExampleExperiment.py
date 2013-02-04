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

        self.graph, authorMap, conferenceMap = SampleGraphUtility.constructPathSimExampleThree(extraAuthorsAndCitations=True)

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