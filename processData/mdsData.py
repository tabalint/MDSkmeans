"""Takes dissimilarity data and uses MDS to make it into coordinate data

Input: csv -> pandas dataframe (dissimilarity data - square matrix)
Output: pd.df -> csv (coordinate data - 2/3 columns)
"""

from sklearn import manifold, utils
import pandas as pd
import os


# Get the student/postcode/OA data from the flat file
def readstudentdata():
    cur_path = os.path.dirname(__file__)
    new_path = os.path.relpath('..\\studentsByOA.csv', cur_path)
    return pd.read_csv(new_path)


inData = pd.read_csv("distancematrix.csv", header=0, index_col="oa11")

# the real distance matrix is asymmetric - mds requires a symmetric one
# use this function to create a symmetric version
# it averages the matrix with its transpose
symmMatrix = utils.check_symmetric(inData.as_matrix())

mds = manifold.MDS(n_components=2, max_iter=3000, eps=1e-4, random_state=None,
                   dissimilarity="precomputed", n_jobs=1, metric=True)
coords = mds.fit(symmMatrix).embedding_

oldData = readstudentdata()
oldData = oldData.set_index("oa11")
coordsDF = pd.DataFrame(data=coords, index=inData.index.values)
oldData.loc[:, "fakex"] = pd.Series(coordsDF.loc[:, 0], index=inData.index.values)
oldData.loc[:, "fakey"] = pd.Series(coordsDF.loc[:, 1], index=inData.index.values)

oldData.to_csv("mdsCoords.csv")

print("done!")
