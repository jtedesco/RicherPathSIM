import unittest
import networkx
from src.importers.CoMoToDataImporter import CoMoToDataImporter
from src.model.edge.comoto.AssignmentSubmission import AssignmentSubmission
from src.model.edge.comoto.Author import Author
from src.model.edge.comoto.Enrollment import Enrollment
from src.model.edge.comoto.SemesterAssignment import SemesterAssignment
from src.model.edge.comoto.matches.SameSemesterMatch import SameSemesterMatch
from src.model.edge.comoto.matches.PartnerMatch import PartnerMatch
from src.model.edge.comoto.matches.SolutionMatch import SolutionMatch
from src.model.node.comoto.Assignment import Assignment
from src.model.node.comoto.Semester import Semester
from src.model.node.comoto.Student import Student
from src.model.node.comoto.Submission import Submission

__author__ = 'jontedesco'

class CoMoToDataImporterTest(unittest.TestCase):
    """
      Unit tests for the CoMoToDataImporter
    """

    def __addEdges(self, graph, a, b, object):
        """
          Helper function to add bi-directional directed edges
        """
        graph.add_edge(a, b, object.attributes())
        graph.add_edge(b, a, object.attributes())

    def setUp(self):

        self.dataImporter = CoMoToDataImporter(None, None, None)

        self.sameSemesterMatchAnalysis = {
            'analysis_data': {
                50: {
                    'matches': {
                        'crossSemesterMatches': [],
                        'solutionMatches': [],
                        'sameSemesterMatches': [
                            {
                                'id': 5000,
                                'score1': 70,
                                'score2': 74,
                                'submission_1_id': 5001,
                                'submission_2_id': 5003
                            }
                        ]
                    },
                    'submissions': {
                        5001: {
                            'id': 5001,
                            'offering_id': 14,
                            'partner_ids': [],
                            'type': 'studentsubmission',
                            'student': {
                                'id': 10001,
                                'display_name': 'Smith, John',
                                'netid': 'johnsmith'
                            }
                        },
                        5002: {
                            'id': 5002,
                            'offering_id': 14,
                            'partner_ids': [],
                            'type': 'studentsubmission',
                            'student': {
                                'id': 10002,
                                'display_name': 'Doe, Jane',
                                'netid': 'janedoe'
                            }
                        },
                        5003: {
                            'id': 5003,
                            'offering_id': 14,
                            'partner_ids': [],
                            'type': 'studentsubmission',
                            'student': {
                                'id': 10003,
                                'display_name': 'Smith, Joe',
                                'netid': 'joesmith'
                            }
                        }
                    }
                }
            },
            'assignments': {
                1: {
                    'id': 1,
                    'analysis_id': 50,
                    'moss_analysis_pruned_offering': {
                        'semester': {
                            'id': 7
                        }
                    }
                }
            },
            'offerings': {
                14: {
                    'id': 14,
                    'semester': {
                        'id': 7,
                        'season': 'Fall',
                        'year': 2012
                    }
                }
            }
        }

        self.partnerMatchAnalysis = {
            'analysis_data': {
                50: {
                    'matches': {
                        'crossSemesterMatches': [],
                        'solutionMatches': [],
                        'sameSemesterMatches': [
                            {
                                'id': 5000,
                                'score1': 70,
                                'score2': 74,
                                'submission_1_id': 5001,
                                'submission_2_id': 5003
                            }
                        ]
                    },
                    'submissions': {
                        5001: {
                            'id': 5001,
                            'offering_id': 14,
                            'partner_ids': [5003],
                            'type': 'studentsubmission',
                            'student': {
                                'id': 10001,
                                'display_name': 'Smith, John',
                                'netid': 'johnsmith'
                            }
                        },
                        5002: {
                            'id': 5002,
                            'offering_id': 14,
                            'partner_ids': [],
                            'type': 'studentsubmission',
                            'student': {
                                'id': 10002,
                                'display_name': 'Doe, Jane',
                                'netid': 'janedoe'
                            }
                        },
                        5003: {
                            'id': 5003,
                            'offering_id': 14,
                            'partner_ids': [5001],
                            'type': 'studentsubmission',
                            'student': {
                                'id': 10003,
                                'display_name': 'Smith, Joe',
                                'netid': 'joesmith'
                            }
                        }
                    }
                }
            },
            'assignments': {
                1: {
                    'id': 1,
                    'analysis_id': 50,
                    'moss_analysis_pruned_offering': {
                        'semester': {
                            'id': 7
                        }
                    }
                }
            },
            'offerings': {
                14: {
                    'id': 14,
                    'semester': {
                        'id': 7,
                        'season': 'Fall',
                        'year': 2012
                    }
                }
            }
        }

        self.solutionMatchAnalysis = {
            'analysis_data': {
                50: {
                    'matches': {
                        'crossSemesterMatches': [],
                        'solutionMatches': [
                            {
                                'id': 5000,
                                'score1': 80,
                                'score2': 80,
                                'submission_1_id': 5001,
                                'submission_2_id': 5004
                            }
                        ],
                        'sameSemesterMatches': []
                    },
                    'submissions': {
                        5001: {
                            'id': 5001,
                            'offering_id': 14,
                            'partner_ids': [],
                            'type': 'studentsubmission',
                            'student': {
                                'id': 10001,
                                'display_name': 'Smith, John',
                                'netid': 'johnsmith'
                            }
                        },
                        5002: {
                            'id': 5002,
                            'offering_id': 14,
                            'partner_ids': [],
                            'type': 'studentsubmission',
                            'student': {
                                'id': 10002,
                                'display_name': 'Doe, Jane',
                                'netid': 'janedoe'
                            }
                        },
                        5003: {
                            'id': 5003,
                            'offering_id': 14,
                            'partner_ids': [],
                            'type': 'studentsubmission',
                            'student': {
                                'id': 10003,
                                'display_name': 'Smith, Joe',
                                'netid': 'joesmith'
                            }
                        },
                        5004: {
                            'id': 5004,
                            'offering_id': 14,
                            'type': 'solutionsubmission'
                        }
                    }
                }
            },
            'assignments': {
                1: {
                    'id': 1,
                    'analysis_id': 50,
                    'moss_analysis_pruned_offering': {
                        'semester': {
                            'id': 7
                        }
                    }
                }
            },
            'offerings': {
                14: {
                    'id': 14,
                    'semester': {
                        'id': 7,
                        'season': 'Fall',
                        'year': 2012
                    }
                }
            }
        }


    def testSameSemesterMatchAnalysis(self):
        """
          Tests that the graph is built correctly given some simple test analysis. This
          test case considers the case of:

            * Single assignment, single analysis, single semester
            * Three submissions
            * One (same semester) submission pair match
        """

        # Setup CoMoTo data & expected graph
        analysisData = self.sameSemesterMatchAnalysis

        student1 = Student(10001, 'Smith, John', 'johnsmith')
        student2 = Student(10002, 'Doe, Jane', 'janedoe')
        student3 = Student(10003, 'Smith, Joe', 'joesmith')
        submission1 = Submission(5001)
        submission2 = Submission(5002)
        submission3 = Submission(5003)
        assignment = Assignment(1)
        semester = Semester(7, 'Fall', 2012)

        expectedGraph = networkx.DiGraph()
        expectedGraph.add_node(student1)
        expectedGraph.add_node(student2)
        expectedGraph.add_node(student3)
        expectedGraph.add_node(submission1)
        expectedGraph.add_node(submission2)
        expectedGraph.add_node(submission3)

        self.__addEdges(expectedGraph, submission1, assignment, AssignmentSubmission())
        self.__addEdges(expectedGraph, submission2, assignment, AssignmentSubmission())
        self.__addEdges(expectedGraph, submission3, assignment, AssignmentSubmission())
        self.__addEdges(expectedGraph, submission1, student1, Author())
        self.__addEdges(expectedGraph, submission2, student2, Author())
        self.__addEdges(expectedGraph, submission3, student3, Author())
        self.__addEdges(expectedGraph, student1, semester, Enrollment())
        self.__addEdges(expectedGraph, student2, semester, Enrollment())
        self.__addEdges(expectedGraph, student3, semester, Enrollment())
        self.__addEdges(expectedGraph, submission1, submission3, SameSemesterMatch(72, 5000))
        self.__addEdges(expectedGraph, semester, assignment, SemesterAssignment())

        actualGraph = self.dataImporter.buildGraph(analysisData)

        self.assertEqual(expectedGraph, actualGraph)


    def testPartnerMatchAnalysis(self):
        """
          Tests that the graph is built correctly given some simple test analysis. This
          test case considers the case of:

            * Single assignment, single analysis, single semester
            * Three submissions
            * One (same semester) submission partner pair match
        """

        # Setup CoMoTo data & expected graph
        analysisData = self.partnerMatchAnalysis

        student1 = Student(10001, 'Smith, John', 'johnsmith')
        student2 = Student(10002, 'Doe, Jane', 'janedoe')
        student3 = Student(10003, 'Smith, Joe', 'joesmith')
        submission1 = Submission(5001)
        submission2 = Submission(5002)
        submission3 = Submission(5003)
        assignment = Assignment(1)
        semester = Semester(7, 'Fall', 2012)

        expectedGraph = networkx.DiGraph()
        expectedGraph.add_node(student1)
        expectedGraph.add_node(student2)
        expectedGraph.add_node(student3)
        expectedGraph.add_node(submission1)
        expectedGraph.add_node(submission2)
        expectedGraph.add_node(submission3)

        self.__addEdges(expectedGraph, submission1, assignment, AssignmentSubmission())
        self.__addEdges(expectedGraph, submission2, assignment, AssignmentSubmission())
        self.__addEdges(expectedGraph, submission3, assignment, AssignmentSubmission())
        self.__addEdges(expectedGraph, submission1, student1, Author())
        self.__addEdges(expectedGraph, submission2, student2, Author())
        self.__addEdges(expectedGraph, submission3, student3, Author())
        self.__addEdges(expectedGraph, student1, semester, Enrollment())
        self.__addEdges(expectedGraph, student2, semester, Enrollment())
        self.__addEdges(expectedGraph, student3, semester, Enrollment())
        self.__addEdges(expectedGraph, submission1, submission3, PartnerMatch(72, 5000))
        self.__addEdges(expectedGraph, semester, assignment, SemesterAssignment())

        actualGraph = self.dataImporter.buildGraph(analysisData)

        self.assertEqual(expectedGraph, actualGraph)


    def testSolutionMatchAnalysis(self):
        """
          Tests that the graph is built correctly given some simple test analysis. This
          test case considers the case of:

            * Single assignment, single analysis, single semester
            * Three submissions
            * One (same semester) solution match
        """

        # Setup CoMoTo data & expected graph
        analysisData = self.solutionMatchAnalysis

        student1 = Student(10001, 'Smith, John', 'johnsmith')
        student2 = Student(10002, 'Doe, Jane', 'janedoe')
        student3 = Student(10003, 'Smith, Joe', 'joesmith')
        submission1 = Submission(5001)
        submission2 = Submission(5002)
        submission3 = Submission(5003)
        solutionSubmission = Submission(5004, True)
        assignment = Assignment(1)
        semester = Semester(7, 'Fall', 2012)

        expectedGraph = networkx.DiGraph()
        expectedGraph.add_node(student1)
        expectedGraph.add_node(student2)
        expectedGraph.add_node(student3)
        expectedGraph.add_node(submission1)
        expectedGraph.add_node(submission2)
        expectedGraph.add_node(submission3)
        expectedGraph.add_node(solutionSubmission)

        self.__addEdges(expectedGraph, submission1, assignment, AssignmentSubmission())
        self.__addEdges(expectedGraph, submission2, assignment, AssignmentSubmission())
        self.__addEdges(expectedGraph, submission3, assignment, AssignmentSubmission())
        self.__addEdges(expectedGraph, submission1, student1, Author())
        self.__addEdges(expectedGraph, submission2, student2, Author())
        self.__addEdges(expectedGraph, submission3, student3, Author())
        self.__addEdges(expectedGraph, student1, semester, Enrollment())
        self.__addEdges(expectedGraph, student2, semester, Enrollment())
        self.__addEdges(expectedGraph, student3, semester, Enrollment())
        self.__addEdges(expectedGraph, submission1, solutionSubmission, SolutionMatch(80, 5000))
        self.__addEdges(expectedGraph, semester, assignment, SemesterAssignment())

        actualGraph = self.dataImporter.buildGraph(analysisData)

        self.assertEqual(expectedGraph, actualGraph)
