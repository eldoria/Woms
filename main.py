import pygame
from math import *
import time

# initialize the game
pygame.init()

# create screen
screen = pygame.display.set_mode((1100, 700))
background_picture = pygame.image.load("terrain.jpg")
background = background_picture.convert()
background = pygame.transform.scale(background, (1100, 700))
# title and icon
pygame.display.set_caption("Worms")
icon = pygame.image.load("imgWorms.png")
pygame.display.set_icon(icon)

# load the player and set position
wormsLeft = pygame.image.load("imgWorms.png")
wormsLeft = pygame.transform.scale(wormsLeft, (50, 50))
wormsRight = pygame.transform.flip(wormsLeft, True, False)

# set the players image and his coordinates
playerImg = wormsRight
playerImg = pygame.transform.scale(playerImg, (50, 50))
playerImg2 = wormsLeft
playerX = 100
playerY = 485
playerX2 = 900
playerY2 = playerY

# set the weapons images and display their icon on the top right of the screen
grenade_image = pygame.image.load("grenade.png")
missile_image = pygame.image.load("missile.png")
grenade_image = pygame.transform.scale(grenade_image, (50, 50))
missile_image = pygame.transform.scale(missile_image, (50, 50))
# rect are used in order to check if images are clicked
rect_grenade = grenade_image.get_rect().move(900, 0)
rect_missile = missile_image.get_rect().move(1000, 0)

# display near the player for information on what they are going to shot
grenade_icon = pygame.transform.scale(grenade_image, (15, 15))
missile_icon = pygame.transform.scale(missile_image, (15, 15))

# weapons display on the screen
grenade_weapon = pygame.transform.scale(grenade_image, (25, 25))
missile_weapon = pygame.transform.scale(missile_image, (25, 25))

explosion_image = pygame.image.load("explosion.png")
explosion_image = pygame.transform.scale(explosion_image, (50, 50))

# set the player action points
playerPoints = 2000

# name of player's worm
namePlayer1 = 'J1'
namePlayer2 = 'J2'

player_turn = 'J1'


font = pygame.font.SysFont("Times New Roman", 18)
display_name_player1 = font.render(namePlayer1, 1, (255, 0, 0))
display_name_player2 = font.render(namePlayer2, 1, (0, 0, 255))

bool_update_scene = True




def display_game():
    # draw a black screen
    screen.blit(background, (0, 0))
    display_timer = font.render(str(round(time_choose, 3)), 1, (255, 255, 255))
    display_action_points = font.render(str(playerPoints), 1, (255, 255, 255))
    screen.blit(display_name_player1, (playerX + 25, playerY - 20))
    screen.blit(display_name_player2, (playerX2, playerY2 - 20))
    screen.blit(display_action_points, (10, 10))
    # draw the player
    screen.blit(playerImg, (playerX, playerY))
    screen.blit(playerImg2, (playerX2, playerY))
    # draw the weapons
    screen.blit(grenade_image, rect_grenade)
    screen.blit(missile_image, rect_missile)
    # draw the start of the trajectory
    if bool_visualize_trajectory:
        visualize_trajectory()
    elif (not bool_time_select or bool_shot) and weapon_selected == "grenade":
        shot()
    # draw the icons when the player clicks on the weapons
    if weapon_selected == "grenade":
        screen.blit(grenade_icon, (playerX + 40, playerY - 20))
        screen.blit(display_timer, (200, 10))

    elif weapon_selected == "missile":
        screen.blit(missile_icon, (playerX + 40, playerY - 20))
    # draw the scene
    pygame.display.update()


angle = -60
speed = 80
set_angle = 1
set_speed = 1
bool_key_press = 1
x_init = 35 + playerX
y_init = playerY - 20


def visualize_trajectory():
    # the boolean is use in order to call the second function only when the player release the key space
    global bool_key_press
    if set_angle:
        modify_angle()
    elif set_speed and (key_pressed[pygame.K_KP_ENTER] == 0 or bool_key_press == 0):
        bool_key_press = 0
        modify_speed()
    elif set_speed == 0 and set_angle == 0:
        global bool_visualize_trajectory
        bool_visualize_trajectory = False
        shot()

    # preview the trajectory in order to aim better
    if set_angle != 0 or set_speed != 0:
        for i in range(1, 4):
            calculate_trajectory(i)


# modify the angle of the projectile before shot
def modify_angle():
    global angle
    global set_angle
    if key_pressed[pygame.K_RIGHT]:
        angle += .1
    elif key_pressed[pygame.K_LEFT]:
        angle -= .1
    elif key_pressed[pygame.K_KP_ENTER]:
        set_angle = 0


# modify the speed of the projectile before shot
def modify_speed():
    global speed
    global set_speed
    if key_pressed[pygame.K_RIGHT]:
        speed += .2
    elif key_pressed[pygame.K_LEFT]:
        speed -= .2
    elif key_pressed[pygame.K_KP_ENTER]:
        set_speed = 0
    if speed < 35:
        speed = 35
    if speed > 100:
        speed = 100


j = 0
bool_time_select = False
time_choose = 0
bool_shot = False


def shot():
    global j
    global time_choose
    global bool_time_select
    global bool_shot
    global speed
    # previous j will be use for keep the grenade rotation when the grenade rebound
    previous_j = 0
    # previous x and y are use in order to be add to the new trajectory during the rebound
    # Without them the projectile reappears at the top of the worms after the rebound
    previous_x = 0
    previous_y = 0
    if weapon_selected == "grenade":
        if not bool_time_select:
            if key_pressed[pygame.K_RIGHT] and time_choose < 10:
                time_choose += .03
            elif key_pressed[pygame.K_LEFT] and time_choose > 0:
                time_choose -= .03
            if time_choose > 0 and key_pressed[pygame.K_KP_ENTER]:
                bool_time_select = True
                bool_shot = True
        else:
            bool_shot = False
            time_pass = 0
            while True:
                j += .1
                time.sleep(.03)
                time_pass += .03
                x = cos(angle / 180 * pi) * speed * j + 35 + playerX + previous_x
                y = 9.82 * (j * j / 2) + sin(angle / 180 * pi) * speed * j + playerY - 20 + previous_y
                display_game()
                screen.blit(pygame.transform.rotate(grenade_weapon, -(j + previous_j)*30), (x, y))
                pygame.display.update()

                if y > playerY + 20:
                    previous_j += j
                    j = 0
                    speed = .6 * speed
                    previous_x = x - playerX - 25
                    previous_y = 40
                if time_pass >= time_choose or speed < 10:
                    display_game()
                    screen.blit(explosion_image, (x, y))
                    pygame.display.update()
                    time.sleep(0.5)
                    check_damages(x, y)
                    break

    elif weapon_selected == "missile":
        y_previous = 10
        y = 0
        while True:
            j += .1
            time.sleep(.03)
            x = cos(angle / 180 * pi) * speed * j + 35 + playerX
            if j != 0.1:
                y_previous = y
            y = 9.82 * (j * j / 2) + sin(angle / 180 * pi) * speed * j + playerY - 20
            # print("x : " + str(x) + ", y : " + str(y) + "and j : " + str(j))
            display_game()
            if y < y_previous:
                screen.blit(missile_weapon, (x, y))
            else:
                screen.blit(pygame.transform.flip(missile_weapon, False, True), (x, y))
            pygame.display.update()

            if y > playerY:
                display_game()
                screen.blit(explosion_image, (x, y))
                pygame.display.update()
                time.sleep(0.5)
                check_damages(x, y)
                break


def calculate_trajectory(i):
    global x
    x = cos(angle / 180 * pi) * speed * i + 35 + playerX
    global y
    y = 9.82 * (i * i / 2) + sin(angle / 180 * pi) * speed * i + playerY - 20
    pygame.draw.circle(screen, 0x000000, [int(x), int(y)], 1, 1)


def check_damages(x, y):
    if abs(x - playerX2) < 50 and abs(y - playerY2) < 50:
        game_end()
    elif abs(x - playerX) < 50 and abs(y - playerY) < 50:
        game_end()
    else:
        new_turn()


def game_end():
    font2 = pygame.font.SysFont("Times New Roman", 35)
    display_str = font2.render("Game Over", 1, (255, 255, 255))
    screen.fill((0, 0, 0))
    screen.blit(display_str, (480, 300))
    pygame.display.update()
    time.sleep(4)
    global running
    running = False
    pygame.quit()


def new_turn():
    # swap playerX/PlayerY and PlayerX2 and playerY2
    # inverser l'affichage
    global playerX
    global playerY
    global playerX2
    global playerY2
    global player_turn
    global playerPoints
    global bool_update_scene
    global set_angle
    global set_speed
    global bool_key_press
    global j
    global bool_time_select
    global time_choose
    global bool_shot
    if player_turn == "J1":
        player_turn = "J2"
    else:
        player_turn = "J1"
    tmpX = playerX
    tmpY = playerY
    playerX = playerX2
    playerY = playerY2
    playerX2 = tmpX
    playerY2 = tmpY
    # reset booleans and variables
    playerPoints = 2000
    bool_update_scene = True
    set_angle = 1
    set_speed = 1
    bool_key_press = 1
    j = 0
    bool_time_select = False
    time_choose = 0
    bool_shot = False


weapon_selected = ""
bool_visualize_trajectory = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # check if weapons are selected
    mouse_pos = pygame.mouse.get_pos()

    if rect_grenade.collidepoint(mouse_pos) and pygame.mouse.get_pressed() == (1, 0, 0):
        weapon_selected = "grenade"
        bool_visualize_trajectory = 1
    elif rect_missile.collidepoint(mouse_pos) and pygame.mouse.get_pressed() == (1, 0, 0):
        weapon_selected = "missile"
        bool_visualize_trajectory = 1

    # user's input
    key_pressed = pygame.key.get_pressed()
    if playerPoints > 0:
        # detect the a instead of the q because pygame consider the keyboard to be a QWERTY
        if key_pressed[pygame.K_a]:
            playerX -= .15
            playerPoints -= 1
            playerImg = wormsLeft
        elif key_pressed[pygame.K_d]:
            playerX += .15
            playerPoints -= 1
            playerImg = wormsRight

    # keep the worm on the screen
    if playerX < 0:
        playerX = 0
    elif playerX > 1050:
        playerX = 1050
    display_game()
