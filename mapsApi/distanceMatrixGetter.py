"""Accesses google maps api to return a distance matrix

Method returns pandas array of dist mat
"""

import logging
import googlemaps
import globalConstants as gc
import pandas as pd
from pandas.io.json import json_normalize
import os

# Set up logger
logging.basicConfig(level=gc.loggingLevel, format='%(asctime)s - %(levelname)s - %(message)s')

# Read API key from file
def getkey():
    f = open(gc.dropboxPath + "MDSproject/mapsDistMatAPIkey.txt", 'r')
    mapsKey = f.readline()
    f.close()
    return mapsKey

def readstudentdata():
    cur_path = os.path.dirname(__file__)
    new_path = os.path.relpath('..\\studentsByOA.csv', cur_path)
    return pd.read_csv(new_path)

# ========== End function definitions ==========

logging.info("Beginning processing to generate distance matrix")

# Load in the data - output areas, lat/long, number of students
logging.debug("Reading student data...")
studentData = readstudentdata()
fromToMatrix = pd.DataFrame(columns=studentData["oa11"], index=studentData["oa11"])
fromToMatrix = fromToMatrix.fillna(-1)

logging.debug("Done. Creating API request strings...")

apiMatrix = []
# Need a loop to create the origin/destination strings for the API
for idx1 in range(0, fromToMatrix.index.size):
    destString = ""
    for idx2 in range(0, fromToMatrix.index.size):
        if idx1 != idx2:
            destString += str(studentData.iloc[idx2]["lat"]) + "," + str(studentData.iloc[idx2]["long"]) + "|"
    originString = str(studentData.iloc[idx1]["lat"]) + "," + str(studentData.iloc[idx1]["long"])
    apiMatrix += [[originString, destString[:-1]]] # The :-1 is to slice off the | from the last added string

logging.debug("Done. Starting API Requests...")


# Start google maps session
gmaps = googlemaps.Client(key=getkey())

for idx1 in range(0, fromToMatrix.index.size):
    matrix = gmaps.distance_matrix(apiMatrix[idx1][0], apiMatrix[idx1][1], units="metric")
    newmat = json_normalize(matrix, ['rows', 'elements'])

    # Verify that the query returned with no errors
    if newmat['status'].unique().size > 1 or newmat['status'][0] != "OK":
        logging.error("Query to mapping API failed")
        quit()
    # Verify that it's the right size
    elif newmat['distance'].size != len(apiMatrix[idx1][1].split("|")) * len(apiMatrix[idx1][0].split("|")):
        logging.error("Query to mapping API returned matrix of wrong size")
        quit()
    else:
        logging.debug("API query success")

    # Successful query, so insert the data into the distance matrix
    pastDiag = 0
    for idx2 in range(0, fromToMatrix.index.size):
        if idx1 == idx2:
            pastDiag = 1
            fromToMatrix.iloc[idx1, idx1] = 0
        else:
            fromToMatrix.iloc[idx1, idx2] = newmat["distance"].iloc[idx2-pastDiag]["value"]

fromToMatrix.to_csv("distanceMatrix.csv")

gmaps.session.close()
