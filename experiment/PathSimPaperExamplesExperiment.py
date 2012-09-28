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
        self.output('Adjacency Matrix:\n')
        line = '|\t|'
        for conference in conferences:
            line += ' ' + conference.name + '\t|'
        self.output(line)
        for author in authors:
            line = '| %s\t|' % author.name
            for conference in conferences:
                metaPaths = MetaPathUtility.findMetaPaths(self.graph, author, conference, [Author, Paper, Conference])
                line += ' %d  \t|' % len(metaPaths)
            self.output(line)

        # Output the PathSim similarity scores
        self.output('\n\nPathsim Scores (compared to Mike):\n')
        line = '|'
        for author in authors[1:]:
            line += ' ' + author.name + '\t|'
        self.output(line)
        line = '|'
        strategy = PathSimStrategy(self.graph, [Author, Paper, Conference, Paper, Author], True)
        for author in authors[1:]:
            line += ' %1.2f\t|' % strategy.findSimilarityScore(authorMap['Mike'], author)
        self.output(line)


if __name__ == '__main__':
    experiment = PathSimPaperExamplesExperiment(
        None,
        'PathSim Similarity on paper examples'
    )
    experiment.start()