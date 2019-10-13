import sys
import constants
sys.path.insert(0, '../..')
sys.path.insert(1, "../../x86")
import Leap
from Leap import Finger, Bone
import pygame
import pickle
import numpy as np
from pygameWindow import PYGAME_WINDOW

clf = pickle.load( open('userData/classifier.p', 'rb') )
global testData
testData = np.zeros((1,30),dtype='f')

pygameWindow = PYGAME_WINDOW()

x = 0
y = 0

xMin = -200.0
xMax = 200.0
yMin = -200.0
yMax = 200.0

def Scale(var, min1, max1, min2, max2):
    range1 = max1 - min1
    range2 = max2 - min2
    if (max1 == min1):
        scaled_value = float(range2) / 2 + min2
        
    else:
        scaled_value = ( ( float(var - min1) / range1 ) * range2) + min2
    return int(scaled_value)

def Handle_Frame(frame):
    global x,y, xMin, xMax, yMin, yMax, testData
    hand = frame.hands[0]
    fingers = hand.fingers

    for finger in fingers:
        Handle_Finger(finger)
    testData = CenterData(testData)
    predictedClass = clf.Predict(testData)
    print(predictedClass)

    indexFingerList = fingers.finger_type(Finger.TYPE_INDEX)
    indexFinger = indexFingerList[0]
    distalPhalanx = indexFinger.bone(Bone.TYPE_DISTAL)
    tip = distalPhalanx.next_joint
    x = int(tip[0])
    y = int(tip[2])

    if ( x < xMin ):
        xMin = x
    if ( x > xMax ):
        xMax = x
    if (y < yMin ):
        yMin = y
    if ( y > yMax ):
        yMax = y

def Handle_Finger(finger):
    for b in range (0,4):
        Handle_Bone(finger.bone(b), b)

def Handle_Bone(bone, b):
    global k, testData
    base = bone.prev_joint
    tip = bone.next_joint
    base_x, base_y, base_z = Handle_Vector_From_Leap(base)
    tip_x, tip_y, tip_z = Handle_Vector_From_Leap(tip)
    pygameWindow.Draw_Black_Line(base_x, base_z, tip_x, tip_z, 3 - bone.type)
    if (( b == 0) or (b == 3)):
            testData[0,k]   = tip[0]
            testData[0,k+1] = tip[1]
            testData[0,k+2] = tip[2]
            k = k + 3

def Handle_Vector_From_Leap(v):
    global xMin, xMax, yMin, yMax

    x = Scale(v[0], xMin, xMax, 0, constants.pygameWindowWidth)
    y = Scale(v[1], yMin, yMax, 0, constants.pygameWindowDepth)
    z = Scale(v[2], yMin, yMax, 0, constants.pygameWindowDepth)

    return x, y, z

def CenterData(X):
    allXCoordinates = X[0,::3]
    meanValue = allXCoordinates.mean()
    X[0,::3] = allXCoordinates - meanValue
    
    allYCoordinates = X[0,1::3]
    meanValue = allYCoordinates.mean()
    X[0,1::3] = allYCoordinates - meanValue

    allZCoordinates = X[0,2::3]
    meanValue = allZCoordinates.mean()
    X[0,2::3] = allZCoordinates - meanValue
    return X

#MAIN
controller = Leap.Controller()
while True:
    pygameWindow.Prepare()
    frame = controller.frame()
    if(len(frame.hands) > 0):
        k = 0
        Handle_Frame(frame)

    pygameWindow.Reveal()
