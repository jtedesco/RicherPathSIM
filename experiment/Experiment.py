import logging
import threading
import cPickle
from src.logger.ColoredLogger import ColoredLogger

__author__ = 'jontedesco'


class Experiment(threading.Thread):
    """
      Top-level class for running experiments, containing helper methods common code for experiments
    """

    def __init__(self, inputGraphPath, experimentTitle, outputFilePath=None):
        """
          Creates a new experiment to run, given the path to the serialized graph object to load
        """
        super(Experiment, self).__init__()

        # Load the graph from the file
        self.graph = cPickle.load(open(inputGraphPath)) if inputGraphPath is not None else None
        self.graph.inputPath = inputGraphPath

        self.outputFilePath = outputFilePath

        logging.setLoggerClass(ColoredLogger)
        self.logger = logging.getLogger(experimentTitle)


    def output(self, text):
        """
          Output a line of text to the output file (if it exists), or otherwise, output to console
        """

        if self.outputFilePath is not None:
            with open(self.outputFilePath, 'a') as f:
                f.write(text + '\n')
        else:
            print(text)
