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
def get_key():
    f = open(gc.dropboxPath + "MDSproject/newAPIkey.txt", 'r')
    maps_key = f.readline()
    f.close()
    return maps_key


# Get the student/postcode/OA data from the flat file
def read_student_data():
    cur_path = os.path.dirname(__file__)
    new_path = os.path.relpath('..\\studentsByOA.csv', cur_path)
    return pd.read_csv(new_path)


# Given origin and destination strings, make the gmaps API call. Return the data.
def make_api_call(origin, dest):
    # Make the API request
    matrix = gmaps.distance_matrix(origin, dest, units="metric")  # [:-1] is to remove last "|"
    new_mat = json_normalize(matrix, ["rows", "elements"])

    # Verify that the query returned with no errors
    if new_mat['status'][0] == "MAX_ELEMENTS_EXCEEDED ":
        logging.warning("Max elements exceeded")
        return (pd.DataFrame(), False)
    if new_mat['status'].unique().size > 1 or new_mat['status'][0] != "OK":
        logging.error("Query to mapping API failed with error " + new_mat['status'][0])
        quit()
    # Verify that it's the right size
    elif new_mat['distance'].size != len(destString[:-1].split("|")) * len(originString.split("|")):
        logging.error("Query to mapping API returned matrix of wrong size")
        logging.error("Expected " + str(len(destString[:-1].split("|")) * len(originString.split("|"))) +
                      ", got" + str(new_mat['distance'].size) )
        quit()
    else:
        logging.debug("API query success")
        return (new_mat,True)


# ========== End function definitions ==========

logging.info("Beginning processing to generate distance matrix")

# Load in the data - output areas, lat/long, number of students
logging.debug("Reading student data...")
studentData = read_student_data()
if os.path.isfile("distancematrix.csv"):
    fromToMatrix = pd.read_csv("distancematrix.csv", header=0, index_col="oa11")
else:
    fromToMatrix = pd.DataFrame(columns=studentData["oa11"], index=studentData["oa11"])
    fromToMatrix = fromToMatrix.fillna(-1)

logging.debug("Done. Starting API Requests...")

# Start google maps session
gmaps = googlemaps.Client(key=getkey(), queries_per_second=1, client_id="kmeans-171418", retry_timeout=200)

apiMatrix = []
# Need a loop to create the origin/destination strings for the API
for idx1 in range(0, fromToMatrix.index.size):
    originString = str(studentData.iloc[idx1]["lat"]) + "," + str(studentData.iloc[idx1]["long"])
    destString = ""
    # startVal = 0
    continueRun = True
    for idx2 in range(0, fromToMatrix.index.size):
        if fromToMatrix.iloc[idx1, idx2] == -1:# or fromToMatrix.iloc[idx1, startVal+1] == -1:   # If the row is not yet filled in
            destString += str(studentData.iloc[idx2]["lat"]) + "," + str(studentData.iloc[idx2]["long"]) + "|"
            # API can only handle requests up to length 25; since we have 230 elements, break it into 23s
            #if ((idx2 % 23 == 0 and idx2 > 0) or idx2==229) and destString!="":
            try:
                (newmat, success) = makeAPIcall(originString, destString[:-1]) # [:-1] is to remove last "|"
            except googlemaps.exceptions.Timeout:
                logging.warn("Timeout error")
                continueRun = False
                break
            except googlemaps.exceptions.ApiError:
                logging.warn("API error")
                continueRun = False
                break
            except googlemaps.exceptions.TransportError:
                logging.warn("Transport error?")
                continueRun = False
                break
            if success: # Successful query, so insert the data into the distance matrix
                for idx in range(0, newmat.index.size):
                    fromToMatrix.iloc[idx1, idx2] = newmat["distance"].iloc[idx]["value"]
                # startVal = idx2+1
                destString = ""
            else: # Query returned "max queries reached"
                continueRun = False
                break
        # startVal = idx2 + 1
        # destString = ""
    if not continueRun:
        break


fromToMatrix.to_csv("distanceMatrix.csv")

gmaps.session.close()
