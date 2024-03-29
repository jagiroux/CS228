import sys
import constants
sys.path.insert(0, '..')
sys.path.insert(1, "../x86")
import Leap
from Leap import Finger, Bone
import pygame
from pygameWindow import PYGAME_WINDOW

pygameWindow = PYGAME_WINDOW()

x = 1000
y = 1000

xMin = 1000.0
xMax = -1000.0
yMin = 1000.0
yMax = -1000.0

def Scale(var, min1, max1, min2, max2):
    range1 = max1 - min1
    range2 = max2 - min2
    if (max1 == min1):
        scaled_value = float(range2) / 2 + min2
        
    else:
        scaled_value = ( ( float(var - min1) / range1 ) * range2) + min2
    return scaled_value

def Handle_Frame(frame):
    global x,y, xMin, xMax, yMin, yMax
    hand = frame.hands[0]
    fingers = hand.fingers
    for finger in fingers:
        Handle_Finger(finger)

    indexFingerList = fingers.finger_type(Finger.TYPE_INDEX)
    indexFinger = indexFingerList[0]
    distalPhalanx = indexFinger.bone(Bone.TYPE_DISTAL)
    tip = distalPhalanx.next_joint
    x = int(tip[0])
    y = int(tip[1])

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
        Handle_Bone(finger.bone(b))

def Handle_Bone(bone):
    base = bone.prev_joint
    tip = bone.next_joint
    base_x, base_y = Handle_Vector_From_Leap(base)
    tip_x, tip_y = Handle_Vector_From_Leap(tip)
    pygameWindow.Draw_Black_Line(base_x, base_y, tip_x, tip_y, 3 - bone.type)

def Handle_Vector_From_Leap(v):
    global xMin, xMax, yMin, yMax

    x = Scale(v[0], xMin, xMax, 0, constants.pygameWindowWidth)
    y = Scale(v[2], yMin, yMax, 0, constants.pygameWindowDepth)

    return x, y

#MAIN
controller = Leap.Controller()
while True:
    pygameWindow.Prepare()
    frame = controller.frame()
    if(len(frame.hands) > 0):
        Handle_Frame(frame)

    pygameWindow.Reveal()
