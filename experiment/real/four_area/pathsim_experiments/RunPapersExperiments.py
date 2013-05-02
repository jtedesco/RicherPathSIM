from experiment.real.four_area.barebones import PapersPathSimPCPExperiment, PapersPathSimPAPExperiment, PapersPathSimPTPExperiment
from experiment.real.four_area.pathsim_experiments.papers import PapersNeighborSimTPPExperiment, PapersNeighborSimCPPExperiment, PapersNeighborSimAPPExperiment

__author__ = 'jontedesco'

print("Running NeighborSim APP Experiment:")
PapersNeighborSimAPPExperiment.run()
print("Running NeighborSim CPP Experiment:")
PapersNeighborSimCPPExperiment.run()
print("Running NeighborSim TPP Experiment:")
PapersNeighborSimTPPExperiment.run()
print("Running PathSim PAP Experiment:")
PapersPathSimPAPExperiment.run()
print("Running PathSim PCP Experiment:")
PapersPathSimPCPExperiment.run()
print("Running PathSim PTP Experiment:")
PapersPathSimPTPExperiment.run()