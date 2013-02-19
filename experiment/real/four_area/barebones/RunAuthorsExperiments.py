from experiment.real.four_area.barebones import   AuthorsPathSimAPCPAExperiment, AuthorsNeighborSimPPAExperiment, AuthorsNeighborSimPPAAPCPAExperiment, AuthorsNeighborSimTPPAExperiment

__author__ = 'jontedesco'

# Standalone experiments
print("Running NeighborSim PPA experiment:")
citationCounts, publicationCounts = AuthorsNeighborSimPPAExperiment.run()
print("Running NeighborSim TPPA experiment:")
AuthorsNeighborSimTPPAExperiment.run(citationCounts, publicationCounts)
print("Running PathSim APCPA experiment:")
AuthorsPathSimAPCPAExperiment.run(citationCounts, publicationCounts)

# Combined/lazy experiments
print("Running NeighborSim PPA - PathSim APCPA experiment:")
AuthorsNeighborSimPPAAPCPAExperiment.run(citationCounts, publicationCounts)
print("Running NeighborSim PPA - PathSim APCPA experiment (0.3, 0.7):")
AuthorsNeighborSimPPAAPCPAExperiment.run(citationCounts, publicationCounts, weights = (0.3,0.7))
print("Running NeighborSim TPPA - PathSim APCPA experiment:")
AuthorsNeighborSimPPAAPCPAExperiment.run(citationCounts, publicationCounts)
print("Running NeighborSim TPPA - PathSim APCPA experiment (0.3, 0.7):")
AuthorsNeighborSimPPAAPCPAExperiment.run(citationCounts, publicationCounts, weights = (0.3,0.7))
