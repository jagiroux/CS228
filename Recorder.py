import constants
from pygameWindow_Del03 import PYGAME_WINDOW
import pygame
import os
import shutil
import sys
sys.path.insert(0, '..')
sys.path.insert(1, "../x86")
import Leap
import numpy as np
import pickle
from Leap import Finger, Bone

class RECORDER:
    def __init__(self):
        self.pygameWindow = PYGAME_WINDOW()
        self.numberOfGestures = 1000
        self.gestureIndex = 0
        self.x = 300
        self.y = 300
        self.xMin = 1000.0
        self.xMax = -1000.0
        self.yMin = 1000.0
        self.yMax = -1000.0
        self.controller = Leap.Controller()

        self.previousNumberOfHands = 0
        self.currentNumberOfHands = 0

        self.gesturedata = np.zeros((5,4,6, self.numberOfGestures), dtype='f')
        self.gesturenumber = 0

        self.Clear_Data()

    def Scale(self, var, min1, max1, min2, max2):
        range1 = max1 - min1
        range2 = max2 - min2
        if (max1 == min1):
            scaled_value = float(range2) / 2 + min2
            
        else:
            scaled_value = ( ( float(var - min1) / range1 ) * range2) + min2
        return scaled_value

    def Handle_Frame(self, frame):
        hand = frame.hands[0]
        fingers = hand.fingers
        for finger in fingers:
            self.Handle_Finger(finger)

        indexFingerList = fingers.finger_type(Finger.TYPE_INDEX)
        indexFinger = indexFingerList[0]
        distalPhalanx = indexFinger.bone(Bone.TYPE_DISTAL)
        tip = distalPhalanx.next_joint
        x = int(tip[0])
        y = int(tip[1])

        if ( x < self.xMin ):
            self.xMin = x
        if ( x > self.xMax ):
            self.xMax = x
        if (y < self.yMin ):
            self.yMin = y
        if ( y > self.yMax ):
            self.yMax = y
            
        if self.currentNumberOfHands == 2:
            print('gesture ' + str(self.gestureIndex) + ' stored.')
            self.gestureIndex = self.gestureIndex + 1
            if self.gestureIndex == self.numberOfGestures:
                self.Save_Gesture()
                exit(0)

    def Handle_Finger(self, finger):
        for b in range (0,4):
            self.Handle_Bone(finger.bone(b), finger)

    def Handle_Bone(self, bone, finger):
        base = bone.prev_joint
        tip = bone.next_joint
        base_x, base_y = self.Handle_Vector_From_Leap(base)
        tip_x, tip_y = self.Handle_Vector_From_Leap(tip)
        
        if self.currentNumberOfHands == 1:
            self.pygameWindow.Draw_Line(base_x, base_y, tip_x, tip_y, 3 - bone.type, (0,255,0))
        if self.currentNumberOfHands == 2:
            self.pygameWindow.Draw_Line(base_x, base_y, tip_x, tip_y, 3 - bone.type, (255,0,0))

        if (self.currentNumberOfHands == 2):
            self.gesturedata[finger.type,bone.type,0, self.gestureIndex] = base[0]
            self.gesturedata[finger.type,bone.type,1, self.gestureIndex] = base[1]
            self.gesturedata[finger.type,bone.type,2, self.gestureIndex] = base[2]
            self.gesturedata[finger.type,bone.type,3, self.gestureIndex] = tip[0]
            self.gesturedata[finger.type,bone.type,4, self.gestureIndex] = tip[1]
            self.gesturedata[finger.type,bone.type,5, self.gestureIndex] = tip[2]


    def Handle_Vector_From_Leap(self, v):

        x = self.Scale(v[0], self.xMin, self.xMax, 0, constants.pygameWindowWidth)
        y = self.Scale(v[2], self.yMin, self.yMax, 0, constants.pygameWindowDepth)

        return x, y

    def Run_Forever(self):
        while True:
            self.Run_Once()

    def Run_Once(self):
        self.pygameWindow.Prepare()
        self.frame = self.controller.frame()
        self.currentNumberOfHands = len(self.frame.hands)
        if(len(self.frame.hands) > 0):
            self.Handle_Frame(self.frame)
        self.pygameWindow.Reveal()
        self.previousNumberOfHands = self.currentNumberOfHands

    def Recording_Is_Ending(self):
        if (self.currentNumberOfHands == 1 and self.previousNumberOfHands == 2):
            return True
        else:
            return False

    def Save_Gesture(self):
        pickle_out = open("userData/gesture.p", "wb")
        pickle.dump(self.gesturedata, pickle_out)
        pickle_out.close()
        self.gesturenumber = self.gesturenumber + 1

    def Clear_Data(self):
        shutil.rmtree("userData")
        os.mkdir("userData")
