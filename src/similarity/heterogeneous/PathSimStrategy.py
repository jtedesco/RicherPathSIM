from src.similarity import MetaPathSimilarityStrategy

__author__ = 'jontedesco'

class PathSimStrategy(MetaPathSimilarityStrategy):
    """
      Class that implements the PathSim similarity measure for same-typed nodes on heterogeneous graphs. Based on
      publication by Yizhou Sun et al.

        @see    http://citeseer.ist.psu.edu/viewdoc/summary?doi=10.1.1.220.2455
    """