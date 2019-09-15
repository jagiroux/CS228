import constants
from pygameWindow_Del03 import PYGAME_WINDOW
import pygame
import sys
sys.path.insert(0, '..')
sys.path.insert(1, "../x86")
import Leap
from Leap import Finger, Bone

class DELIVERABLE:
    def __init__(self):
        self.pygameWindow = PYGAME_WINDOW()
        self.x = 500
        self.y = 500
        self.xMin = 1000.0
        self.xMax = -1000.0
        self.yMin = 1000.0
        self.yMax = -1000.0
        self.controller = Leap.Controller()

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

    def Handle_Finger(self, finger):
        for b in range (0,4):
            self.Handle_Bone(finger.bone(b))

    def Handle_Bone(self, bone):
        base = bone.prev_joint
        tip = bone.next_joint
        base_x, base_y = self.Handle_Vector_From_Leap(base)
        tip_x, tip_y = self.Handle_Vector_From_Leap(tip)

        self.numberOfHands = len(self.controller.frame().hands)
        print(self.numberOfHands)
        
        if self.numberOfHands == 1:
            self.pygameWindow.Draw_Line(base_x, base_y, tip_x, tip_y, 3 - bone.type, (0,255,0))
        if self.numberOfHands == 2:
            self.pygameWindow.Draw_Line(base_x, base_y, tip_x, tip_y, 3 - bone.type, (255,0,0))   

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
        if(len(self.frame.hands) > 0):
            self.Handle_Frame(self.frame)

        self.pygameWindow.Reveal()
