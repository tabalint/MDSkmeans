from sklearn import metrics
import pandas as pd

fullCoords = pd.read_csv('mdsCoords.csv')

fakeDistMat = metrics.pairwise.pairwise_distances(fullCoords[['fakex','fakey']], Y=None, metric='euclidean')

realDistMat = pd.read_csv("distancematrix.csv", header=0, index_col="oa11")
