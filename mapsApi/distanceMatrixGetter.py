"""Accesses google maps api to return a distance matrix

Method returns pandas array of dist mat
"""

import logging
import googlemaps
import globalConstants
import pandas as pd
from pandas.io.json import json_normalize
import os

# Set up logger
logging.basicConfig(level=globalConstants.loggingLevel, format='%(asctime)s - %(levelname)s - %(message)s')

# Read API key from file
def getkey():
    f = open(globalConstants.dropboxPath + "MDSproject/mapsDistMatAPIkey.txt", 'r')
    mapsKey = f.readline()
    f.close()
    return mapsKey

def readstudentdata():
    cur_path = os.path.dirname(__file__)
    new_path = os.path.relpath('..\\studentsByOA.csv', cur_path)
    return pd.read_csv(new_path)


# Start google maps session
gmaps = googlemaps.Client(key=getkey())

# Load in the data
studentData = readstudentdata()

destinations = "54.008102,-1.536223|54.002248,-1.522599|53.9983792,-1.509521"
origins = destinations

matrix = gmaps.distance_matrix(origins, destinations, units="metric")
newmat = json_normalize(matrix, ['rows', 'elements'])

# Verify that the matrix came back with no errors
if newmat['status'].unique().size > 1 or newmat['status'][0] != "OK":
    logging.error("Query to mapping API failed")
    quit()
# Verify that it's the right size
elif newmat['distance'].size != len(destinations.split("|")) * len(origins.split("|")):
    logging.error("Query to mapping API returned matrix of wrong size")
    quit()
else:
    logging.debug("Mapping API query success")
print newmat

gmaps.session.close()
