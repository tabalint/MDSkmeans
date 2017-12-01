# Method to generate a few images of the two different coordinate systems
# Not very pretty - if these will be for publishing, need a lot of formatting
import pandas as pd

fullCoords = pd.read_csv('mdsCoords.csv')

realAx = fullCoords.plot.scatter(x='lat', y='long')
realFig = realAx.get_figure()
realFig.savefig('realCoords.png')

fakeAx = fullCoords.plot.scatter(x='fakex', y='fakey')
fakeFig = fakeAx.get_figure()
fakeFig.savefig('fakeCoords.png')
