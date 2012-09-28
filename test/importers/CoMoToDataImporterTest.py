from src.graph.GraphFactory import GraphFactory
from src.importer.CoMoToDataImporter import CoMoToDataImporter
from src.model.edge.comoto.AssignmentSubmission import AssignmentSubmission
from src.model.edge.comoto.Authorship import Authorship
from src.model.edge.comoto.Enrollment import Enrollment
from src.model.edge.comoto.SemesterAssignment import SemesterAssignment
from src.model.edge.comoto.matches.CrossSemesterMatch import CrossSemesterMatch
from src.model.edge.comoto.matches.SameSemesterMatch import SameSemesterMatch
from src.model.edge.comoto.matches.PartnerMatch import PartnerMatch
from src.model.edge.comoto.matches.SolutionMatch import SolutionMatch
from src.model.node.comoto.Assignment import Assignment
from src.model.node.comoto.Semester import Semester
from src.model.node.comoto.Student import Student
from src.model.node.comoto.Submission import Submission
from test.importers.ImporterTest import ImporterTest

__author__ = 'jontedesco'

class CoMoToDataImporterTest(ImporterTest):
    """
      Unit tests for the CoMoToDataImporter
    """

    def setUp(self):

        self.dataImporter = CoMoToDataImporter(None, None, None)

        self.sameSemesterMatchAnalysis = {
            'analysis_data': {
                50: {
                    'matches': {
                        'cross_semester_matches': [],
                        'solution_matches': [],
                        'same_semester_matches': [
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
                        '5001': {
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
                        '5002': {
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
                        '5003': {
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
            'assignments': [{
                'id': 1,
                'name': 'MP1',
                'analysis_id': 50,
                'moss_analysis_pruned_offering': {
                    'semester': {
                        'id': 7
                    }
                }
            }],
            'offerings': [{
                'id': 14,
                'semester': {
                    'id': 7,
                    'season': 'Spring',
                    'year': 2011
                }
            }]
        }

        self.invalidSameSemesterMatchAnalysis = {
            'analysis_data': {
                50: {
                    'matches': {
                        'cross_semester_matches': [],
                        'solution_matches': [],
                        'same_semester_matches': [
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
                        '5001': {
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
                        '5002': {
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
                        '5003': {
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
            'assignments': [{
                'id': 1,
                'analysis_id': 50,
                'name': 'MP1',
                'moss_analysis_pruned_offering': {
                    'semester': {
                        'id': 7
                    }
                }
            }, {
                'name': 'invalid assignment!',
                'id': -1
            }],
            'offerings': [{
                'id': 14,
                'semester': {
                    'id': 7,
                    'season': 'Spring',
                    'year': 2011
                }
            }, {
                'id': 15,
                'semester': {
                    'id': 8,
                    'season': 'Spring',
                    'year': -1
                }
            }]
        }

        self.partnerMatchAnalysis = {
            'analysis_data': {
                50: {
                    'matches': {
                        'cross_semester_matches': [],
                        'solution_matches': [],
                        'same_semester_matches': [
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
                        '5001': {
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
                        '5002': {
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
                        '5003': {
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
            'assignments': [{
                'id': 1,
                'analysis_id': 50,
                'name': 'MP1',
                'moss_analysis_pruned_offering': {
                    'semester': {
                        'id': 7
                    }
                }
            }],
            'offerings': [{
                'id': 14,
                'semester': {
                    'id': 7,
                    'season': 'Spring',
                    'year': 2011
                }
            }]
        }

        self.solutionMatchAnalysis = {
            'analysis_data': {
                50: {
                    'matches': {
                        'cross_semester_matches': [],
                        'solution_matches': [
                            {
                                'id': 5000,
                                'score1': 80,
                                'score2': 80,
                                'submission_1_id': 5001,
                                'submission_2_id': 5004
                            }
                        ],
                        'same_semester_matches': []
                    },
                    'submissions': {
                        '5001': {
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
                        '5002': {
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
                        '5003': {
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
                        '5004': {
                            'id': 5004,
                            'offering_id': 14,
                            'type': 'solutionsubmission'
                        }
                    }
                }
            },
            'assignments': [{
                'id': 1,
                'analysis_id': 50,
                'name': 'MP1',
                'moss_analysis_pruned_offering': {
                    'semester': {
                        'id': 7
                    }
                }
            }],
            'offerings': [{
                'id': 14,
                'semester': {
                    'id': 7,
                    'season': 'Spring',
                    'year': 2011
                }
            }]
        }

        self.crossSemesterMatchAnalysis = {
            'analysis_data': {
                50: {
                    'matches': {
                        'cross_semester_matches': [
                            {
                                'id': 5000,
                                'score1': 70,
                                'score2': 74,
                                'submission_1_id': 5001,
                                'submission_2_id': 5004
                            }
                        ],
                        'solution_matches': [],
                        'same_semester_matches': []
                    },
                    'submissions': {
                        '5001': {
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
                        '5002': {
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
                        '5003': {
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
                        '5004': {
                            'id': 5004,
                            'offering_id': 15,
                            'partner_ids': [],
                            'type': 'studentsubmission',
                            'student': {
                                'id': 10004,
                                'display_name': 'Smith, Alex',
                                'netid': 'alexsmith'
                            }
                        }
                    }
                }
            },
            'assignments': [{
                'id': 1,
                'analysis_id': 50,
                'name': 'MP1',
                'moss_analysis_pruned_offering': {
                    'semester': {
                        'id': 7
                    }
                }
            }, {
                'id': 2,
                'analysis_id': 71,
                'name': 'MP2',
                'moss_analysis_pruned_offering': {
                    'semester': {
                        'id': 8
                    }
                }
            }],
            'offerings': [{
                'id': 14,
                'semester': {
                    'id': 7,
                    'season': 'Spring',
                    'year': 2011
                }
            }, {
                'id': 15,
                'semester': {
                    'id': 8,
                    'season': 'Spring',
                    'year': 2012
                }
            }]
        }

        self.retakingStudentAnalysis = {
            'analysis_data': {
                50: {
                    'matches': {
                        'cross_semester_matches': [
                            {
                                'id': 5000,
                                'score1': 70,
                                'score2': 74,
                                'submission_1_id': 5001,
                                'submission_2_id': 5004
                            }
                        ],
                        'solution_matches': [],
                        'same_semester_matches': []
                    },
                    'submissions': {
                        '5001': {
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
                        '5002': {
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
                        '5003': {
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
                        '5004': {
                            'id': 5004,
                            'offering_id': 15,
                            'partner_ids': [],
                            'type': 'studentsubmission',
                            'student': {
                                'id': 10001,
                                'display_name': 'Smith, John',
                                'netid': 'johnsmith'
                            }
                        },
                        '5005': {
                            'id': 5005,
                            'offering_id': 15,
                            'partner_ids': [],
                            'type': 'studentsubmission',
                            'student': {
                                'id': 10004,
                                'display_name': 'Smith, Alex',
                                'netid': 'alexsmith'
                            }
                        }
                    }
                }
            },
            'assignments': [{
                'id': 1,
                'analysis_id': 50,
                'name': 'MP1',
                'moss_analysis_pruned_offering': {
                    'semester': {
                        'id': 7
                    }
                }
            }, {
                'id': 2,
                'analysis_id': 61,
                'name': 'MP2',
                'moss_analysis_pruned_offering': {
                    'semester': {
                        'id': 8
                    }
                }
            }],
            'offerings': [{
                'id': 14,
                'semester': {
                    'id': 7,
                    'season': 'Spring',
                    'year': 2011
                }
            }, {
                'id': 15,
                'semester': {
                    'id': 8,
                    'season': 'Spring',
                    'year': 2012
                }
            }]
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
        assignment = Assignment(1, 'MP1')
        semester = Semester(7, 'Spring', 2011)

        expectedGraph = GraphFactory.createInstance()
        expectedGraph.addNode(student1)
        expectedGraph.addNode(student2)
        expectedGraph.addNode(student3)
        expectedGraph.addNode(submission1)
        expectedGraph.addNode(submission2)
        expectedGraph.addNode(submission3)
        expectedGraph.addNode(assignment)
        expectedGraph.addNode(semester)

        expectedGraph.addBothEdges(submission1, assignment, AssignmentSubmission())
        expectedGraph.addBothEdges(submission2, assignment, AssignmentSubmission())
        expectedGraph.addBothEdges(submission3, assignment, AssignmentSubmission())
        expectedGraph.addBothEdges(submission1, student1, Authorship())
        expectedGraph.addBothEdges(submission2, student2, Authorship())
        expectedGraph.addBothEdges(submission3, student3, Authorship())
        expectedGraph.addBothEdges(student1, semester, Enrollment())
        expectedGraph.addBothEdges(student2, semester, Enrollment())
        expectedGraph.addBothEdges(student3, semester, Enrollment())
        expectedGraph.addBothEdges(submission1, submission3, SameSemesterMatch(5000, 72.0))
        expectedGraph.addBothEdges(semester, assignment, SemesterAssignment())

        actualGraph = self.dataImporter.buildGraph(analysisData)

        self.assertGraphsEqual(expectedGraph, actualGraph)


    def testInvalidSameSemesterMatchAnalysis(self):
        """
          Tests that the graph is built correctly given some simple test analysis. This
          test case considers the case of:

            * Single assignment, single analysis, single semester
            * Three submissions
            * One (same semester) submission pair match

          Except, also includes extraneous data that should be discarded
        """

        # Setup CoMoTo data & expected graph
        analysisData = self.invalidSameSemesterMatchAnalysis

        student1 = Student(10001, 'Smith, John', 'johnsmith')
        student2 = Student(10002, 'Doe, Jane', 'janedoe')
        student3 = Student(10003, 'Smith, Joe', 'joesmith')
        submission1 = Submission(5001)
        submission2 = Submission(5002)
        submission3 = Submission(5003)
        assignment = Assignment(1, 'MP1')
        semester = Semester(7, 'Spring', 2011)

        expectedGraph = GraphFactory.createInstance()
        expectedGraph.addNode(student1)
        expectedGraph.addNode(student2)
        expectedGraph.addNode(student3)
        expectedGraph.addNode(submission1)
        expectedGraph.addNode(submission2)
        expectedGraph.addNode(submission3)
        expectedGraph.addNode(assignment)
        expectedGraph.addNode(semester)

        expectedGraph.addBothEdges(submission1, assignment, AssignmentSubmission())
        expectedGraph.addBothEdges(submission2, assignment, AssignmentSubmission())
        expectedGraph.addBothEdges(submission3, assignment, AssignmentSubmission())
        expectedGraph.addBothEdges(submission1, student1, Authorship())
        expectedGraph.addBothEdges(submission2, student2, Authorship())
        expectedGraph.addBothEdges(submission3, student3, Authorship())
        expectedGraph.addBothEdges(student1, semester, Enrollment())
        expectedGraph.addBothEdges(student2, semester, Enrollment())
        expectedGraph.addBothEdges(student3, semester, Enrollment())
        expectedGraph.addBothEdges(submission1, submission3, SameSemesterMatch(5000, 72.0))
        expectedGraph.addBothEdges(semester, assignment, SemesterAssignment())

        actualGraph = self.dataImporter.buildGraph(analysisData)

        self.assertGraphsEqual(expectedGraph, actualGraph)


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
        submission1 = Submission(5001, {5003})
        submission2 = Submission(5002)
        submission3 = Submission(5003, {5001})
        assignment = Assignment(1, 'MP1')
        semester = Semester(7, 'Spring', 2011)

        expectedGraph = GraphFactory.createInstance()
        expectedGraph.addNode(student1)
        expectedGraph.addNode(student2)
        expectedGraph.addNode(student3)
        expectedGraph.addNode(submission1)
        expectedGraph.addNode(submission2)
        expectedGraph.addNode(submission3)
        expectedGraph.addNode(assignment)
        expectedGraph.addNode(semester)

        expectedGraph.addBothEdges(submission1, assignment, AssignmentSubmission())
        expectedGraph.addBothEdges(submission2, assignment, AssignmentSubmission())
        expectedGraph.addBothEdges(submission3, assignment, AssignmentSubmission())
        expectedGraph.addBothEdges(submission1, student1, Authorship())
        expectedGraph.addBothEdges(submission2, student2, Authorship())
        expectedGraph.addBothEdges(submission3, student3, Authorship())
        expectedGraph.addBothEdges(student1, semester, Enrollment())
        expectedGraph.addBothEdges(student2, semester, Enrollment())
        expectedGraph.addBothEdges(student3, semester, Enrollment())
        expectedGraph.addBothEdges(submission1, submission3, PartnerMatch(5000, 72.0))
        expectedGraph.addBothEdges(semester, assignment, SemesterAssignment())

        actualGraph = self.dataImporter.buildGraph(analysisData)

        self.assertGraphsEqual(expectedGraph, actualGraph)


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
        solutionSubmission = Submission(5004, None, True)
        assignment = Assignment(1, 'MP1')
        semester = Semester(7, 'Spring', 2011)

        expectedGraph = GraphFactory.createInstance()
        expectedGraph.addNode(student1)
        expectedGraph.addNode(student2)
        expectedGraph.addNode(student3)
        expectedGraph.addNode(submission1)
        expectedGraph.addNode(submission2)
        expectedGraph.addNode(submission3)
        expectedGraph.addNode(solutionSubmission)
        expectedGraph.addNode(assignment)
        expectedGraph.addNode(semester)

        expectedGraph.addBothEdges(submission1, assignment, AssignmentSubmission())
        expectedGraph.addBothEdges(submission2, assignment, AssignmentSubmission())
        expectedGraph.addBothEdges(submission3, assignment, AssignmentSubmission())
        expectedGraph.addBothEdges(solutionSubmission, assignment, AssignmentSubmission())
        expectedGraph.addBothEdges(submission1, student1, Authorship())
        expectedGraph.addBothEdges(submission2, student2, Authorship())
        expectedGraph.addBothEdges(submission3, student3, Authorship())
        expectedGraph.addBothEdges(student1, semester, Enrollment())
        expectedGraph.addBothEdges(student2, semester, Enrollment())
        expectedGraph.addBothEdges(student3, semester, Enrollment())
        expectedGraph.addBothEdges(submission1, solutionSubmission, SolutionMatch(5000, 80))
        expectedGraph.addBothEdges(semester, assignment, SemesterAssignment())

        actualGraph = self.dataImporter.buildGraph(analysisData)

        self.assertGraphsEqual(expectedGraph, actualGraph)


    def testCrossSemesterMatchAnalyses(self):
        """
          Tests that the graph is built correctly given some more complex test analysis. This
          test case considers the case of:

            * Two assignments, two analyses, two semesters
            * Four submissions
            * One (cross semester) match
        """

        # Setup CoMoTo data & expected graph
        analysisData = self.crossSemesterMatchAnalysis

        student1 = Student(10001, 'Smith, John', 'johnsmith')
        student2 = Student(10002, 'Doe, Jane', 'janedoe')
        student3 = Student(10003, 'Smith, Joe', 'joesmith')
        student4 = Student(10004, 'Smith, Alex', 'alexsmith')
        submission1 = Submission(5001)
        submission2 = Submission(5002)
        submission3 = Submission(5003)
        submission4 = Submission(5004)
        assignment1 = Assignment(1, 'MP1')
        assignment2 = Assignment(2, 'MP2')
        semester1 = Semester(7, 'Spring', 2011)
        semester2 = Semester(8, 'Spring', 2012)

        expectedGraph = GraphFactory.createInstance()
        expectedGraph.addNode(student1)
        expectedGraph.addNode(student2)
        expectedGraph.addNode(student3)
        expectedGraph.addNode(student4)
        expectedGraph.addNode(submission1)
        expectedGraph.addNode(submission2)
        expectedGraph.addNode(submission3)
        expectedGraph.addNode(submission4)
        expectedGraph.addNode(assignment1)
        expectedGraph.addNode(assignment2)
        expectedGraph.addNode(semester1)
        expectedGraph.addNode(semester2)

        expectedGraph.addBothEdges(submission1, assignment1, AssignmentSubmission())
        expectedGraph.addBothEdges(submission2, assignment1, AssignmentSubmission())
        expectedGraph.addBothEdges(submission3, assignment1, AssignmentSubmission())
        expectedGraph.addBothEdges(submission4, assignment2, AssignmentSubmission())
        expectedGraph.addBothEdges(submission1, student1, Authorship())
        expectedGraph.addBothEdges(submission2, student2, Authorship())
        expectedGraph.addBothEdges(submission3, student3, Authorship())
        expectedGraph.addBothEdges(submission4, student4, Authorship())
        expectedGraph.addBothEdges(student1, semester1, Enrollment())
        expectedGraph.addBothEdges(student2, semester1, Enrollment())
        expectedGraph.addBothEdges(student3, semester1, Enrollment())
        expectedGraph.addBothEdges(student4, semester2, Enrollment())
        expectedGraph.addBothEdges(semester1, assignment1, SemesterAssignment())
        expectedGraph.addBothEdges(semester2, assignment2, SemesterAssignment())

        # Every type of edge should be symmetric, except for the cross-semester match (since current submissions can
        # match past submissions, but not vice versa)
        expectedGraph.addEdge(submission1, submission4, CrossSemesterMatch(5000, 72.0))

        # Test
        actualGraph = self.dataImporter.buildGraph(analysisData)

        # Verify
        self.assertGraphsEqual(expectedGraph, actualGraph)


    def testRetakingStudentAnalyses(self):
        """
          Tests that the graph is built correctly given some more complex test analysis. This
          test case considers the case of:

            * Two assignments, two analyses, two semesters
            * Five submissions, two by a single student (in two semesters)
            * One (cross semester) match between two submissions from the same student

          In this case, the match should be removed
        """

        # Setup CoMoTo data & expected graph
        analysisData = self.retakingStudentAnalysis

        student1 = Student(10001, 'Smith, John', 'johnsmith', True)
        student2 = Student(10002, 'Doe, Jane', 'janedoe')
        student3 = Student(10003, 'Smith, Joe', 'joesmith')
        student4 = Student(10004, 'Smith, Alex', 'alexsmith')
        submission2 = Submission(5002)
        submission3 = Submission(5003)
        submission4 = Submission(5004)
        submission5 = Submission(5005)
        assignment1 = Assignment(1, 'MP1')
        assignment2 = Assignment(2, 'MP2')
        semester1 = Semester(7, 'Spring', 2011)
        semester2 = Semester(8, 'Spring', 2012)

        expectedGraph = GraphFactory.createInstance()
        expectedGraph.addNode(student1)
        expectedGraph.addNode(student2)
        expectedGraph.addNode(student3)
        expectedGraph.addNode(student4)
        expectedGraph.addNode(submission2)
        expectedGraph.addNode(submission3)
        expectedGraph.addNode(submission4)
        expectedGraph.addNode(submission5)
        expectedGraph.addNode(assignment1)
        expectedGraph.addNode(assignment2)
        expectedGraph.addNode(semester1)
        expectedGraph.addNode(semester2)

        expectedGraph.addBothEdges(submission2, assignment1, AssignmentSubmission())
        expectedGraph.addBothEdges(submission3, assignment1, AssignmentSubmission())
        expectedGraph.addBothEdges(submission4, assignment2, AssignmentSubmission())
        expectedGraph.addBothEdges(submission5, assignment2, AssignmentSubmission())
        expectedGraph.addBothEdges(submission2, student2, Authorship())
        expectedGraph.addBothEdges(submission3, student3, Authorship())
        expectedGraph.addBothEdges(submission4, student1, Authorship())
        expectedGraph.addBothEdges(submission5, student4, Authorship())
        expectedGraph.addBothEdges(student1, semester2, Enrollment())
        expectedGraph.addBothEdges(student2, semester1, Enrollment())
        expectedGraph.addBothEdges(student3, semester1, Enrollment())
        expectedGraph.addBothEdges(student4, semester2, Enrollment())
        expectedGraph.addBothEdges(semester1, assignment1, SemesterAssignment())
        expectedGraph.addBothEdges(semester2, assignment2, SemesterAssignment())

        # Test
        actualGraph = self.dataImporter.buildGraph(analysisData)

        # Verify
        self.assertGraphsEqual(expectedGraph, actualGraph)
