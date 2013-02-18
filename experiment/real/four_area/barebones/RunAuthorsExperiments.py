from experiment.real.four_area.barebones import AuthorsNeighborSimAPPAExperiment, AuthorsNeighborSimCPPAExperiment, AuthorsPathSimAPCPAExperiment, AuthorsPathSimAPPAExperiment, AuthorsPathSimAPTPAExperiment, AuthorsNeighborSimAPPAAPCPAExperiment

__author__ = 'jontedesco'

print("Running NeighborSim APPA experiment:")
citationCounts = AuthorsNeighborSimAPPAExperiment.run()
print("Running NeighborSim APPA-APCPA experiment:")
citationCounts = AuthorsNeighborSimAPPAAPCPAExperiment.run()
print("Running NeighborSim CPPA experiment:")
AuthorsNeighborSimCPPAExperiment.run(citationCounts = citationCounts)
print("Running PathSim APCPA experiment:")
AuthorsPathSimAPCPAExperiment.run(citationCounts = citationCounts)
print("Running PathSim APPA experiment:")
AuthorsPathSimAPPAExperiment.run(citationCounts = citationCounts)
print("Running PathSim APTPA experiment:")
AuthorsPathSimAPTPAExperiment.run(citationCounts = citationCounts)