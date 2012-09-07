from src.importers.CoMoToDataImporterThread import CoMoToDataImporterThread

__author__ = 'jon'

# Imports all experimental data from files in 'data/' directory, and outputs as pickled NetworkX objects in 'graphs/'
if __name__ == '__main__':

    # Get UIUC login info from user (for CoMoTo)
    netid = input("Netid:")
    password = input("Password:")

    comotoDataImporter = CoMoToDataImporterThread('graphs/dblp-arnet-v5', netid, password)

    comotoDataImporter.start()