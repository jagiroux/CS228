import numpy as np
import pickle
from knn import KNN

pickle_in = open("userData/train1.p", "rb")
train1 = pickle.load(pickle_in)
pickle_in = open("userData/train2.p", "rb")
train2 = pickle.load(pickle_in)
pickle_in = open("userData/test1.p", "rb")
test1 = pickle.load(pickle_in)
pickle_in = open("userData/test2.p", "rb")
test2 = pickle.load(pickle_in)

def ReshapeData(set1,set2):
    X = np.zeros((2000,5*2*3),dtype='f')
    y = np.zeros(2000)
    for row in range(0,1000):
        y[row] = 1
        y[row+1000] = 2
        col = 0
        for j in range(0,5):
            for k in range(0,2):
                for m in range(0,3):
                    X[row,col] = set1[j,k,m,row]
                    X[row+1000,col] = set2[j,k,m,row]
                    col = col + 1
    return X,y

def ReduceData(X):
    X = np.delete(X,1,1)
    X = np.delete(X,1,1)
    X = np.delete(X,0,2)
    X = np.delete(X,0,2)
    X = np.delete(X,0,2)
    return X

def CenterData(X):
    allXCoordinates = X[:,:,0,:]
    meanValue = allXCoordinates.mean()
    X[:,:,0,:] = allXCoordinates - meanValue
    allYCoordinates = X[:,:,1,:]
    meanValue = allYCoordinates.mean()
    X[:,:,1,:] = allYCoordinates - meanValue
    allZCoordinates = X[:,:,2,:]
    meanValue = allZCoordinates.mean()
    X[:,:,2,:] = allZCoordinates - meanValue
    return X

train1 = ReduceData(train1)
train1 = CenterData(train1)
train2 = ReduceData(train2)
train2 = CenterData(train2)
test1 = ReduceData(test1)
test1 = CenterData(test1)
test2 = ReduceData(test2)
test2 = CenterData(test2)

trainX, trainy = ReshapeData(train1, train2)
testX, testy = ReshapeData(test1, test2)

knn = KNN()
knn.Use_K_Of(15)
knn.Fit(trainX, trainy)
correct = 0
for row in range(0, len(testy)):
    actualClass = testy[row]
    prediction = knn.Predict(testX[row])
    if (actualClass == prediction):
        correct = correct + 1
print correct / 2000.0 * 100.0


