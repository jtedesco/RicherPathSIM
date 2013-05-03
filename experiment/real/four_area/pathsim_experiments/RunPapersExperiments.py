from experiment.real.four_area.pathsim_experiments.papers import PapersNeighborSimTPPExperiment,\
    PapersNeighborSimCPPExperiment, PapersNeighborSimAPPExperiment, PapersPathsimPAPExperiment,\
    PapersPathsimPCPExperiment, PapersPathsimPTPExperiment

__author__ = 'jontedesco'

print("Running NeighborSim APP Experiment:")
PapersNeighborSimAPPExperiment.run()
print("Running NeighborSim CPP Experiment:")
PapersNeighborSimCPPExperiment.run()
print("Running NeighborSim TPP Experiment:")
PapersNeighborSimTPPExperiment.run()
print("Running PathSim PAP Experiment:")
PapersPathsimPAPExperiment.run()
print("Running PathSim PCP Experiment:")
PapersPathsimPCPExperiment.run()
print("Running PathSim PTP Experiment:")
PapersPathsimPTPExperiment.run()