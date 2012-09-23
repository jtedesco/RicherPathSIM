import os
from src.importer.ArnetMinerDataImporter import ArnetMinerDataImporter

__author__ = 'jon'

# Imports all experimental data from files in 'data/' directory, and outputs as pickled NetworkX objects in 'graphs/'
if __name__ == '__main__':

    os.putenv('PROJECT_ROOT', os.getcwd())

    #comotoDataImporter = CoMoToDataImporter('graphs/dblp-arnet-v5', netid, password)
    arnetMinerDataImporter = ArnetMinerDataImporter('data/real/DBLP-citation-Feb21.txt', 'graphs/arnetV5WithPublicationLinks')
    arnetMinerDataImporter.start()