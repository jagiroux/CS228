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

    def Draw_Black_Line(self, base_x, base_y, tip_x, tip_y, size):
        pygame.draw.line(self.screen, (0,0,0), (base_x, base_y), (tip_x, tip_y), size)

    def Draw_Image(self, image, x, y, scale_x, scale_y):
        image = pygame.transform.scale(image, (scale_x, scale_y))
        self.screen.blit(image, (x, y))

    def Draw_Graph(self, x, y, width, height, color):
        pygame.draw.rect(self.screen, color, (x,y,width,height), 0)
        
    
