import pygame
import random

# === CONSTANS === (UPPER_CASE names)
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED   = (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE  = (  0,   0, 255)

SCREEN_WIDTH  = 1600
SCREEN_HEIGHT = 800

class Scav(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((16,16))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = random.randint(200,500)
        self.speed = 2
        self.patrol_direction = random.choice(["right", "left", "up", "down"])
        self.patrol_distance = random.randint(100,200) # distance the scav will patrol before changing direction
        self.patrol_count = 0 # counter to keep track of distance patrolled
    def update(self):
        if self.patrol_direction == "right":
            self.rect.x += self.speed
            self.patrol_count += self.speed
        elif self.patrol_direction == "left":
            self.rect.x -= self.speed
            self.patrol_count += self.speed
        elif self.patrol_direction == "up":
            self.rect.y -= self.speed
            self.patrol_count += self.speed
        elif self.patrol_direction == "down":
            self.rect.y += self.speed
            self.patrol_count += self.speed
        # check if the scav has patrolled the desired distance
        if self.patrol_count >= self.patrol_distance:
            self.patrol_count = 0
            self.patrol_direction = random.choice(["right", "left", "up", "down"])
    def take_damage(self, damage):
        self.health -= damage
        print(self.health)
        if self.health <= 0:
            self.die()
    def die(self):
        self.kill()
        
def scav_patrol_dir(num):
    if num == 1:
        return 2
    elif num == 2:
        return -2
    elif num == 3:
        return 0