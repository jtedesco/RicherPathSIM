import logging
import os
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

        # Bad analysis ids to skip from CoMoTo data
        self.analysisIdsToSkip = {51, 98, 95, 108, 76}

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


        self.logger.info("Fetching CoMoTo data")
        coMoToData = self.getCoMoToData()

        self.logger.info("Building CoMoTo graph data")
        graph = self.buildGraph(coMoToData)

        self.logger.info("Pickling CoMoTo graph data to file")
        with open(self.outputPath, 'w') as outputFile:
            cPickle.dump(graph, outputFile)


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
                assert(len(assignments) == 0)
                assignments = connection.getAssignments(course['id'])
                assert(len(offerings) == 0)
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
            semesterData = offering['semester']

            # Skip invalid semesters and semesters that are too new to have analyses
            if semesterData['id'] < 0 or semesterData['year'] <= 0:
                continue
            if semesterData['year'] == 2012 and semesterData['season'] == 'Fall':
                continue

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


    def buildGraph(self, coMoToData):

        graph = GraphFactory.createInstance()

        # Add semesters to graph
        analysisIdToAssignmentMap, offeringIdToSemesterMap = self.__addSemestersAndAssignmentsToGraph(coMoToData, graph)

        # Add submissions & students to graph, connect submissions with students and assignment, and students with assignments
        self.addStudentsAndSemestersToGraph(analysisIdToAssignmentMap, coMoToData, graph, offeringIdToSemesterMap)

        return graph


    def __addSemestersAndAssignmentsToGraph(self, coMoToData, graph):
        """
          Add semesters and assignments to the graph (assumes graph is empty)
        """

        semesterIdToSemesterMap = {}
        offeringIdToSemesterMap = {}
        for offeringData in coMoToData['offerings']:
            offeringId = offeringData['id']
            semesterData = offeringData['semester']

            # Skip invalid or dummy semesters
            if semesterData['id'] >= 0 and semesterData['year'] >= 0:
                semester = Semester(semesterData['id'], semesterData['season'], semesterData['year'])
                semesterIdToSemesterMap[semesterData['id']] = semester
                offeringIdToSemesterMap[offeringId] = semester

                graph.addNode(semester)

        # Add assignments to graph & connect them to semesters
        analysisIdToAssignmentMap = {}
        for assignmentData in coMoToData['assignments']:

            # Skip invalid / dummy assignments
            if assignmentData['id'] < 0:
                continue

            # For assignments not pruned by offering, delegate to manual map of semesters
            if len(assignmentData['moss_analysis_pruned_offering']) > 0:
                offeredSemester = semesterIdToSemesterMap[assignmentData['moss_analysis_pruned_offering']['semester']['id']]
            else:
                offeredSemester = self.__explicitlyCategorizeAssignment(assignmentData, semesterIdToSemesterMap)

            # For assignments where we couldn't resolve semester, skip
            if offeredSemester is None:
                continue

            assignment = Assignment(assignmentData['id'], assignmentData['name'])
            analysisIdToAssignmentMap[assignmentData['analysis_id']] = assignment

            semesterAssignmentEdge = SemesterAssignment()
            graph.addNode(assignment)
            graph.addEdge(assignment, offeredSemester, semesterAssignmentEdge)
            graph.addEdge(offeredSemester, assignment, semesterAssignmentEdge)

        return analysisIdToAssignmentMap, offeringIdToSemesterMap


    def __explicitlyCategorizeAssignment(self, assignmentData, semesterIdToSemesterMap):
        """
          Use a manually created map to categorize the assignment if not pruned to semester in DB
        """

        def findSemester(season, year):
            for id in semesterIdToSemesterMap:
                if semesterIdToSemesterMap[id].season == season and semesterIdToSemesterMap[id].year == year:
                    return semesterIdToSemesterMap[id]
            return None

        assignmentName = assignmentData['name']
        if 'Spring 2010' in assignmentName:
            return findSemester('Spring', 2010)
        elif 'su11' in assignmentName:
            return findSemester('Summer', 2011)
        elif 'Fall2011' in assignmentName:
            return findSemester('Fall', 2011)
        elif 'su12' in assignmentName:
            return findSemester('Summer', 2012)

        return None


    def __addExistingStudentToGraph(self, addEnrollmentEdge, graph, studentId, students, submissionIdsRemoved,
                                    submissionSemester):
        """
          Add an existing student to the graph, given the student id and map of existing students
        """

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
                    submissionIdsRemoved.add(int(node.id))
                    graph.removeNode(node)

            addEnrollmentEdge = True
        return addEnrollmentEdge, student


    def addStudentsAndSemestersToGraph(self, analysisIdToAssignmentMap, coMoToData, graph, offeringIdToSemesterMap):
        """
          Add the student and semester nodes (and corresponding enrollment edges) to graph (assuming all
          semester / assignment data has been added to graph.
        """

        submissions = {}
        students = {}
        submissionIdsRemoved = set()
        for analysisId in coMoToData['analysis_data']:

            # Skip known bad analyses
            if int(analysisId) not in analysisIdToAssignmentMap and int(analysisId) in self.analysisIdsToSkip:
                for submissionId in coMoToData['analysis_data'][analysisId]['submissions']:
                    submissionIdsRemoved.add(int(submissionId))
                continue

            analysisData = coMoToData['analysis_data'][analysisId]
            for submissionId in analysisData['submissions']:
                submissionData = analysisData['submissions'][submissionId]

                # Skip useless submissions
                if submissionData['type'] not in {'solutionsubmission', 'studentsubmission'}:
                    continue

                # Get submission data & add to graph
                isSolution = (submissionData['type'] == 'solutionsubmission')
                partnerIds = None if isSolution else set(submissionData['partner_ids'])
                submission = Submission(int(submissionId), partnerIds, isSolution)
                submissions[submissionId] = submission

                graph.addNode(submission)

                if not isSolution:

                    # Get semester corresponding to this submission
                    submissionSemester = offeringIdToSemesterMap[submissionData['offering_id']]
                    if submissionSemester is None:
                        raise CoMoToParseError('Failed to find semester corresponding to student')

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
                        addEnrollmentEdge, student = self.__addExistingStudentToGraph(addEnrollmentEdge, graph,
                            studentId, students, submissionIdsRemoved, submissionSemester)

                    if addEnrollmentEdge:
                        graph.addNode(student)
                        graph.addBothEdges(submissionSemester, student, Enrollment())

                    # We know that this student has only one submission for this offering, connect them in the graph
                    graph.addBothEdges(student, submission, Authorship())

                # Associate submission with assignment
                associatedAssignment = analysisIdToAssignmentMap[int(analysisId)]
                if associatedAssignment is None:
                    raise CoMoToParseError('Failed to find assignment corresponding to submission')

                graph.addBothEdges(submission, associatedAssignment, AssignmentSubmission())

        for analysisId in coMoToData['analysis_data']:
            self.__addMatchesToGraph(coMoToData['analysis_data'][analysisId], graph, submissionIdsRemoved, submissions)


    def __addMatchesToGraph(self, analysisData, graph, submissionIdsRemoved, submissions):
        """
          Add match edges to graph (assuming all other data has been added to graph)
        """

        matchTypeToClassMap = {
            'same_semester_matches': SameSemesterMatch,
            'cross_semester_matches': CrossSemesterMatch,
            'solution_matches': SolutionMatch
        }

        for matchType in matchTypeToClassMap.keys():
            for matchData in analysisData['matches'][matchType]:

                # Don't add this match edge if we removed the submission cleaning retaking students before
                if len({matchData['submission_1_id'], matchData['submission_2_id']}.intersection(
                    submissionIdsRemoved)) is not 0:
                    continue

                if str(matchData['submission_1_id']) not in submissions:
                    raise CoMoToParseError(
                        'Failed to find submission 1 corresponding to match for id %d' % matchData['submission_1_id']
                    )
                if str(matchData['submission_2_id']) not in submissions:
                    raise CoMoToParseError(
                        'Failed to find submission 2 corresponding to match for id %d' % matchData['submission_2_id']
                    )

                submissionOne = submissions[str(matchData['submission_1_id'])]
                submissionTwo = submissions[str(matchData['submission_2_id'])]
                averageScore = (float(matchData['score1']) + float(matchData['score2'])) / 2.0

                isPartnerMatch = matchData['submission_1_id'] in submissionTwo.partnerIds\
                    or matchData['submission_2_id'] in submissionOne.partnerIds

                matchClass = matchTypeToClassMap[matchType]
                if matchClass is SameSemesterMatch and isPartnerMatch:
                    matchClass = PartnerMatch

                matchEdge = matchClass(matchData['id'], averageScore)
                graph.addEdge(submissionOne, submissionTwo, matchEdge)

                # If this is a cross semester match, don't make it bidirectional
                if matchType != 'cross_semester_matches':
                    graph.addEdge(submissionTwo, submissionOne, matchEdge)


if __name__ == '__main__':
    netid = raw_input("Netid:")
    password = raw_input("Password:")
    comotoDataImporter = CoMoToDataImporter(os.path.join('graphs','cs225comotodata'), netid, password)
    comotoDataImporter.start()