import pygame
import random
from parameters import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load("assests/sprites/bomb_image.png"), (60,60)).convert()
        self.image.set_colorkey((0,0,0))
        self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.x =x
        self.y =y
        self.speed = random.uniform(min_speed, max_speed)
        self.rect.center = (x,y)
        self.initial_x = random.randint(600,700)
        self.x = self.initial_x
        self.initial_y = y

    def update(self):
        self.x -= self.speed
        self.rect.x = self.x
    def draw(self, surface):
        print('enemy draw')
        surface.blit(self.image, self.rect)

    def reset_position(self):
        # Reset the enemy's position to the initial position
        print("test2")
        self.rect.x = self.initial_x
        self.rect.y = self.initial_y
        self.x = self.rect.x
        print(self.rect.x,self.rect.y)

enemies = pygame.sprite.Group()



