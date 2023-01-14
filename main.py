import sys
import random
import pygame as pg
from pygame.locals import *

# === CONSTANS === (UPPER_CASE names)
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)

SCREEN_WIDTH  = 1600
SCREEN_HEIGHT = 800

class Bullet:
    def __init__(self, position, speed):
        self.position = position
        self.speed = speed
    def update(self):
        self.position += self.speed

class Player:
    def __init__(self,x,y,width,height,color):
        self.x = x
        self.y = y 
        self.width = width
        self.height = height
        self.color = color
        self.rect = pg.Rect(x,y,width,height)
        self.center = self.rect.center
    def update(self,x,y,width,height,color):
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.height = height
        self.rect = pg.Rect(x,y,width,height)
        self.center = self.rect.center
    def draw(self,surface):
        pg.draw.rect(surface, self.color, self.rect)
    def drawGun(self,screen,color,start,end):
        self.gun = pg.draw.line(screen, color, start, end)

class Scav(pg.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pg.Surface((16,16))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def update(self):
        dir_x = scav_patrol_dir(random.randint(1,3))
        dir_y = scav_patrol_dir(random.randint(1,3))
        self.rect.x += dir_x
        self.rect.y += dir_y

def scav_patrol_dir(num):
    if num == 1:
        return 2
    elif num == 2:
        return -2
    elif num == 3:
        return 0

def main():
    #init
    screen = pg.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    #objects
    #PMC
    player = Player(64, 54, 16, 16, WHITE)
    start = pg.math.Vector2(player.center)
    end = start
    length = 15
    #Scavs
    scav = Scav(500,500)
    scavs = pg.sprite.Group()
    scavs.add(scav)
    #gameplay loop
    clock = pg.time.Clock()
    is_running = True

    bullets = []
    while is_running:
        for i, bullet in enumerate(bullets):
            bullet.update()
            if bullet.position.x < 0 or bullet.position.x > SCREEN_WIDTH or bullet.position.y < 0 or bullet.position.y > SCREEN_HEIGHT:
                bullets.pop(i)
            else:
                pos_x = int(bullet.position.x)
                pos_y = int(bullet.position.y)
                pg.draw.line(screen, (0,255,0), (pos_x,pos_y), (pos_x,pos_y))
        mouse = pg.mouse.get_pos()
        end = start + (mouse - start).normalize() * length
        for event in pg.event.get():
            #global events
            if event.type == pg.QUIT:
                is_running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    is_running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse = pg.mouse.get_pos()
                distance = mouse - start
                position = pg.math.Vector2(start)
                speed = distance.normalize()*8
                if len(bullets) < 5:
                    bullet = Bullet(position, speed)
                    bullets.append(bullet)
        
        pg.display.update()
        mv = 4
        keys = pg.key.get_pressed()
        if keys[pg.K_LSHIFT]:
            mv = 6
        if keys[pg.K_a]:
            start.x -= mv
        if keys[pg.K_d]:
            start.x += mv
        if keys[pg.K_s]:
            start.y += mv
        if keys[pg.K_w]:
            start.y -= mv
        #pg.draw.rect(screen,(150,200,20),player)
        screen.fill(BLACK)
        player.update(start.x,start.y,16, 16,WHITE)
        player.draw(screen)
        player.drawGun(screen, GREEN, start, end)
        scavs.draw(screen)
        scavs.update()
        clock.tick(60)

if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()