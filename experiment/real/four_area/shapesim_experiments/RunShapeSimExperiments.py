from experiment.real.four_area.shapesim_experiments import AuthorsShapeSimCPPAExperiment, \
    AuthorsShapeSimCPPAOmitCPExperiment, ConferencesShapeSimTPPCExperiment, ConferencesShapeSimTPPCExperimentRelative

__author__ = 'jontedesco'

# Standalone experiments
print("Running ShapeSim CPPA experiment:")
citationCounts, publicationCounts, conferenceCitations, conferencePublications = AuthorsShapeSimCPPAExperiment.run()
print("Running ShapeSim CPPA experiment (omit CPC):")
AuthorsShapeSimCPPAOmitCPExperiment.run(citationCounts, publicationCounts)
print("Running ShapeSim TPPC experiment:")
ConferencesShapeSimTPPCExperiment.run(conferenceCitations, conferencePublications)
print("Running ShapeSim (Relative) TPPC experiment:")
ConferencesShapeSimTPPCExperimentRelative.run(conferenceCitations, conferencePublications)