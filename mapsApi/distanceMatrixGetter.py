"""Accesses google maps api to return a distance matrix

Method returns pandas array of dist mat
"""

import googlemaps

# Read API key from file
f = open("C:\Users\TrevHP\Dropbox\MDSproject\mapsAPIkey.txt",'r')
mapsKey = f.readline()
f.close()


gmaps = googlemaps.Client(key=mapsKey)

