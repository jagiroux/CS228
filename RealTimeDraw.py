import random
from pygameWindow import PYGAME_WINDOW

x = 500
y = 500

def Perturb_Circle_Position():
    global x,y
    fourSidedDieRoll = random.randint(1,4)

    if (fourSidedDieRoll == 1):
        x-=1
    elif (fourSidedDieRoll == 2):
        x+=1
    elif (fourSidedDieRoll == 3):
        y-=1
    else:
        y+=1

pygameWindow = PYGAME_WINDOW()

while True:
    pygameWindow.Prepare()
    Perturb_Circle_Position()
    pygameWindow.Draw_Black_Circle(x,y)
    pygameWindow.Reveal()

