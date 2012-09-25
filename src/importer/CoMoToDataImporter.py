import logging
import xmlrpclib
import cPickle
from threading import Thread
from src.graph.GraphFactory import GraphFactory
from src.importer.error.CoMoToParseError import CoMoToParseError
from src.logger.ColoredLogger import ColoredLogger
from src.model.edge.comoto.AssignmentSubmission import AssignmentSubmission
from src.model.edge.comoto.Authorship import Authorship
from src.model.edge.comoto.Enrollment import Enrollment
from src.model.edge.comoto.SemesterAssignment import SemesterAssignment
from src.model.edge.comoto.matches.SameSemesterMatch import SameSemesterMatch
from src.model.edge.comoto.matches.CrossSemesterMatch import CrossSemesterMatch
from src.model.edge.comoto.matches.SolutionMatch import SolutionMatch
from src.model.edge.comoto.matches.PartnerMatch import PartnerMatch
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

        logging.setLoggerClass(ColoredLogger)
        self.logger = logging.getLogger('CoMoToDataImporter')

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

        try:

            self.logger.info("Fetching CoMoTo data")
            coMoToData = self.getCoMoToData()

            self.logger.info("Building CoMoTo graph data")
            graph = self.buildGraph(coMoToData)

            self.logger.info("Pickling CoMoTo graph data to file")
            with open(self.outputPath, 'w') as outputFile:
                cPickle.dump(graph, outputFile)

        except Exception, error:

            self.logger.error(error.__class__.__name__ + ": " + error.message)


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

        graph = GraphFactory.createInstance()

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

                graph.addNode(semester)

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
            graph.addNode(assignment)
            graph.addEdge(assignment, offeredSemester, semesterAssignmentEdge)
            graph.addEdge(offeredSemester, assignment, semesterAssignmentEdge)

        # Add submissions & students to graph, connect submissions with students and assignment,
        # and students with assignments
        submissions = {}
        students = {}
        submissionIdsRemoved = set()
        for analysisId in coMoToData['analysis_data']:
            analysisData = coMoToData['analysis_data'][analysisId]
            for submissionId in analysisData['submissions']:

                # Get submission data & add to graph
                submissionData = analysisData['submissions'][submissionId]
                isSolution = (submissionData['type'] == 'solutionsubmission')
                partnerIds = None if isSolution else set(submissionData['partner_ids'])
                submission = Submission(submissionId, partnerIds, isSolution)
                submissions[submissionId] = submission

                # Get semester corresponding to this submission
                submissionSemester = offeringIdToSemesterMap[submissionData['offering_id']]
                if submissionSemester is None:
                    raise CoMoToParseError('Failed to find semester corresponding to student')

                graph.addNode(submission)

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
                        studentNodePredecessors = graph.getPredecessors(student)
                        studentIsRetake = False
                        for node in studentNodePredecessors:
                            if isinstance(node, Semester) and node != submissionSemester:
                                studentIsRetake = True

                        # Remove all edges
                        if studentIsRetake:
                            student.retake = True

                            # Remove old enrollments & submissions for last semester
                            for node in studentNodePredecessors:
                                isSemester = isinstance(node, Semester) and node != submissionSemester
                                isSubmission = isinstance(node, Submission)

                                if isSemester or isSubmission:
                                    if graph.hasEdge(node, student):
                                        graph.removeEdge(node, student)
                                    if graph.hasEdge(student, node):
                                        graph.removeEdge(student, node)
                                if isSubmission:
                                    submissionIdsRemoved.add(node.id)
                                    graph.removeNode(node)

                            addEnrollmentEdge = True

                    if addEnrollmentEdge:
                        graph.addNode(student)
                        graph.addBothEdges(submissionSemester, student, Enrollment())

                    # We know that this student has only one submission for this offering, connect them in the graph
                    graph.addBothEdges(student, submission, Authorship())

                # Associate submission with assignment
                associatedAssignment = analysisIdToAssignmentMap[analysisId]
                if associatedAssignment is None:
                    raise CoMoToParseError('Failed to find assignment corresponding to submission')

                graph.addBothEdges(submission, associatedAssignment, AssignmentSubmission())

            matchTypeToClassMap = {
                'same_semester_matches': SameSemesterMatch,
                'cross_semester_matches': CrossSemesterMatch,
                'solution_matches': SolutionMatch
            }
            for matchType in matchTypeToClassMap.keys():
                for matchData in analysisData['matches'][matchType]:

                    # Don't add this match edge if we removed the submission cleaning retaking students before
                    if len({matchData['submission_1_id'], matchData['submission_2_id']}.intersection(submissionIdsRemoved)) is not 0:
                        continue

                    submissionOne = submissions[matchData['submission_1_id']]
                    submissionTwo = submissions[matchData['submission_2_id']]
                    averageScore = (float(matchData['score1']) + float(matchData['score2'])) / 2.0

                    isPartnerMatch = matchData['submission_1_id'] in submissionTwo.partnerIds \
                        or matchData['submission_2_id'] in submissionOne.partnerIds

                    if submissionOne is None:
                        raise CoMoToParseError('Failed to find submission 1 corresponding to match')
                    if submissionTwo is None:
                        raise CoMoToParseError('Failed to find submission 2 corresponding to match')

                    matchClass = matchTypeToClassMap[matchType]
                    if matchClass is SameSemesterMatch and isPartnerMatch:
                        matchClass = PartnerMatch

                    matchEdge = matchClass(matchData['id'], averageScore)
                    graph.addEdge(submissionOne, submissionTwo, matchEdge)

                    # If this is a cross semester match, don't make it bidirectional
                    if matchType != 'cross_semester_matches':
                        graph.addEdge(submissionTwo, submissionOne, matchEdge)

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
