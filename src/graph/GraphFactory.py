import os
from src.graph.impl.NetworkXGraph import NetworkXGraph

__author__ = 'jontedesco'


class GraphFactory(object):
    """
      Forms a wrapper to graph library implementations, to allow swapping out underlying implementation without changing
      code in rest of project.
    """

    typeMap = {
        'networkx': NetworkXGraph
    }

    @staticmethod
    def createInstance():
        """
          Create a new (directed) graph instance
        """

        graphTypeEnvVariable = os.getenv('GRAPH_TYPE')
        graphTypeKey = graphTypeEnvVariable if graphTypeEnvVariable is not None else 'networkx' # Default to networkx
        graphType = GraphFactory.typeMap[str(graphTypeKey)]

        return graphType()
