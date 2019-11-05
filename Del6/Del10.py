import sys
import constants
sys.path.insert(0, '../..')
sys.path.insert(1, "../../x86")
import Leap
from Leap import Finger, Bone
import pygame
import pickle
import time
import random
import numpy as np
from pygameWindow import PYGAME_WINDOW

clf = pickle.load( open('userData/classifier.p', 'rb') )
global testData, programState, centerOfHandX, centerOfHandY, timeSinceWrong, previousPredicted, numPredictions, userRecord, timer, sessionAttempted, sessionSuccess, databaseAttempted, databaseSuccess
previousPredicted = 999
programState = 0
numPredictions = 0
timeSinceWrong = 0
sessionAttempted = 0
sessionSuccess = 0
databaseAttempted = 0
databaseSuccess = 0

database = pickle.load(open('userData/database.p','rb'))
userName = raw_input('Please enter your name: ')
                       
if userName in database:
    print('Welcome back ' + userName + '.')
    userRecord = database[userName]
    database[userName]["logins"] += 1

else:
    database[userName] = {"logins":1, "digit0attempted":0, "digit1attempted":0, "digit2attempted":0, "digit3attempted":0, "digit4attempted":0, "digit5attempted":0, "digit6attempted":0, "digit7attempted":0, "digit8attempted":0, "digit9attempted":0, "successful":0, "attempted":0, "digit0success":0, "digit1success":0, "digit2success":0, "digit3success":0, "digit4success":0, "digit5success":0, "digit6success":0, "digit7success":0, "digit8success":0, "digit9success":0}
    userRecord = database[userName]
    print('Welcome ' + userName + '.')

for user in database:
    databaseAttempted += database[user]["attempted"]
    databaseSuccess += database[user]["successful"]

example_image = pygame.image.load("leap_example.bmp")
up_arrow = pygame.image.load("handup.bmp")
down_arrow = pygame.image.load("handdown.bmp")
left_arrow = pygame.image.load("handleft.bmp")
right_arrow = pygame.image.load("handright.bmp")
correct = pygame.image.load("correct.bmp")
incorrect = pygame.image.load("incorrect.bmp")
zero = pygame.image.load("zero.bmp")
one = pygame.image.load("one.bmp")
two = pygame.image.load("two.bmp")
three = pygame.image.load("three.bmp")
four = pygame.image.load("four.bmp")
five = pygame.image.load("five.bmp")
six = pygame.image.load("six.bmp")
seven = pygame.image.load("seven.bmp")
eight = pygame.image.load("eight.bmp")
nine = pygame.image.load("nine.bmp")
num0 = pygame.image.load("0.bmp")
num1 = pygame.image.load("1.bmp")
num2 = pygame.image.load("2.bmp")
num3 = pygame.image.load("3.bmp")
num4 = pygame.image.load("4.bmp")
num5 = pygame.image.load("5.bmp")
num6 = pygame.image.load("6.bmp")
num7 = pygame.image.load("7.bmp")
num8 = pygame.image.load("8.bmp")
num9 = pygame.image.load("9.bmp")
clock = pygame.image.load("clock.bmp")
group = pygame.image.load("group.bmp")
movehand = pygame.image.load("movehand.bmp")

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
    global x,y, xMin, xMax, yMin, yMax, testData, previousPredicted, numPredictions
    hand = frame.hands[0]
    fingers = hand.fingers
    for finger in fingers:
        Handle_Finger(finger)
    testData = CenterData(testData)
    predictedClass = clf.Predict(testData)
    print(predictedClass)
    if (predictedClass == previousPredicted and programState == 2 and predictedClass == randInt):
        print("Num Predictions: " + str(numPredictions))
        numPredictions = numPredictions + 1

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

    previousPredicted = predictedClass
    text = "Digit: " + str(randInt) + " Presented: " + str(userRecord["digit" + str(randInt) + "attempted"]) + " Success: " + str(userRecord["digit" + str(randInt) + "success"])
    font = pygame.font.Font(pygame.font.get_default_font(), 15)
    text = font.render(text, True, (0,0,0))
    pygameWindow.screen.blit(text, (0,constants.pygameWindowDepth / 2))

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

    x = Scale(v[0], xMin, xMax, 0, constants.pygameWindowWidth / 2 )
    y = Scale(v[1], yMin, yMax, 0, constants.pygameWindowDepth / 2 )
    z = Scale(v[2], yMin, yMax, 0, constants.pygameWindowDepth / 2 )

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

def HandleState0():
    global programState
    pygameWindow.Draw_Image(example_image, constants.pygameWindowWidth / 2, 0, (constants.pygameWindowWidth / 2), (constants.pygameWindowDepth / 2))
    if (len(frame.hands) > 0):
        programState = 1

def isHandCentered():
    global centerOfHandX, centerOfHandY
    centerOfHandX = Scale(frame.hands[0].fingers[2].bone(0).prev_joint[0], xMin, xMax, 0, constants.pygameWindowWidth / 2 )
    centerOfHandY = Scale(frame.hands[0].fingers[2].bone(0).prev_joint[2], yMin, yMax, 0, constants.pygameWindowDepth / 2 )

    middleX = constants.pygameWindowWidth / 4
    middleY = constants.pygameWindowDepth / 4

    if (centerOfHandX > ((50 + middleX * .75))):
        return 1

    elif (centerOfHandX < ((50 + middleX * .25))):
        return 2

    elif (centerOfHandY > ((100 + middleY * .75))):
        return 3

    elif (centerOfHandY < ((100 + middleY * 0.25))):
        return 4

    else:
        return 0

def HandleState1():
    global programState, timeSinceWrong, k, timer
    k = 0
    Handle_Frame(frame)

    
    if (isHandCentered() == 1):
        pygameWindow.Draw_Image(left_arrow, constants.pygameWindowWidth / 2, 0, (constants.pygameWindowWidth / 2), (constants.pygameWindowDepth / 2))
        timeSinceWrong = time.time()

    elif (isHandCentered() == 2):
        pygameWindow.Draw_Image(right_arrow, constants.pygameWindowWidth / 2, 0, (constants.pygameWindowWidth / 2), (constants.pygameWindowDepth / 2))    
        timeSinceWrong = time.time()

    elif (isHandCentered() == 3):
        pygameWindow.Draw_Image(up_arrow, constants.pygameWindowWidth / 2, 0, (constants.pygameWindowWidth / 2), (constants.pygameWindowDepth / 2))
        timeSinceWrong = time.time()

    elif (isHandCentered() == 4):
        pygameWindow.Draw_Image(down_arrow, constants.pygameWindowWidth / 2, 0, (constants.pygameWindowWidth / 2), (constants.pygameWindowDepth / 2))
        timeSinceWrong = time.time()
        
    else:
        if ((time.time() - timeSinceWrong) > 1 ):
            pygameWindow.Draw_Image(correct, constants.pygameWindowWidth / 2, 0, (constants.pygameWindowWidth / 2), (constants.pygameWindowDepth / 2))
            timer = time.time()
            programState = 2

    if (len(frame.hands) == 0):
        programState = 0

def HandleState2():
    global programState, randInt, k, timer, numPredictions, sessionAttempted, sessionSuccess, databaseSuccess, databaseAttempted

    k = 0
    Handle_Frame(frame)
    handImages = [zero, one, two, three, four, five, six, seven, eight, nine]
    handSymbols = [num0, num1, num2, num3, num4, num5, num6, num7, num8, num9]

    #top line
    pygameWindow.Draw_Black_Line(constants.pygameWindowWidth/8 - 20, 3 * constants.pygameWindowDepth/4 - 91, constants.pygameWindowWidth/8 * 3 + 20, 3 * constants.pygameWindowDepth/4 - 91, 1)
    text = "100%"
    font = pygame.font.Font(pygame.font.get_default_font(), 13)
    text = font.render(text, True, (0,0,0))
    pygameWindow.screen.blit(text, (constants.pygameWindowWidth/8 - 60, 3 * constants.pygameWindowDepth/4 - 96))

    #bottom line
    pygameWindow.Draw_Black_Line(constants.pygameWindowWidth/8 - 20, 3 * constants.pygameWindowDepth/4 + 10, constants.pygameWindowWidth/8 * 3 + 20, 3 * constants.pygameWindowDepth/4 + 10, 1)
    text = "0%"
    font = pygame.font.Font(pygame.font.get_default_font(), 13)
    text = font.render(text, True, (0,0,0))
    pygameWindow.screen.blit(text, (constants.pygameWindowWidth/8 - 50, 3 * constants.pygameWindowDepth/4 + 6))

    # middle, current session
    pygameWindow.Draw_Graph(constants.pygameWindowWidth/4 - 10, 3 * constants.pygameWindowDepth/4 - 90, 20, 100, (0,255,0))
    if(sessionAttempted > 0):
        pygameWindow.Draw_Graph(constants.pygameWindowWidth/4 - 10, 3 * constants.pygameWindowDepth/4 - 90, 20, 101.0 - (sessionSuccess / float(sessionAttempted) * 100.0), (255,0,0))
    
    else:
        pygameWindow.Draw_Graph(constants.pygameWindowWidth/4 - 10, 3 * constants.pygameWindowDepth/4 - 90, 20, 100, (0,255,0))
        
    #left, previous sessions
    if(userRecord["attempted"] > 0):
        pygameWindow.Draw_Graph(constants.pygameWindowWidth/8 - 10, 3 * constants.pygameWindowDepth/4 - 90, 20, 100, (0,255,0))
        pygameWindow.Draw_Graph(constants.pygameWindowWidth/8 - 10, 3 * constants.pygameWindowDepth/4 - 90, 20, 101.0 - userRecord["successful"] / float(userRecord["attempted"]) * 100.0, (255,0,0))
        pygameWindow.Draw_Image(clock, constants.pygameWindowWidth/8 - 10, 3 * constants.pygameWindowDepth/4 + 15, 20, 20)

    #right, other users
    if (databaseAttempted > 0):
        pygameWindow.Draw_Graph(constants.pygameWindowWidth/8 * 3 - 10, 3 * constants.pygameWindowDepth/4 - 90, 20, 100, (0,255,0))
        pygameWindow.Draw_Graph(constants.pygameWindowWidth/8 * 3 - 10, 3 * constants.pygameWindowDepth/4 - 90, 20, 101.0 - databaseSuccess / float(databaseAttempted) * 100.0, (255,0,0))
        pygameWindow.Draw_Image(group, constants.pygameWindowWidth/8 * 3 - 10, 3 * constants.pygameWindowDepth/4 + 10, 20, 20)

    #bottom, numPredictions
    pygameWindow.Draw_Graph(constants.pygameWindowWidth/8, 3 * constants.pygameWindowDepth/4 + 70, 143, 20, (100,100,100))
    pygameWindow.Draw_Graph(constants.pygameWindowWidth/8, 3 * constants.pygameWindowDepth/4 + 70, numPredictions * 16, 20, (0,255,0))
    if (numPredictions == 0):
        pygameWindow.Draw_Image(movehand, constants.pygameWindowWidth/8 + 150, 3 * constants.pygameWindowDepth/4 + 70, 40, 40)
    
    minimumTimer = 10 - (userRecord["digit" + str(randInt) + "attempted"])
    if((10 - (userRecord["digit" + str(randInt) + "attempted"])) < 5):
        minimumTimer = 5
        
    pygameWindow.Draw_Image(handSymbols[randInt], constants.pygameWindowWidth / 2, 0, (constants.pygameWindowWidth / 2), (constants.pygameWindowDepth / 2))    
    if (userRecord["digit" + str(randInt) + "attempted"] < 6):
        pygameWindow.Draw_Image(handImages[randInt], constants.pygameWindowWidth / 2, constants.pygameWindowDepth / 2, (constants.pygameWindowWidth / 2), (constants.pygameWindowDepth / 2))
    
    if (isHandCentered() > 0):
        programState = 1

    if (len(frame.hands) == 0):
        programState = 0

    elif ((time.time() - timer) > minimumTimer):
        timer = time.time()
        pygameWindow.Draw_Image(incorrect, 0, 0, (constants.pygameWindowWidth), (constants.pygameWindowDepth)) 
        userRecord["digit" + str(randInt) + "attempted"] += 1
        userRecord["attempted"] += 1
        sessionAttempted += 1
        if (((userRecord["successful"] / 3) + 1) > 9):
            randInt = random.randint(0, 9)
        else:
            randInt = random.randint(0, (userRecord["successful"] / 3) + 1)
        numPredictions = 0

    elif (numPredictions == 10):
        userRecord["digit" + str(randInt) + "attempted"] += 1
        userRecord["attempted"] += 1
        sessionAttempted +=1
        programState = 3
        

def HandleState3():
    global programState, randInt, k, numPredictions, timer, sessionSuccess
    k = 0
    numPredictions = 0
    userRecord["successful"] += 1
    sessionSuccess += 1
    userRecord["digit" + str(randInt) + "success"] += 1
    if (((userRecord["successful"] / 3) + 1) > 9):
        randInt = random.randint(0, 9)
    else:
        randInt = random.randint(0, (userRecord["successful"] / 3) + 1)
    Handle_Frame(frame)
    pygameWindow.Draw_Image(correct, 0, 0, (constants.pygameWindowWidth), (constants.pygameWindowDepth))
    pickle.dump(database, open('userData/database.p', 'wb'))

    if (isHandCentered() > 0):
        programState = 1

    elif (len(frame.hands) == 0):
        programState = 0
    
    else:
        timer = time.time()
        programState = 2

#MAIN
controller = Leap.Controller()
randInt = random.randint(0, (userRecord["successful"] / 3) + 1)
while True:
    k = 0
    pygameWindow.Prepare()
    frame = controller.frame()

    if (programState == 0):
        HandleState0()

    if (programState == 1):
        HandleState1()

    if (programState == 2):
        HandleState2()

    if (programState == 3):
        HandleState3()

    pygameWindow.Reveal()
    
