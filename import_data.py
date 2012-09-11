from src.importer.CoMoToDataImporter import CoMoToDataImporter

__author__ = 'jon'

# Imports all experimental data from files in 'data/' directory, and outputs as pickled NetworkX objects in 'graphs/'
if __name__ == '__main__':

    # Get UIUC login info from user (for CoMoTo)
    netid = raw_input("Netid:")
    password = raw_input("Password:")

    comotoDataImporter = CoMoToDataImporter('graphs/dblp-arnet-v5', netid, password)

    comotoDataImporter.start()