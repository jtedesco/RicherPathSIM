import unittest
from src.model.GraphObjectFactory import GraphObjectFactory
from src.model.node.comoto.Assignment import Assignment
from src.model.node.comoto.Semester import Semester
from src.model.node.dblp.Author import Author
from src.model.node.dblp.Conference import Conference
from src.model.node.dblp.Paper import Paper

__author__ = 'jontedesco'

class GraphObjectFactoryTest(unittest.TestCase):

    def testCreateDBLPNode(self):

        paperDict = {'type': 'Paper', 'id': 68, 'title': 'VLDB Paper 57'}
        expectedPaper = Paper(id=68, title='VLDB Paper 57')
        actualPaper = GraphObjectFactory.createDBLPNode(paperDict)
        self.assertEqual(actualPaper, expectedPaper)

        authorDict = {'type': 'Author', 'id': 0, 'name': 'Mike'}
        expectedAuthor = Author(id=0, name='Mike')
        actualAuthor = GraphObjectFactory.createDBLPNode(authorDict)
        self.assertEqual(actualAuthor, expectedAuthor)

        conferenceDict = {'type': 'Conference', 'id': 6, 'name': 'VLDB'}
        expectedConference = Conference(id=6, name='VLDB')
        actualConference = GraphObjectFactory.createDBLPNode(conferenceDict)
        self.assertEqual(actualConference, expectedConference)

    def testCreateCoMoToNode(self):

        assignmentDict = {'type': 'Assignment', 'id': 68, 'name': 'MP0'}
        expectedAssignment = Assignment(id=68, name='MP0')
        actualAssignment = GraphObjectFactory.createCoMoToNode(assignmentDict)
        self.assertEqual(actualAssignment, expectedAssignment)

        semesterDict = {'type': 'Semester', 'id': 0, 'season': 'Fall', 'year': 2008}
        expectedSemester = Semester(id=0, season='Fall', year=2008)
        actualSemester = GraphObjectFactory.createCoMoToNode(semesterDict)
        self.assertEqual(actualSemester, expectedSemester)