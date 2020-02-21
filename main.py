import pygame
from math import *
import time

# initialize the game
pygame.init()

# create screen
screen = pygame.display.set_mode((1100, 700))

# title and icon
pygame.display.set_caption("Worms")
icon = pygame.image.load("imgWorms.png")
pygame.display.set_icon(icon)

# load the player and set position
wormsLeft = pygame.image.load("imgWorms.png")
wormsLeft = pygame.transform.scale(wormsLeft, (50, 50))
wormsRight = pygame.transform.flip(wormsLeft, True, False)

# set the player image and his coordinates
playerImg = wormsRight
playerImg = pygame.transform.scale(playerImg, (50, 50))
playerX = 100
playerY = 500

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

time_choose = 0

font = pygame.font.SysFont("Times New Roman", 18)
display_name_player1 = font.render(namePlayer1, 1, (0, 255, 0))


def display_game():
    # draw a black screen
    screen.fill((0, 0, 0))
    display_timer = font.render(str(round(time_choose, 3)), 1, (255, 255, 255))
    display_action_points = font.render(str(playerPoints), 1, (255, 255, 255))
    screen.blit(display_name_player1, (playerX + 25, playerY - 20))
    screen.blit(display_action_points, (10, 10))
    # draw the player
    screen.blit(playerImg, (playerX, playerY))
    # draw the weapons
    screen.blit(grenade_image, rect_grenade)
    screen.blit(missile_image, rect_missile)
    # draw the start of the trajectory
    if bool_visualize_trajectory:
        visualize_trajectory()
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
        speed += 1
    elif key_pressed[pygame.K_LEFT]:
        speed -= 1
    elif key_pressed[pygame.K_KP_ENTER]:
        set_speed = 0
    if speed < 35:
        speed = 35
    if speed > 100:
        speed = 100


j = 1
bool_time_select = False


def shot():
    global j
    global time_choose
    global bool_time_select
    if weapon_selected == "grenade":
        if time_choose == 0 or not bool_time_select:
            print(bool_time_select)
            if key_pressed[pygame.K_RIGHT] and time_choose < 10:
                time_choose += .03
            elif key_pressed[pygame.K_LEFT] and time_choose > 0:
                time_choose -= .03
            if time_choose > 0 and key_pressed[pygame.K_KP_ENTER]:
                bool_time_select = True
        else:
            j = 0
            y_previous = 10
            y = 0
            time_pass = 0
            while True:
                j += .1
                time.sleep(.03)
                time_pass += .03
                x = cos(angle / 180 * pi) * speed * j + 35 + playerX
                if j != 0:
                    y_previous = y
                y = (9.82) * (j * j / 2) + sin(angle / 180 * pi) * speed * j + playerY - 20
                display_game()
                if y < y_previous:
                    screen.blit(grenade_weapon, (x, y))
                else:
                    screen.blit(pygame.transform.flip(grenade_weapon, False, True), (x, y))
                pygame.display.update()
                if time_pass >= time_choose:
                    display_game()
                    screen.blit(explosion_image, (x, y))
                    pygame.display.update()
                    time.sleep(0.5)
                    break

    elif weapon_selected == "missile":
        j = 0
        y_previous = 10
        y = 0
        while True:
            j += .1
            time.sleep(.03)
            x = cos(angle / 180 * pi) * speed * j + 35 + playerX
            if j != 0:
                y_previous = y
            y = (9.82) * (j * j / 2) + sin(angle / 180 * pi) * speed * j + playerY - 20
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
                break


def calculate_trajectory(i):
    global x
    x = cos(angle / 180 * pi) * speed * i + 35 + playerX
    global y
    y = (9.82) * (i * i / 2) + sin(angle / 180 * pi) * speed * i + playerY - 20
    # print("i : ", i, " x : ", int(x), " and y : ", int(y))
    pygame.draw.circle(screen, 0xFF0000, [int(x), int(y)], 1, 1)


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
