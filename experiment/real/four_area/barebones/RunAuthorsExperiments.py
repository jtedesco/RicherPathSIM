from experiment.real.four_area.barebones import AuthorsNeighborSimAPPAExperiment, AuthorsNeighborSimCPPAExperiment, AuthorsPathSimAPCPAExperiment, AuthorsPathSimAPPAExperiment, AuthorsPathSimAPTPAExperiment, AuthorsNeighborSimAPPAAPCPAExperiment

__author__ = 'jontedesco'

# Standalone experiments
print("Running NeighborSim APPA experiment:")
citationCounts = AuthorsNeighborSimAPPAExperiment.run()
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
citationCounts = AuthorsNeighborSimAPPAAPCPAExperiment.run()
