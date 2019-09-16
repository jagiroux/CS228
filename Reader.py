import numpy as np
import os
import pickle
import constants
import time
from pygameWindow_Del03 import PYGAME_WINDOW

class READER:
    def __init__(self):
        self.pygameWindow = PYGAME_WINDOW()
        self.numGestures = 0
        self.Get_Num_Files()

    def Get_Num_Files(self):
        path, dirs, files = next(os.walk('userData'))   
        self.numGestures = len(files)

    def Draw_Gestures(self):
        while True:
            self.Draw_Each_Gesture_Once()

    def Draw_Each_Gesture_Once(self):
        for i in range (0, self.numGestures):
            pickle_in = open("userData/gesture" + str(i) + ".p", "rb")
            gestureData = pickle.load(pickle_in)
            self.Draw_Gesture(i, gestureData)

    def Draw_Gesture(self, gesture_num, gestureData):
        self.pygameWindow.Prepare()
        for i in range(0,5):
            for j in range(0,4):
                currentBone = []
                currentBone.append(gestureData[i,j,0])
                currentBone.append(gestureData[i,j,1])
                currentBone.append(gestureData[i,j,2])
                currentBone.append(gestureData[i,j,3])
                currentBone.append(gestureData[i,j,4])
                currentBone.append(gestureData[i,j,5])
                xBaseNotYetScaled = currentBone[0]
                yBaseNotYetScaled = currentBone[2]
                xTipNotYetScaled = currentBone[3]
                yTipNotYetScaled = currentBone[5]

                xBase = self.Scale(xBaseNotYetScaled, constants.min, constants.max, 0, constants.pygameWindowWidth)
                yBase = self.Scale(yBaseNotYetScaled, constants.min, constants.max, 0, constants.pygameWindowDepth)
                xTip = self.Scale(xTipNotYetScaled, constants.min, constants.max, 0, constants.pygameWindowWidth)
                yTip = self.Scale(yTipNotYetScaled, constants.min, constants.max, 0, constants.pygameWindowDepth)
                
                self.pygameWindow.Draw_Line(xBase, yBase, xTip, yTip, 1, (0,0,255))
        self.pygameWindow.Reveal()
        time.sleep(0.75)

    def Scale(self, var, min1, max1, min2, max2):
        range1 = max1 - min1
        range2 = max2 - min2
        if (max1 == min1):
            scaled_value = float(range2) / 2 + min2
            
        else:
            scaled_value = ( ( float(var - min1) / range1 ) * range2) + min2
        return scaled_value
