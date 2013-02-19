from experiment.real.four_area.barebones import AuthorsNeighborSimAPPAExperiment, AuthorsNeighborSimCPPAExperiment, AuthorsPathSimAPCPAExperiment, AuthorsPathSimAPPAExperiment, AuthorsPathSimAPTPAExperiment, AuthorsNeighborSimAPPAAPCPAExperiment, AuthorsNeighborSimPPAExperiment

__author__ = 'jontedesco'

# Standalone experiments
print("Running NeighborSim APPA experiment:")
citationCounts = AuthorsNeighborSimAPPAExperiment.run()
print("Running NeighborSim PPA experiment:")
AuthorsNeighborSimPPAExperiment.run(citationCounts = citationCounts)
print("Running NeighborSim CPPA experiment:")
AuthorsNeighborSimCPPAExperiment.run(citationCounts = citationCounts)
print("Running PathSim APCPA experiment:")
AuthorsPathSimAPCPAExperiment.run(citationCounts = citationCounts)
print("Running PathSim APPA experiment:")
AuthorsPathSimAPPAExperiment.run(citationCounts = citationCounts)
print("Running PathSim APTPA experiment:")
AuthorsPathSimAPTPAExperiment.run(citationCounts = citationCounts)

# Combined/lazy experiments
print("Running NeighborSim APPA - PathSim APCPA experiment:")
AuthorsNeighborSimAPPAAPCPAExperiment.run(citationCounts = citationCounts)
print("Running NeighborSim APPA - PathSim APCPA experiment (0.4, 0.6:")
AuthorsNeighborSimAPPAAPCPAExperiment.run(citationCounts = citationCounts, weights = (0.4,0.6))
print("Running NeighborSim APPA - PathSim APCPA experiment (0.6, 0.4:")
AuthorsNeighborSimAPPAAPCPAExperiment.run(citationCounts = citationCounts, weights = (0.6,0.4))
print("Running NeighborSim APPA - PathSim APCPA experiment (0.3, 0.7:")
AuthorsNeighborSimAPPAAPCPAExperiment.run(citationCounts = citationCounts, weights = (0.3,0.7))
print("Running NeighborSim APPA - PathSim APCPA experiment (0.2, 0.8:")
AuthorsNeighborSimAPPAAPCPAExperiment.run(citationCounts = citationCounts, weights = (0.2,0.8))
print("Running NeighborSim APPA - PathSim APCPA experiment (0.1, 0.9:")
AuthorsNeighborSimAPPAAPCPAExperiment.run(citationCounts = citationCounts, weights = (0.1,0.9))