import os
import texttable
from experiment.Experiment import Experiment
from src.experiment.helper.ExperimentHelper import ExperimentHelper
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

        experimentHelper = ExperimentHelper()

        # Get the author node for 'Christos Faloutsos)
        authors = experimentHelper.getNodesByAttribute(self.graph, 'name', 'Christos Faloutsos')
        assert(len(authors) == 1)
        christos = list(authors)[0]
        number = 10

        # Output the top ten most similar authors on the APA meta path
        self.output('\n\nTop Ten Similar Authors to Christos Faloutsos (APA meta path):')
        self.conserveMemory = True
        mostSimilarNodes = strategy.findMostSimilarNodes(christos, number)
        apaPathTable = texttable.Texttable()
        apaPathTable.add_rows([['Rank', 'Author']] + [[i+1, mostSimilarNodes[i].name] for i in xrange(0, number)])
        self.output(apaPathTable.draw())

        # Output the top ten most similar authors on the APCPA meta path
        self.conserveMemory = False
        strategy = PathSimStrategy(self.graph, [Author, Paper, Conference, Paper, Author], True)
        self.output('\n\nTop Ten Similar Authors to Christos Faloutsos (APCPA meta path):')
        mostSimilarNodes = strategy.findMostSimilarNodes(christos, number)
        apcpaPathTable = texttable.Texttable()
        apcpaPathTable.add_rows([['Rank', 'Author']] + [[i+1, mostSimilarNodes[i].name] for i in xrange(0, number)])
        self.output(apcpaPathTable.draw())


if __name__ == '__main__':
    experiment = AuthorPathSimFourAreaExperiment(
        os.path.join('graphs', 'fourArea'),
        'Author PathSim Similarity on Four Area dataset'
    )
    experiment.start()
