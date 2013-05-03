import cPickle
import os
from scipy.sparse import lil_matrix
import texttable
from experiment.Experiment import Experiment
from experiment.real.four_area.helper.MetaPathHelper import findMostSimilarNodes, getMetaPathAdjacencyData, testAuthors

__author__ = 'jontedesco'


class AuthorsPathSimAPPCPPAExperiment(Experiment):
    """
      Runs some experiments with PathSim on author similarity for the 'four area' dataset
    """

    def runFor(self, author, adjMatrix, extraData, citationCounts, publicationCounts):
        print("Running for %s..." % author)

        # Find the top 10 most similar nodes to some given node
        mostSimilar, similarityScores = findMostSimilarNodes(adjMatrix, author, extraData)
        self.output('\nMost Similar to "%s":' % author)
        mostSimilarTable = texttable.Texttable()
        rows = [['Author', 'Score', 'Citations', 'Publications']]
        rows += [[name, score, citationCounts[name], publicationCounts[name]] for name, score in mostSimilar]
        mostSimilarTable.add_rows(rows)
        self.output(mostSimilarTable.draw())

        # Output all similarity scores
        outputPath = os.path.join('../../results', 'authors', 'intermediate', '%s-pathsim-appcppa' % author.replace(' ', ''))
        cPickle.dump(similarityScores, open(outputPath, 'wb'))


def run(citationCounts, publicationCounts):
    experiment = AuthorsPathSimAPPCPPAExperiment(
        None,
        'Most Similar APPCPPA PathSim Authors',
        outputFilePath = os.path.join('../../results','authors','appcppaPathSim')
    )

    # Compute once, since these never change
    graph, nodeIndex = cPickle.load(open(os.path.join('../../data', 'graphWithCitations')))

    # Compute APCPA adjacency matrix
    apcAdjMatrix, extraData = getMetaPathAdjacencyData(graph, nodeIndex, ['author', 'paper', 'paper', 'conference'], rows=True)
    cpaAdjMatrix = apcAdjMatrix.transpose()
    apcpaAdjMatrix = lil_matrix(apcAdjMatrix * cpaAdjMatrix)

    # Correct the toNodes content in extraData
    extraData['toNodes'] = extraData['fromNodes']
    extraData['toNodesIndex'] = extraData['fromNodesIndex']

    for testAuthor in testAuthors:
        experiment.runFor(testAuthor, apcpaAdjMatrix, extraData, citationCounts, publicationCounts)
