import pygame
import sys
from fish_explode_utils import make_background, Player, add_enemies, add_coins
from parameters import *
from enemies import enemies, Enemy
from coins2 import coins

import random


pygame.init()
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.music.load("assests/sprites/bomb_explode.ogg")

player_lives = 3
player_life_image = pygame.image.load("assests/sprites/player_life_image.png")
player_life_image = pygame.transform.scale(player_life_image, (24, 24))
player_life_image.set_colorkey((255,255,255))
font = pygame.font.Font(None, 36)
score = 0





def show_game_over():
    font = pygame.font.Font(None, 40)
    text = font.render('Game Over. Score: ' + str(score) + ' Press R to Restart', True, (0, 0, 0))
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 2))
    return text, text_rect

def show_start_menu():
    font = pygame.font.Font(None, 50)
    text_start = font.render('Press SPACE to Start', True, (0, 0, 0))
    text_rect_start = text_start.get_rect(center=(screen_width // 2, screen_height // 2))
    return text_start, text_rect_start


def start_game(level):
    # Initialize game elements
    make_background(background)
    add_enemies(enemies, level) #Increases the nubmer of enemies with each level
    add_coins(coins, level * 10)
    player_1 = Player(screen, 'shark', x=0, y=0)
    return player_1


def check_collisions(player, enemies, coins):
    collide_enemies = pygame.sprite.spritecollide(player,enemies, False, pygame.sprite.collide_rect_ratio(0.65))
    collide_coins = pygame.sprite.spritecollide(player,coins, True, pygame.sprite.collide_rect_ratio(0.65))
    if collide_coins:
        add_coins(coins, 1)
    return collide_enemies, collide_coins


#Return both the player and the enemies to origal starting positions upon game over
def reset_positions(player, enemies, coins):
    player.reset_position()
    for enemy in enemies:
        enemy.reset_position()
    for coin in coins:
        coin.reset_position()


def show_instruction():
    font = pygame.font.Font(None, 30)
    text = font.render('Avoid the bombs and outlast the timer', True, (0, 0, 0))
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 3))
    return text, text_rect


def show_level_start(level):
    font = pygame.font.Font(None, 50)
    text = font.render(f'Level {level}', True, (0, 0, 0))
    text_rect = text.get_rect(center=(screen_width // 2, screen_height // 4))
    return text, text_rect


def show_level_complete():
    font = pygame.font.Font(None, 50)
    text = font.render('You passed this level!', True, (0, 0, 0))
    text_rect = text.get_rect(center=(screen_width // 2, screen_height //2 ))
    return text, text_rect

def increase_difficulty(level):
    #Adjust game parameters for increased difficulty with each level
    num_enemies = level *5
    time_limit = level *5000
    new_enemies = pygame.sprite.Group()
    add_enemies(new_enemies, num_enemies)
    return new_enemies, time_limit


def reset_game_state():
    global level, game_over, start_menu, game_started, player_lives
    level = 1
    game_over = False
    start_menu = True
    game_started = False
    player_lives = 3
    pygame.mixer.music.load("assests/sprites/game_music.ogg")
    pygame.mixer.music.set_volume(.5)
    pygame.mixer.music.play(1)



def display_player_lives(image, lives, screen):
    for i in range(lives):
        screen.blit(image, (screen_width -40 *(i+1), 10))
def check_game_over():
    global player_lives, game_over
    if player_lives <= 0:
        game_over = True
        pygame.mixer.music.stop()

def wait_time(time):
    n = pygame.time.get_ticks()
    while (pygame.time.get_ticks() - n) < time:
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()










screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
pygame.display.set_caption('fish_explode')







background = screen.copy()


start_menu = True
text_start, text_rect_start = show_start_menu()
game_over = False
text_game_over, text_rect_game_over = show_game_over()
text_win, text_rect_win = show_level_complete()

#Music Set up
pygame.mixer.music.load("assests/sprites/game_music.ogg")
pygame.mixer.music.set_volume(.5)
pygame.mixer.music.play(1)
collect_sound = pygame.mixer.Sound('assests/sprites/Eating_fish.ogg')

# Font for score.
# c_font = pygame.font.Font(name='',size=128)
c_font = pygame.font.SysFont('Comic Sans MS', 30)

running = True
game_started = False
level = 1
start_time = 0  # Initialize start_time here
time_limit = 10000
enemies = pygame.sprite.Group()  # Initialize enemies as a sprite group
reset_game_state() #initializing the game state
restarting_level = False
while running:
    #Display the player lives as images on the screen

    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                start_menu = False
                if not game_started:
                    player_1 = start_game(level)
                    game_started = True
                    start_time = pygame.time.get_ticks()
                    pygame.mixer.music.play(-1)
                    enemies.empty()
                    enemies.add(Enemy(random.randint(screen_width, screen_width + 20), random.randint(0, screen_height - 1.5 * Player_size)))
                    enemies.add(Enemy(random.randint(screen_width, screen_width + 20), random.randint(0, screen_height - 1.5 * Player_size)))

            elif event.key == pygame.K_1:
                reset_game_state()  # Restart the game when '1' is pressed

            elif event.key == pygame.K_r and (game_over or restarting_level):
                if game_over:
                    reset_game_state()
                    score = 0
                    start_menu = True
                    game_over = False
                else:
                    player_lives -= 1
                    check_game_over()
                    if not game_over:
                        restarting_level = True  # Set the flag to indicate that the level is restarting
                        wait_time(1000)  # Add a delay to allow the player to see the game state after losing a life
                        start_time = pygame.time.get_ticks()
                        reset_positions(player_1, enemies, coins)
                        restarting_level = False  # Reset the flag after the delay

    screen.blit(background, (0, 0))  # displays the background

    #Draw the start menu on the screen
    if start_menu:
        screen.blit(start_menu_image, (0,0))
        text_start, text_rect_start = show_start_menu()
        text_level, text_rect_level = show_instruction()
        screen.blit(text_start, text_rect_start)
        screen.blit(text_level, text_rect_level)

    elif not game_over and not start_menu:
        time_display = int((pygame.time.get_ticks() - start_time) - ((pygame.time.get_ticks() - start_time)%100))/1000
        time = font.render(str(time_display), False, (0,0,0))
        screen.blit(time, (0,0))

        enemies.update()
        coins.update()
        coins.draw(screen)
        player_1.move_player()
        player_1.draw()
        display_player_lives(player_life_image, player_lives, screen)



    #Check to see if the bombs goes off the screen
        for enemy in enemies:
            if enemy.rect.x < -enemy.rect.width:
                enemies.remove(enemy)
                add_enemies(enemies, 1)

        for coin in coins:
            if coin.rect.x < -coin.rect.width:
                coins.remove(coin)
                add_coins(coins, 1)

        check_bomb, check_coin = check_collisions(player_1, enemies, coins)
        #Check for collisions between player and enemies
        if check_bomb:
            player_lives -= 1
            check_game_over()
            pygame.mixer.music.load("assests/sprites/bomb_explode.ogg")
            pygame.mixer.music.set_volume(.3)
            pygame.mixer.music.play(1)
            if not game_over:
                restarting_level = True
                wait_time(1000)
                reset_positions(player_1, enemies, coins)
                start_time = pygame.time.get_ticks()
                pygame.mixer.music.load("assests/sprites/game_music.ogg")
                pygame.mixer.music.set_volume(.5)
                pygame.mixer.music.play(1)
                restarting_level = False


        if check_coin:
            score += 1
            collect_sound.play()











        else:
            enemies.draw(screen)


        if pygame.time.get_ticks() - start_time > time_limit:  # This is checking to see of the toime limit has been reached
            screen.blit(text_win, text_rect_win)
            pygame.display.flip()

            # Transition to the next level
            wait_time(2000)
            level += 1
            if level <= MAX_LEVELS:
                enemies, time_limit = increase_difficulty(level)
                reset_positions(player_1, enemies, coins)
                game_over = False

                text_level_start, text_rect_level_start = show_level_start(level)
                screen.blit(text_level_start, text_rect_level_start)
                pygame.display.flip()
                wait_time(2000)
                start_time = pygame.time.get_ticks()
            else:
                victory_font = pygame.font.Font(None, 50)
                victory_text = victory_font.render('Congratulations! You\'ve completed all levels.', True,
                                                   (255, 255, 255))
                victory_rect = victory_text.get_rect(center=(screen_width // 2, screen_height // 2))
                screen.blit(victory_text, victory_rect)
                pygame.display.flip()

                # Wait for a moment and then exit the loop
                wait_time(3000)  # Wait for 3 seconds
                running = False  # Exit the loop

    else:
        # Display game over screen
        screen.blit(text_game_over, text_rect_game_over)


    # Display score.
    txt = f'Score {score}'
    d_txt = font.render(txt, False,(0,0,0))
    screen.blit(d_txt, (0, 610 ))


    pygame.display.flip()

    clock.tick(60)




pygame.quit()
sys.exit()







#Display the score
# have the game music continue and sound affect for eating a fish at the same time
