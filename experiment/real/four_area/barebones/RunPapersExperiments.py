from experiment.real.four_area.barebones import PapersNeighborSimCPPExperiment, PapersNeighborSimAPPExperiment, PapersPathSimPCPExperiment, PapersPathSimPAPExperiment, PapersPathSimPTPExperiment

__author__ = 'jontedesco'

print("Running NeighborSim APP Experiment:")
PapersNeighborSimAPPExperiment.run()
print("Running NeighborSim CPP Experiment:")
PapersNeighborSimCPPExperiment.run()
print("Running PathSim PAP Experiment:")
PapersPathSimPAPExperiment.run()
print("Running PathSim PCP Experiment:")
PapersPathSimPCPExperiment.run()
print("Running PathSim PTP Experiment:")
PapersPathSimPTPExperiment.run()