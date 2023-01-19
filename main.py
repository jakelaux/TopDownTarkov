import sys
import pygame
import pygame.mouse
from pygame.locals import *
from player import Player
from scav import Scav

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
   
def main():
    # Initialize the screen
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    # Create the crosshair cursor
    crosshair = (
        "   X    ",
        "   X    ",
        "   X    ",
        "XXXXXXX ",
        "   X    ",
        "   X    ",
        "   X    ",
        "        "
    )
    # Create the cursor using the crosshair image
    cursor, mask = pygame.cursors.compile(crosshair, ".", "X")
    # Set the cursor using the cursor and mask
    pygame.mouse.set_cursor((8, 8), (4, 4), cursor, mask)

    #Player
    player = Player(64, 54, 16, 16, WHITE)
    start = pygame.math.Vector2(player.center)
    end = start
    length = 15

    #Scavs
    scav = Scav(500,500)
    scavs = pygame.sprite.Group()
    scavs.add(scav)

    #gameplay loop
    clock = pygame.time.Clock()
    is_running = True
    bullets = []
    while is_running:
        # Handle events 
        for event in pygame.event.get():
            #global events
            if event.type == pygame.QUIT:
                is_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    is_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse = pygame.mouse.get_pos()
                distance = mouse - start
                position = pygame.math.Vector2(start)
                speed = distance.normalize()*8
                if len(bullets) < 5:
                    bullet = Bullet(position, speed)
                    bullets.append(bullet)

        #Handle bullets moving off the screen
        for i, bullet in enumerate(bullets):
            bullet.update()
            if bullet.position.x < 0 or bullet.position.x > SCREEN_WIDTH or bullet.position.y < 0 or bullet.position.y > SCREEN_HEIGHT:
                bullets.pop(i)
            else:
                pos_x = int(bullet.position.x)
                pos_y = int(bullet.position.y)
                pygame.draw.line(screen, (0,255,0), (pos_x,pos_y), (pos_x,pos_y))
        mouse = pygame.mouse.get_pos()
        end = start + (mouse - start).normalize() * length
        
        # handle bullets damaging scav ** refacrot this to the enumberate bullets loop so this isn't even more inefficient
        for bullet in bullets:
            for scav in scavs:
                if bullet.position.x > scav.rect.x and bullet.position.x < scav.rect.x + scav.rect.width:
                    if bullet.position.y > scav.rect.y and bullet.position.y < scav.rect.y + scav.rect.height:
                        scav.take_damage(60)
                        bullets.pop(bullets.index(bullet))

        pygame.display.update()

        # Player Movement
        mv = 4
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LSHIFT]:
            mv = 6
        if keys[pygame.K_a]:
            start.x -= mv
        if keys[pygame.K_d]:
            start.x += mv
        if keys[pygame.K_s]:
            start.y += mv
        if keys[pygame.K_w]:
            start.y -= mv

        screen.fill(BLACK)
        player.update(start.x,start.y,16, 16,WHITE)
        player.draw(screen)
        player.drawGun(screen, GREEN, start, end)
        scavs.draw(screen)
        scavs.update()
        clock.tick(60)

if __name__ == "__main__":
    pygame.init()
    main()
    pygame.quit()
    sys.exit()