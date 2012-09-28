import os
from experiment.Experiment import Experiment

__author__ = 'jontedesco'

class AuthorPathSimFourAreaExperiment(Experiment):
    """
      Runs some experiments with PathSim on author similarity for the 'four area' dataset
    """

    def run(self):
        pass


if __name__ == '__main__':
    experiment = AuthorPathSimFourAreaExperiment(
        os.path.join('graphs', 'fourArea'),
        'Author PathSim Similarity on Four Area dataset'
    )
    experiment.start()