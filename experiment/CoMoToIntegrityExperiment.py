import os
from src.model.node.comoto.Assignment import Assignment
from src.model.node.comoto.Semester import Semester
from src.model.node.comoto.Submission import Submission

__author__ = 'jontedesco'

from Experiment import Experiment

class CoMoToIntegrityExperiment(Experiment):

    def run(self):

        assignmentData = {}

        # Print the semesters with submissions & the number of submissions for each
        for node in self.graph.getNodes():
            if isinstance(node, Assignment):

                node.submissionCount = 0
                semester = None
                for otherNode in self.graph.getSuccessors(node):
                    if isinstance(otherNode , Submission):
                        node.submissionCount += 1
                    elif isinstance(otherNode, Semester):
                        semester = otherNode

                if semester not in assignmentData:
                    assignmentData[semester] = []

                assignmentData[semester].append(node)

        # Order by calendar dates
        keys = sorted(assignmentData.keys(), key=lambda s: (s.year, ('Spring', 'Summer', 'Fall').index(s.season)))

        for semester in keys:
            nodes = assignmentData[semester]
            for node in nodes:

                # Output the name of the assignment & number of submissions we have for it
                self.output("%s (%s %d):  %d" % (node.name, semester.season, semester.year, node.submissionCount))


if __name__ == '__main__':
    experiment = CoMoToIntegrityExperiment(
        os.path.join('graphs', 'cs225comotodata'),
        'CoMoTo data integrity experiment',
        os.path.join('experiment', 'results', 'coMoToDataSummary')
    )
    experiment.start()