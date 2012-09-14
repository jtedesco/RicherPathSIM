import xmlrpclib
import networkx
from threading import Thread
from src.importer.error.CoMoToParseError import CoMoToParseError
from src.model.edge.comoto.AssignmentSubmission import AssignmentSubmission
from src.model.edge.comoto.Authorship import Authorship
from src.model.edge.comoto.Enrollment import Enrollment
from src.model.edge.comoto.SemesterAssignment import SemesterAssignment
from src.model.edge.comoto.matches.SameSemesterMatch import SameSemesterMatch
from src.model.node.comoto.Assignment import Assignment
from src.model.node.comoto.Semester import Semester
from src.model.node.comoto.Student import Student
from src.model.node.comoto.Submission import Submission


__author__ = 'jon'

class CoMoToDataImporter(Thread):
    """
      Imports CoMoTo CS 225 data into a python graph structure stored in NetworkX.
    """

    def __init__(self, outputPath, userName, password):
        """
          Constructs a thread to handle importing CoMoTo data from the CoMoTo API

            @param  outputPath  The path to which to write the generated graph (serialized using cPickle)
            @param  userName    The netid of user with access to the CoMoTo API
            @param  password    The AD password of user with access to the CoMoTo API
        """

        self.outputPath = outputPath
        self.userName = userName
        self.password = password

        super(CoMoToDataImporter, self).__init__()


    def run(self):
        """
          Import data from CoMoTo and save at output path as a graph. This happens in three steps:

          <ol>
            <li>Fetch the CoMoTo data from the server</li>
            <li>Create the heterogeneous graph of CoMoTo data</li>
            <li>Use cPickle to dump the bytes of the graph to disk</li>
          </ol>
        """

        coMoToData = self.getCoMoToData()
        graph = self.buildGraph(coMoToData)


    def getCoMoToData(self):
        """
          Gets all CoMoTo data necessary for building the graph
        """

        # Attempt to login & create a connection to the CoMoTo API
        connection = xmlrpclib.Server(
            "https://%s:%s@comoto.cs.illinois.edu/comoto/api" % (self.userName, self.password)
        )

        # Get the list of courses, offerings, assignments,filesets, and additional class data available from the API
        courses = connection.getCourses(True)

        # Find CS 225, the semesters/offerings, and get the assignments
        offerings = []
        assignments = []
        for course in courses:
            if course['name'] == 'CS 225':
                assignments = connection.getAssignments(course['id'])
                offerings = course['offerings']

        fileSetIdsList = []
        analysisIds = []
        for assignment in assignments:
            fileSetIdsList.append(assignment['fileset_ids'])
            analysisId = assignment['analysis_id']
            if analysisId > 0:
                analysisIds.append(analysisId)

        # Associate offerings with analyses (bypass fileset ids)
        fileSetAnalysisMap = {}
        for analysisId, fileSetIds in zip(analysisIds, fileSetIdsList):
            for fileSetId in fileSetIds:
                fileSetAnalysisMap[fileSetId] = analysisId
        for offering in offerings:
            if len(offering['fileset_ids']):
                aFileSetId = offering['fileset_ids'][0]
                offering['analysis_id'] = fileSetAnalysisMap[aFileSetId]

        # Get the match & submission data for each analysis
        analysisData = {}
        for analysisId, fileSetIds in zip(analysisIds, fileSetIdsList):
            analysisData[analysisId] = self.__getMatchesAndSubmissions(analysisId, fileSetIds, connection)

        return {
            'offerings': offerings, # Offerings of the class
            'assignments': assignments, # Assignments (in a particular semester, associated with individual analyses)
            'analysis_data': analysisData # Contains submissions & student data
        }


    def buildGraph(self, coMoToData):

        graph = networkx.DiGraph()

        # Add semesters to graph
        semesterIdToSemesterMap = {}
        offeringIdToSemesterMap = {}
        for offeringId in coMoToData['offerings']:

            semesterData = coMoToData['offerings'][offeringId]['semester']

            # Skip invalid or dummy semesters
            if semesterData['id'] >= 0 and semesterData['year'] >= 0:

                semester = Semester(semesterData['id'], semesterData['season'], semesterData['year'])
                semesterIdToSemesterMap[semesterData['id']] = semester
                offeringIdToSemesterMap[offeringId] = semester

                graph.add_node(semester)

        # Add assignments to graph & connect them to semesters
        analysisIdToAssignmentMap = {}
        for assignmentId in coMoToData['assignments']:

            # Skip invalid / dummy assignments
            if assignmentId < 0:
                continue

            assignmentData = coMoToData['assignments'][assignmentId]
            assignment = Assignment(assignmentId, assignmentData['name'])
            offeredSemester = semesterIdToSemesterMap[assignmentData['moss_analysis_pruned_offering']['semester']['id']]
            if offeredSemester is None:
                raise CoMoToParseError('Failed to find semester corresponding to assignment')
            analysisIdToAssignmentMap[assignmentData['analysis_id']] = assignment

            semesterAssignmentEdge = SemesterAssignment()
            graph.add_node(assignment)
            graph.add_edge(assignment, offeredSemester, semesterAssignmentEdge.toDict())
            graph.add_edge(offeredSemester, assignment, semesterAssignmentEdge.toDict())

        # Add submissions & students to graph, connect submissions with students and assignment,
        # and students with assignments
        submissions = {}
        students = {}
        for analysisId in coMoToData['analysis_data']:
            analysisData = coMoToData['analysis_data'][analysisId]
            for submissionId in analysisData['submissions']:

                # Get submission data & add to graph
                submissionData = analysisData['submissions'][submissionId]
                isSolution = (submissionData['type'] == 'solutionsubmission')
                submission = Submission(submissionId, isSolution)
                submissions[submissionId] = submission

                # Get semester corresponding to this submission
                submissionSemester = offeringIdToSemesterMap[submissionData['offering_id']]
                if submissionSemester is None:
                    raise CoMoToParseError('Failed to find semester corresponding to student')

                graph.add_node(submission)

                if not isSolution:

                    studentId = submissionData['student']['id']
                    addEnrollmentEdge = False
                    if studentId not in students:

                        # Add student data to the graph if not already encountered
                        studentData = submissionData['student']
                        student = Student(studentId, studentData['display_name'], studentData['netid'])
                        students[studentId] = student

                        # We know that student is not associated with this offering yet, just add him/her & corresponding
                        # enrollment edges to graph
                        addEnrollmentEdge = True

                    else:

                        # Get student encountered before
                        student = students[studentId]

                        # Check all incoming edges to student node for connections to another (different) analysis
                        studentNodePredecessors = graph.predecessors(student)
                        studentIsRetake = False
                        for node in studentNodePredecessors:
                            if isinstance(node, Semester) and node != submissionSemester:
                                studentIsRetake = True

                        # Remove all edges
                        if studentIsRetake:
                            student.retake = True

                            # Remove old enrollments & submissions for last semester
                            for node in studentNodePredecessors:
                                if isinstance(node, Semester) and node != submissionSemester:
                                    graph.remove_edge(node, student)
                                    graph.remove_edge(student, node)
                                elif isinstance(node, Submission):
                                    graph.remove_edge(node, student)
                                    graph.remove_edge(student, node)
                                    graph.remove_node(node)


                            addEnrollmentEdge = True

                    if addEnrollmentEdge:
                        enrollmentEdge = Enrollment()
                        graph.add_node(student)
                        graph.add_edge(submissionSemester, student, enrollmentEdge.toDict())
                        graph.add_edge(student, submissionSemester, enrollmentEdge.toDict())

                    # We know that this student has only one submission for this offering, connect them in the graph
                    authorshipEdge = Authorship()
                    graph.add_edge(student, submission, authorshipEdge.toDict())
                    graph.add_edge(submission, student, authorshipEdge.toDict())

                # Associate submission with assignment
                associatedAssignment = analysisIdToAssignmentMap[analysisId]
                if associatedAssignment is None:
                    raise CoMoToParseError('Failed to find assignment corresponding to submission')

                assignmentSubmissionEdge = AssignmentSubmission()
                graph.add_edge(submission, associatedAssignment, assignmentSubmissionEdge.toDict())
                graph.add_edge(associatedAssignment, submission, assignmentSubmissionEdge.toDict())

            for sameSemesterMatchData in analysisData['matches']['same_semester_matches']:

                submissionOne = submissions[sameSemesterMatchData['submission_1_id']]
                submissionTwo = submissions[sameSemesterMatchData['submission_2_id']]
                averageScore = (float(sameSemesterMatchData['score1']) + float(sameSemesterMatchData['score2'])) / 2.0

                if submissionOne is None:
                    raise CoMoToParseError('Failed to find submission 1 corresponding to match')
                if submissionTwo is None:
                    raise CoMoToParseError('Failed to find submission 2 corresponding to match')

                sameSemesterMatchEdge = SameSemesterMatch(sameSemesterMatchData['id'], averageScore)
                graph.add_edge(submissionOne, submissionTwo, sameSemesterMatchEdge.toDict())
                graph.add_edge(submissionTwo, submissionOne, sameSemesterMatchEdge.toDict())

            # TODO: Handle cross-semester matches
            # TODO: Handle solution matches

        return graph


    def __getMatchesAndSubmissions(self, analysisId, fileSetIds, connection):
        """
          Get the code submissions and submission matches for a particular analysis
        """

        # Get the analysis & assignment data for this id
        analysis = connection.getAnalysis(analysisId)

        # Get the MOSS matches for this assignment
        sameSemesterMatches =\
        connection.getMossAnalysis(analysis['moss_analysis_id'], True, 0)['same_semester_matches']
        solutionMatches = connection.getMossAnalysis(analysis['moss_analysis_id'], True, 0)['solution_matches']
        crossSemesterMatches =\
        connection.getMossAnalysis(analysis['moss_analysis_id'], True, 0)['cross_semester_matches']
        matches = {
            'same_semester_matches': sameSemesterMatches,
            'solution_matches': solutionMatches,
            'cross_semester_matches': crossSemesterMatches
        }

        # Get the submissions for this semester
        fileSets = connection.getFileSets(fileSetIds, True)
        submissions = {}
        for fileSet in fileSets:
            for submission in fileSet['submissions']:
                submissions[submission['id']] = submission

        # Encode the submissions & matches to send them back
        return {
            'matches' : matches,
            'submissions' : submissions
        }
