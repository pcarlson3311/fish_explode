#dimensions of the screen
import pygame

screen_width = 600
screen_height = 650
Player_size = 60

start_menu_image = pygame.image.load("assests/sprites/start_menu_image.png")
start_menu_image = pygame.transform.scale(start_menu_image, (screen_width, screen_height))
game_over_image = pygame.image.load("assests/sprites/game_over_image_2.png")
game_over_image = pygame.transform.scale(game_over_image, (650, 600))


min_speed = 2
max_speed = 4
max_coin_speed = 2
min_coin_speed = 1

MAX_LEVELS = 5

MAX_LIVES = 3



player_life_image = pygame.image.load("assests/sprites/player_life_image.png")
player_life_image = pygame.transform.scale(start_menu_image, (20, 20))

