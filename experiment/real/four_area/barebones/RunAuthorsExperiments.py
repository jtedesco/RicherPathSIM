import os
from experiment.real.four_area.barebones import AuthorsNeighborSimPPAExperiment, AuthorsNeighborSimTPPAExperiment, AuthorsPathSimAPCPAExperiment, AggregateAuthorsExperiment

__author__ = 'jontedesco'

# Standalone experiments
print("Running NeighborSim PPA experiment:")
citationCounts, publicationCounts = AuthorsNeighborSimPPAExperiment.run()
print("Running NeighborSim TPPA experiment:")
AuthorsNeighborSimTPPAExperiment.run(citationCounts, publicationCounts)
print("Running PathSim APCPA experiment:")
AuthorsPathSimAPCPAExperiment.run(citationCounts, publicationCounts)

# Combined/lazy experiments
print("Running NeighborSim PPA - PathSim APCPA experiment:")
AggregateAuthorsExperiment.run(
    'Most Similar PPA-APCPA NeighborSim Authors',
    os.path.join('results','authors','ppa-apcpaNeighborSim-%1.1f-%1.1f' % (0.5, 0.5)),
    citationCounts,
    publicationCounts,
    [(os.path.join('results', 'intermediate', '%s-neighborsim-ppa'), 0.5),
     (os.path.join('results', 'intermediate', '%s-pathsim-apcpa'), 0.5)]
)
print("Running NeighborSim PPA - PathSim APCPA experiment (0.3, 0.7):")
AggregateAuthorsExperiment.run(
    'Most Similar PPA-APCPA NeighborSim Authors',
    os.path.join('results','authors','ppa-apcpaNeighborSim-%1.1f-%1.1f' % (0.3, 0.7)),
    citationCounts,
    publicationCounts,
    [(os.path.join('results', 'intermediate', '%s-neighborsim-ppa'), 0.3),
     (os.path.join('results', 'intermediate', '%s-pathsim-apcpa'), 0.7)]
)
print("Running NeighborSim TPPA - PathSim APCPA experiment:")
AggregateAuthorsExperiment.run(
    'Most Similar TPPA-APCPA NeighborSim Authors',
    os.path.join('results','authors','tppa-apcpaNeighborSim-%1.1f-%1.1f' % (0.5, 0.5)),
    citationCounts,
    publicationCounts,
    [(os.path.join('results', 'intermediate', '%s-neighborsim-tppa'), 0.5),
     (os.path.join('results', 'intermediate', '%s-pathsim-apcpa'), 0.5)]
)
print("Running NeighborSim TPPA - PathSim APCPA experiment (0.3, 0.7):")
AggregateAuthorsExperiment.run(
    'Most Similar TPPA-APCPA NeighborSim Authors',
    os.path.join('results','authors','tppa-apcpaNeighborSim-%1.1f-%1.1f' % (0.3, 0.7)),
    citationCounts,
    publicationCounts,
    [(os.path.join('results', 'intermediate', '%s-neighborsim-tppa'), 0.3),
     (os.path.join('results', 'intermediate', '%s-pathsim-apcpa'), 0.7)]
)
