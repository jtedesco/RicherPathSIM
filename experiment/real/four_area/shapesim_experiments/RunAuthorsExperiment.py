from experiment.real.four_area.shapesim_experiments import AuthorsShapeSimCPPAExperiment, \
    AuthorsShapeSimCPPAOmitCPExperiment

__author__ = 'jontedesco'

# Standalone experiments
print("Running ShapeSim CPPA experiment:")
citationCounts, publicationCounts = AuthorsShapeSimCPPAExperiment.run()
print("Running ShapeSim CPPA experiment (omit CPC):")
AuthorsShapeSimCPPAOmitCPExperiment.run(citationCounts, publicationCounts)
