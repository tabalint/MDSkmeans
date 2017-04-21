"""Accesses google maps api to return a distance matrix

Method returns pandas array of dist mat
"""

import googlemaps
from pandas.io.json import json_normalize


# Read API key from file
def getkey():
    f = open("C:\Users\TrevHP\Dropbox\MDSproject\mapsDistMatAPIkey.txt",'r')
    mapsKey = f.readline()
    f.close()
    return mapsKey


gmaps = googlemaps.Client(key=getkey())

destinations = "54.008102,-1.536223|54.002248,-1.522599|53.9983792,-1.509521"

matrix = gmaps.distance_matrix(destinations, destinations, units="metric")
newmat = json_normalize(matrix,['rows', 'elements'])
if newmat['status'].unique().size > 1: quit("ARGHS")
else: print "Everything is awesome!"
print newmat
#geocode_result = gmaps.geocode('1600 Amphitheatre Parkway, Mountain View, CA')
