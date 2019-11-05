import numpy as np
import pickle
from knn import KNN

train1 = pickle.load(open("userData/Clark_train1.p", "rb"))
train2 = pickle.load(open("userData/Trinity_train2.p", "rb"))
train3 = pickle.load(open("userData/Apple_train3.p", "rb"))
train4 = pickle.load(open("userData/Ward_train4.p", "rb"))
train5 = pickle.load(open("userData/Deluca_train5.p", "rb"))
train6 = pickle.load(open("userData/Picard_train6.p", "rb"))
train7 = pickle.load(open("userData/Burleson_train7.p", "rb"))
train8 = pickle.load(open("userData/Erickson_train8.p", "rb"))
train9 = pickle.load(open("userData/Lee_train9.p", "rb"))
train0 = pickle.load(open("userData/Lee_train0.p", "rb"))

#test1 = pickle.load(open("userData/Clark_test1.p", "rb"))
#test2 = pickle.load(open("userData/Giroux_test2.p", "rb"))
#test3 = pickle.load(open("userData/Ward_test3.p", "rb"))
#test4 = pickle.load(open("userData/Ward_test4.p", "rb"))
#test5 = pickle.load(open("userData/Deluca_test5.p", "rb"))
#test6 = pickle.load(open("userData/Boland_test6.p", "rb"))
#test7 = pickle.load(open("userData/Burleson_test7.p", "rb"))
#test8 = pickle.load(open("userData/Erickson_test8.p", "rb"))
#test9 = pickle.load(open("userData/Lee_test9.p", "rb"))
#test0 = pickle.load(open("userData/Lee_test0.p", "rb"))

def ReshapeData(set1, set2, set3, set4, set5, set6, set7, set8, set9, set0):
    X = np.zeros((10000,5*2*3),dtype='f')
    y = np.zeros(10000)
    for row in range(0,1000):
        y[row]      = 1
        y[row+1000] = 2
        y[row+2000] = 3
        y[row+3000] = 4
        y[row+4000] = 5
        y[row+5000] = 6
        y[row+6000] = 7
        y[row+7000] = 8
        y[row+8000] = 9
        y[row+9000] = 0
        col = 0
        for j in range(0,5):
            for k in range(0,2):
                for m in range(0,3):
                    X[row,col]      = set1[j,k,m,row]
                    X[row+1000,col] = set2[j,k,m,row]
                    X[row+2000,col] = set3[j,k,m,row]
                    X[row+3000,col] = set4[j,k,m,row]
                    X[row+4000,col] = set5[j,k,m,row]
                    X[row+5000,col] = set6[j,k,m,row]
                    X[row+6000,col] = set7[j,k,m,row]
                    X[row+7000,col] = set8[j,k,m,row]
                    X[row+8000,col] = set9[j,k,m,row]
                    X[row+9000,col] = set0[j,k,m,row]
                    col = col + 1
    return X,y

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

def ReduceData(X):
    X = np.delete(X,1,1)
    X = np.delete(X,1,1)
    X = np.delete(X,0,2)
    X = np.delete(X,0,2)
    X = np.delete(X,0,2)
    return X

train1 = ReduceData(train1)
train2 = ReduceData(train2)
train3 = ReduceData(train3)
train4 = ReduceData(train4)
train5 = ReduceData(train5)
train6 = ReduceData(train6)
train7 = ReduceData(train7)
train8 = ReduceData(train8)
train9 = ReduceData(train9)
train0 = ReduceData(train0)

train1 = CenterData(train1)
train2 = CenterData(train2)
train3 = CenterData(train3)
train4 = CenterData(train4)
train5 = CenterData(train5)
train6 = CenterData(train6)
train7 = CenterData(train7)
train8 = CenterData(train8)
train9 = CenterData(train9)
train0 = CenterData(train0)

#test1 = ReduceData(CenterData(test1))
#test2 = ReduceData(CenterData(test2))
#test3 = ReduceData(CenterData(test3))
#test4 = ReduceData(CenterData(test4))
#test5 = ReduceData(CenterData(test5))
#test6 = ReduceData(CenterData(test6))
#test7 = ReduceData(CenterData(test7))
#test8 = ReduceData(CenterData(test8))
#test9 = ReduceData(CenterData(test9))
#test0 = ReduceData(CenterData(test0))

trainX, trainy = ReshapeData(train1, train2, train3, train4, train5, train6, train7, train8, train9, train0)
#testX, testy = ReshapeData(test1, test2, test3, test4, test5, test6, test7, test8, test9, test0)

knn = KNN()
knn.Use_K_Of(15)
knn.Fit(trainX, trainy)
correct = 0
#for row in range(0, len(testy)):
#    actualClass = testy[row]
#    prediction = knn.Predict(testX[row])
#    if (actualClass == prediction):
#        correct = correct + 1
#print correct / 8000.0 * 100.0

pickle.dump(knn, open('userData/classifier.p', 'wb'))

