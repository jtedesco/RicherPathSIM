from copy import deepcopy
from src.model.edge.comoto.AssignmentSubmission import AssignmentSubmission
from src.model.edge.comoto.Authorship import Authorship as CoMoToAuthorship
from src.model.edge.comoto.Enrollment import Enrollment
from src.model.edge.comoto.Match import Match
from src.model.edge.comoto.SemesterAssignment import SemesterAssignment
from src.model.edge.comoto.matches.CrossSemesterMatch import CrossSemesterMatch
from src.model.edge.comoto.matches.PartnerMatch import PartnerMatch
from src.model.edge.comoto.matches.SameSemesterMatch import SameSemesterMatch
from src.model.edge.comoto.matches.SolutionMatch import SolutionMatch
from src.model.edge.dblp.Authorship import Authorship as DBLPAuthorship
from src.model.edge.dblp.Citation import Citation
from src.model.edge.dblp.Containment import Containment
from src.model.edge.dblp.Mention import Mention
from src.model.edge.dblp.Publication import Publication
from src.model.node.comoto.Assignment import Assignment
from src.model.node.comoto.Semester import Semester
from src.model.node.comoto.Student import Student
from src.model.node.comoto.Submission import Submission
from src.model.node.dblp.Author import Author
from src.model.node.dblp.Conference import Conference
from src.model.node.dblp.Paper import Paper
from src.model.node.dblp.Topic import Topic

__author__ = 'jontedesco'

class GraphObjectFactory(object):
    """
      Factory that handles creation of graph nodes and edges
    """

    # Map of types to classes for DBLP & CoMoTo (kept separately, since type names may overlap between the two domains
    dblpTypeMap = {
        'Author': Author,
        'Authorship': DBLPAuthorship,
        'Citation': Citation,
        'Containment': Containment,
        'Conference': Conference,
        'Mention': Mention,
        'Paper': Paper,
        'Publication': Publication,
        'Topic': Topic
    }
    comotoTypeMap = {
        'Assignment': Assignment,
        'AssignmentSubmission': AssignmentSubmission,
        'Authorship': CoMoToAuthorship,
        'CrossSemesterMatch': CrossSemesterMatch,
        'Enrollment': Enrollment,
        'Match': Match,
        'PartnerMatch': PartnerMatch,
        'SameSemesterMatch': SameSemesterMatch,
        'Semester': Semester,
        'SemesterAssignment': SemesterAssignment,
        'SolutionMatch': SolutionMatch,
        'Student': Student,
        'Submission': Submission
    }

    @staticmethod
    def createDBLPNode(dictionary):
        """
          Create a DBLP graph node given the dictionary data for that node
        """

        nodeClass = GraphObjectFactory.dblpTypeMap[dictionary['type']]
        remainingDictionary = deepcopy(dictionary)
        del remainingDictionary['type']
        return nodeClass(**remainingDictionary)

    @staticmethod
    def createCoMoToNode(dictionary):

        nodeClass = GraphObjectFactory.comotoTypeMap[dictionary['type']]
        remainingDictionary = deepcopy(dictionary)
        del remainingDictionary['type']
        return nodeClass(**remainingDictionary)
