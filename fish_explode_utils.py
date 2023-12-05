import pygame
import random
from enemies import Enemy,enemies
from parameters import *
from coins2 import Coins, coins

pygame.init()





def make_background(surface):


    #load images
    water = pygame.image.load("assests/sprites/water.png").convert()
    sand = pygame.image.load("assests/sprites/sand.png").convert()


    #draw background
    for x in range(0, surface.get_width(), water.get_width()):
        for y in range(0, surface.get_height(), water.get_height()):
            surface.blit(water, (x,y))

    for x in range(0, surface.get_width(), sand.get_width()):
        surface.blit(sand, (x, surface.get_height() - sand.get_height()))


    #adding the enemies onto the background

def add_enemies(enemies,num_enemeis):
    for _ in range(num_enemeis):
        enemy = Enemy(random.randint(screen_width, screen_width + 20), random.randint(0, screen_height - 1.5 * Player_size))
        enemies.add(enemy)
def add_coins(coins,num_coins):
    for _ in range(num_coins):
        coin = Coins(random.randint(screen_width, screen_width + 20), random.randint(0, screen_height - 1.5 * Player_size))
        coins.add(coin)











class Player: # This the class that defines my player and where it is drawn on the screen
    def __init__(self, screen, color, x=0, y=0):
        #load the player
        pname = f'assests/sprites/{color}_fish.png'
        self.original_image = pygame.transform.scale(pygame.image.load(pname),(60,60)).convert() #This allows me to scale the image to the size that I want
        self.original_image.set_colorkey((255, 255, 255))
        self.player = pygame.transform.flip(self.original_image, True, False)
        self.rect = self.player.get_rect()
        self.rect.topleft = (x, y)
        self.screen = screen
        self.initial_x = 0
        self.initial_y = 0



        self.player_x_spd = screen.get_width()/(2* 60) #This is the x speed of the fish
        self.player_y_spd = screen.get_height()/(2*60) #This is the y speed of the fish





    def draw(self):
        self.screen.blit(self.player, self.rect.topleft)


    def move_player(self):

        #Save the current position
        old_x, old_y, = self.rect.topleft

        keys = pygame.key.get_pressed() # list of pressed keys
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.player_x_spd
            self.player = self.original_image
        if keys[pygame.K_RIGHT]  and self.rect.x < screen_width - self.rect.width:
            self.rect.x += self.player_x_spd
            self.player = pygame.transform.flip(self.original_image, True, False)
        if keys[pygame.K_UP] and self.rect.y > 0:
            self.rect.y -= self.player_y_spd
            self.player = pygame.transform.rotate(self.original_image, 270)
        if keys[pygame.K_DOWN] and self.rect.y < screen_height - 64 - self.rect.height:
            self.rect.y += self.player_y_spd
            self.player = pygame.transform.rotate(self.original_image, 90)


        if not self.screen.get_rect().colliderect(self.rect): # this is saying that if it collides with any aspect of the wall than it will no longer be able to move in that direction
            # If outside the boundaries, revert to the old position
            self.rect.topleft = old_x, old_y

    def reset_position(self):
        self.rect.x = self.initial_x
        self.rect.y = self.initial_y




