from experiment.real.four_area.barebones import   AuthorsPathSimAPCPAExperiment, AuthorsNeighborSimPPAExperiment, AuthorsNeighborSimPPAAPCPAExperiment

__author__ = 'jontedesco'

# Standalone experiments
print("Running NeighborSim PPA experiment:")
citationCounts, publicationCounts = AuthorsNeighborSimPPAExperiment.run()
#print("Running NeighborSim APPA experiment:")
#AuthorsNeighborSimAPPAExperiment.run(citationCounts, publicationCounts)
#print("Running NeighborSim CPPA experiment:")
#AuthorsNeighborSimCPPAExperiment.run(citationCounts, publicationCounts)
print("Running PathSim APCPA experiment:")
AuthorsPathSimAPCPAExperiment.run(citationCounts, publicationCounts)
#print("Running PathSim APPA experiment:")
#AuthorsPathSimAPPAExperiment.run(citationCounts, publicationCounts)
#print("Running PathSim APTPA experiment:")
#AuthorsPathSimAPTPAExperiment.run(citationCounts, publicationCounts)

# Combined/lazy experiments
print("Running NeighborSim PPA - PathSim APCPA experiment:")
AuthorsNeighborSimPPAAPCPAExperiment.run(citationCounts, publicationCounts)
print("Running NeighborSim PPA - PathSim APCPA experiment (0.4, 0.6:")
AuthorsNeighborSimPPAAPCPAExperiment.run(citationCounts, publicationCounts, weights = (0.4,0.6))
print("Running NeighborSim PPA - PathSim APCPA experiment (0.6, 0.4:")
AuthorsNeighborSimPPAAPCPAExperiment.run(citationCounts, publicationCounts, weights = (0.6,0.4))
print("Running NeighborSim PPA - PathSim APCPA experiment (0.3, 0.7:")
AuthorsNeighborSimPPAAPCPAExperiment.run(citationCounts, publicationCounts, weights = (0.3,0.7))
print("Running NeighborSim PPA - PathSim APCPA experiment (0.2, 0.8:")
AuthorsNeighborSimPPAAPCPAExperiment.run(citationCounts, publicationCounts, weights = (0.2,0.8))
print("Running NeighborSim PPA - PathSim APCPA experiment (0.1, 0.9:")
AuthorsNeighborSimPPAAPCPAExperiment.run(citationCounts, publicationCounts, weights = (0.1,0.9))