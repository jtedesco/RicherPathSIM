import texttable
from experiment.Experiment import Experiment
from src.model.node.dblp.Author import Author
from src.model.node.dblp.Conference import Conference
from src.model.node.dblp.Paper import Paper
from src.similarity.heterogeneous.PathSimStrategy import PathSimStrategy
from src.util.MetaPathUtility import MetaPathUtility
from src.util.SampleGraphUtility import SampleGraphUtility

__author__ = 'jontedesco'

class PathSimPaperExamplesExperiment(Experiment):
    """
      Experiment to test results of PathSim on examples given in PathSim paper
    """

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

        # Output the adjacency matrix for authors & conferences in the graph
        self.output('\nAdjacency Matrix:')
        adjMatrixTable = texttable.Texttable()
        rows = [['Author'] + [conference.name for conference in conferences]]
        for author in authors:
            row = [author.name]
            for conference in conferences:
                metaPaths = MetaPathUtility.findMetaPaths(self.graph, author, conference, [Author, Paper, Conference])
                row.append(len(metaPaths))
            rows.append(row)
        adjMatrixTable.add_rows(rows)
        self.output(adjMatrixTable.draw())

        # Output the PathSim similarity scores
        strategy = PathSimStrategy(self.graph, [Author, Paper, Conference, Paper, Author], True)
        self.output('\n\nPathsim Scores (compared to Mike):')
        rows = [
            [author.name for author in authors[1:]],
            ['%1.2f' % strategy.findSimilarityScore(authorMap['Mike'], author) for author in authors[1:]]
        ]
        pathSimTable = texttable.Texttable()
        pathSimTable.add_rows(rows)
        self.output(pathSimTable.draw())


if __name__ == '__main__':
    experiment = PathSimPaperExamplesExperiment(
        None,
        'PathSim Similarity on paper examples'
    )
    experiment.start()