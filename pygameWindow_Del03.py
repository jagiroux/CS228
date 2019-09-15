import pygame
from constants import pygameWindowWidth, pygameWindowDepth

class PYGAME_WINDOW:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((pygameWindowWidth, pygameWindowDepth))

    def Prepare(self):
        self.screen.fill((255,255,255))

    def Reveal(self):
        pygame.display.update()

    def Draw_Black_Circle(self,x,y):
        pygame.draw.circle(self.screen,(0,0,0) ,(x,y), 25)

    def Draw_Line(self, base_x, base_y, tip_x, tip_y, size, color):
        pygame.draw.line(self.screen, color, (base_x, base_y), (tip_x, tip_y), size)

    
