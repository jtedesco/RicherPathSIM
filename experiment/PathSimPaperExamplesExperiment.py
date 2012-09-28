import os
from experiment.Experiment import Experiment

__author__ = 'jontedesco'

class PathSimPaperExamplesExperiment(Experiment):
    """
      Experiment to test results of PathSim on examples given in PathSim paper
    """

    def run(self):
        pass

if __name__ == '__main__':
    experiment = PathSimPaperExamplesExperiment(
        os.path.join('graphs', 'fourArea'),
        'PathSim Similarity on paper examples'
    )
    experiment.start()