import os
from experiment.Experiment import Experiment
from src.model.node.dblp.Author import Author
from src.model.node.dblp.Conference import Conference
from src.model.node.dblp.Paper import Paper
from src.similarity.heterogeneous.PathSimStrategy import PathSimStrategy

__author__ = 'jontedesco'

class ConferencePathSimFourAreaExperiment(Experiment):
    """
      Runs some experiments with PathSim on author similarity for the 'four area' dataset
    """

    def run(self):

        # Get the conference PKDD
        conferences = self.getNodesByAttribute('name', 'PKDD')
        assert(len(conferences) == 1)
        pkdd = list(conferences)[0]

        # Output the top ten most similar conferences to PKDD (using CPAPC)
        strategy = PathSimStrategy(self.graph, [Conference, Paper, Author, Paper, Conference], True)
        self.output('\n\nTop Ten Similar Conferences to PKDD (CPAPC meta path):\n')
        mostSimilarNodes = strategy.findMostSimilarNodes(pkdd, 10)
        self.output('| Rank\t| Conference')
        for i in xrange(0, 10):
            self.output('| %d \t| %s\t' % (i+1, mostSimilarNodes[i].name))


if __name__ == '__main__':
    experiment = ConferencePathSimFourAreaExperiment(
        os.path.join('graphs', 'fourArea'),
        'Conference PathSim Similarity on Four Area dataset'
    )
    experiment.start()
