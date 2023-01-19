import pygame


# === CONSTANS === (UPPER_CASE names)
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)

SCREEN_WIDTH  = 1600
SCREEN_HEIGHT = 800

class Player:
    def __init__(self,x,y,width,height,color):
        self.x = x
        self.y = y 
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(x,y,width,height)
        self.center = self.rect.center
    def update(self,x,y,width,height,color):
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x,y,width,height)
        self.center = self.rect.center
    def drawGun(self,screen,color,start,end):
        self.gun = pygame.draw.line(screen, color, start, end)
    def draw(self,surface):
        pygame.draw.rect(surface, self.color, self.rect)