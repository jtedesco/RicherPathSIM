from experiment.real.four_area.barebones import AuthorsNeighborSimAPPAExperiment, AuthorsNeighborSimCPPAExperiment, AuthorsPathSimAPCPAExperiment, AuthorsPathSimAPPAExperiment, AuthorsPathSimAPTPAExperiment

__author__ = 'jontedesco'

print("Running NeighborSim APPA experiment:")
AuthorsNeighborSimAPPAExperiment.run()
print("Running NeighborSim CPPA experiment:")
AuthorsNeighborSimCPPAExperiment.run()
print("Running PathSim APCPA experiment:")
AuthorsPathSimAPCPAExperiment.run()
print("Running PathSim APPA experiment:")
AuthorsPathSimAPPAExperiment.run()
print("Running PathSim APTPA experiment:")
AuthorsPathSimAPTPAExperiment.run()