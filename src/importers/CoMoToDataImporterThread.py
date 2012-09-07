import xmlrpc.client
import networkx as nx
from threading import Thread

__author__ = 'jon'

class CoMoToDataImporterThread(Thread):
    """
      Imports CoMoTo CS 225 data into a python graph structure stored in NetworkX.
    """

    def __init__(self, outputPath, userName, password):

        self.outputPath = outputPath
        self.userName = userName
        self.password = password

        # XML-RPC client connection
        self.connection = None

        # Graph structure to create
        self.graph = nx.Graph()

        super(CoMoToDataImporterThread, self).__init__()

    def run(self):

        # Attempt to login & create a connection to the CoMoTo API
        self.connection = xmlrpc.client.Server(
            "https://%s:%s@comoto.cs.illinois.edu/comoto/api" % (self.userName, self.password)
        )

        # Get the list of courses, offerings, assignments,filesets, and additional class data available from the API
        courses = self.connection.getCourses(True)

        # Get the assignment data for each course
        fileSetIdsList = []
        analysisIds = []
        for course in courses:
            if course['name'] == 'CS 225':
                course['assignments'] = self.connection.getAssignments(course['id'])
                for assignment in course['assignments']:
                    if not len(analysisIds): # TODO: Remove this to collect more than one assignment
                        fileSetIdsList.append(assignment['fileset_ids'])
                        analysisId = assignment['analysis_id']
                        if analysisId > 0:
                            analysisIds.append(analysisId)

        # Get the match & submission data for each analysis
        analysisData = {}
        for analysisId, fileSetIds in zip(analysisIds, fileSetIdsList):
            analysisData[analysisId] = self.__getMatchesAndSubmissions((analysisId, fileSetIds))


    def __getMatchesAndSubmissions(self, data):

        analysisId, fileSetIds = data

        # Get the analysis & assignment data for this id
        analysis = self.connection.getAnalysis(analysisId)

        # Get the MOSS matches for this assignment
        sameSemesterMatches =\
            self.connection.getMossAnalysis(analysis['moss_analysis_id'], True, 0)['same_semester_matches']
        solutionMatches = self.connection.getMossAnalysis(analysis['moss_analysis_id'], True, 0)['solution_matches']
        crossSemesterMatches =\
            self.connection.getMossAnalysis(analysis['moss_analysis_id'], True, 0)['cross_semester_matches']
        matches = {
            'sameSemesterMatches': sameSemesterMatches,
            'solutionMatches': solutionMatches,
            'crossSemesterMatches': crossSemesterMatches
        }

        # Get the submissions for this semester
        fileSets = self.connection.getFileSets(fileSetIds, True)
        submissions = {}
        for fileSet in fileSets:
            for submission in fileSet['submissions']:
                submissions[submission['id']] = submission

        # Encode the submissions & matches to send them back
        return {
            'matches' : matches,
            'submissions' : submissions
        }