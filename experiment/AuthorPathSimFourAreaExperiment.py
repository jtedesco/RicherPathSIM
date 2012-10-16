import os
from experiment.Experiment import Experiment
from src.model.node.dblp.Author import Author
from src.model.node.dblp.Conference import Conference
from src.model.node.dblp.Paper import Paper
from src.similarity.heterogeneous.PathSimStrategy import PathSimStrategy

__author__ = 'jontedesco'

class AuthorPathSimFourAreaExperiment(Experiment):
    """
      Runs some experiments with PathSim on author similarity for the 'four area' dataset
    """

    def run(self):

        strategy = PathSimStrategy(self.graph, [Author, Paper, Author], True)

        # Get the author node for 'Christos Faloutsos)
        authors = self.getNodesByAttribute('name', 'Christos Faloutsos')
        assert(len(authors) == 1)
        christos = list(authors)[0]

        # Output the top ten most similar authors on the APA meta path
        self.output('\n\nTop Ten Similar Authors to Christos Faloutsos (APA meta path):\n')
        mostSimilarNodes = strategy.findMostSimilarNodes(christos, 10)
        self.output('| Rank\t| Author')
        for i in xrange(0, 10):
            self.output('| %d \t| %s\t' % (i+1, mostSimilarNodes[i].name))

        # Output the top ten most similar authors on the APCPA meta path
        strategy = PathSimStrategy(self.graph, [Author, Paper, Conference, Paper, Author], True)
        self.output('\n\nTop Ten Similar Authors to Christos Faloutsos (APCPA meta path):\n')
        mostSimilarNodes = strategy.findMostSimilarNodes(christos, 10)
        self.output('| Rank\t| Author')
        for i in xrange(0, 10):
            self.output('| %d \t| %s\t' % (i+1, mostSimilarNodes[i].name))


if __name__ == '__main__':
    experiment = AuthorPathSimFourAreaExperiment(
        os.path.join('graphs', 'fourArea'),
        'Author PathSim Similarity on Four Area dataset'
    )
    experiment.start()
