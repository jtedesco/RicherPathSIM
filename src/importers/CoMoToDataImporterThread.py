import xmlrpc.client
from threading import Thread
import networkx

__author__ = 'jon'

class CoMoToDataImporterThread(Thread):
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

        super(CoMoToDataImporterThread, self).__init__()


    def run(self):
        """
          Import data from CoMoTo and save at output path as a graph. This happens in three steps:

          <ol>
            <li>Fetch the CoMoTo data from the server</li>
            <li>Create the heterogeneous graph of CoMoTo data</li>
            <li>Use cPickle to dump the bytes of the graph to disk</li>
          </ol>
        """

        coMoToData = self.__getCoMoToData()
        graph = self.__buildGraph(coMoToData)


    def __getCoMoToData(self):
        """
          Gets all CoMoTo data necessary for building the graph
        """

        # Attempt to login & create a connection to the CoMoTo API
        connection = xmlrpc.client.Server(
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
            if not len(analysisIds): # TODO: Remove this to collect more than one assignment
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
            aFileSetId = offering['fileset_ids'][0]
            offering['analysis_id'] = fileSetAnalysisMap[aFileSetId]

        # Get the match & submission data for each analysis
        analysisData = {}
        for analysisId, fileSetIds in zip(analysisIds, fileSetIdsList):
            analysisData[analysisId] = self.__getMatchesAndSubmissions(analysisId, fileSetIds, connection)

        return {
            'offerings': offerings, # Offerings of the class
            'assignments': assignments, # Assignments (in a particular semester, associated with individual analyses)
            'analysisData': analysisData # Contains submissions & student data
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
            'sameSemesterMatches': sameSemesterMatches,
            'solutionMatches': solutionMatches,
            'crossSemesterMatches': crossSemesterMatches
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

    def __buildGraph(self, coMoToData):

        graph = networkx.DiGraph()
        return graph