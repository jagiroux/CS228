import sys
import constants
sys.path.insert(0, '..')
sys.path.insert(1, "../x86")
import Leap
from Leap import Finger, Bone
from pygameWindow import PYGAME_WINDOW

x = 1000
y = 1000

#xMin = 1000.0
#xMax = -1000.0
#yMin = 1000.0
#yMax = -1000.0

xMin = -278.0
xMax = 269.0
yMin = 20.0
yMax = 564.0

def Scale(var, min1, max1, min2, max2):
    range1 = max1 - min1
    range2 = max2 - min2
    if (max1 == min1):
        range1 = max1 + min1
    if (max2 == min2):
        range2 = max2 + min2

    scaled_value = ( ( (var - min1) / range1 ) * range2) + min2
    return scaled_value

def Handle_Frame(frame):
    global x,y, xMin, xMax, yMin, yMax
    hand = frame.hands[0]
    fingers = hand.fingers
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

    print("xMin: ", xMin, " xMax: ", xMax, " yMin: ", yMin, " yMax: ", yMax)

pygameWindow = PYGAME_WINDOW()

controller = Leap.Controller()
while True:
    frame = controller.frame()
    if(len(frame.hands) > 0):
        Handle_Frame(frame)

    pygameX = Scale(x, xMin, xMax, 0, constants.pygameWindowWidth)
    pygameY = Scale(y, yMin, yMax, constants.pygameWindowDepth, 0)
        
    pygameWindow.Prepare()
    pygameWindow.Draw_Black_Circle(int(pygameX), int(pygameY))
    pygameWindow.Reveal()

