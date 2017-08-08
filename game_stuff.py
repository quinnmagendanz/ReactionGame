from tkinter import *
import os, pygame, time, sys, pickle, random
from pygame.locals import *
from Fireball import *
from breakout_game import *
from dial import *
from radar import *

LENGTH_OF_TEST = 9000 # 5min = 9000

TEST_NUMBER = 1

# initialize game variables
pygame.init()

DOWNRIGHT = 3
UPRIGHT = 9
UPLEFT = 7
DOWNLEFT = 1
WINNING_PLAYER = 0
WHEIGHT = 720
WWIDTH = 1360
# Color definitions
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
PLAYERSPEED = 9
numOfPlayers = 0

comments = ['Report number of hostile units.', 'Are you on offense or defense?', 'Are there SAM sites?']

basicFont = pygame.font.SysFont(None, 48)
smallFont = pygame.font.SysFont(None, 24)
# Enable this to make the mouse disappear when over our window
pygame.mouse.set_visible(0)
# This is a font we use to draw text on the screen (size 36)
font = pygame.font.Font(None, 36)
# Make global to facilitate coding
player1 = 0
player = 0
ball = 0
random.seed()

# create main game window ------------------------------------------------------
display_surface = pygame.display.set_mode((WWIDTH, WHEIGHT), 0, 32)

fire_area = Rect(0,0,WWIDTH/2-1, WHEIGHT/2-1)
break_area = Rect(WWIDTH/2,0,WWIDTH/2-1, WHEIGHT/2-1)
map_area = Rect(10,WHEIGHT/2+10, WWIDTH/4-21,WHEIGHT/2-WHEIGHT*.05-10)
radar_area = Rect(3*WWIDTH/4, WHEIGHT/2+10-1, WWIDTH/4,WHEIGHT/2-WHEIGHT*.05-1)
pressure_area = Rect(WWIDTH/4,3*WHEIGHT/4, WWIDTH/8-1, WHEIGHT/4-1)
engine_area = Rect(3*WWIDTH/8,3*WHEIGHT/4, WWIDTH/8-1, WHEIGHT/4-1)
airspeed_area = Rect(4*WWIDTH/8,3*WHEIGHT/4, WWIDTH/8-1, WHEIGHT/4-1)
angle_area = Rect(5*WWIDTH/8,3*WHEIGHT/4, WWIDTH/8-1, WHEIGHT/4-1)
question_area = Rect(WWIDTH/4, WHEIGHT/2+10, WWIDTH/2-1, WHEIGHT/4-20-10)

windowSurface = display_surface.subsurface(fire_area)
screen = display_surface.subsurface(break_area)
map_surface = display_surface.subsurface(map_area)
radar_surface = display_surface.subsurface(radar_area)
pressure_surface = display_surface.subsurface(pressure_area)
engine_surface = display_surface.subsurface(engine_area)
airspeed_surface = display_surface.subsurface(airspeed_area)
angle_surface = display_surface.subsurface(angle_area)
question_surface = display_surface.subsurface(question_area)

fire_init(windowSurface)
break_init(screen)

map_image = pygame.image.load('images/map.png')
map_surface.blit(map_image, (0,0))

radar_back = pygame.image.load('images/Treatment 1/Radar background.png')
radar_surface.blit(radar_back, (0,0))
radar_init(radar_surface, TEST_NUMBER)

# dails on bottom
dim = WHEIGHT//4-20
if TEST_NUMBER == 3:
    pressure = Color_dial(0,0,dim,dim)
elif TEST_NUMBER == 2:
    pressure = Middle_dial(0,0,dim,dim)
else:
    pressure = Digits(0,0,dim,dim)

engine = Generic(0,0,dim,dim)
airspeed = TurnCoord(0,0,dim,dim)
angle = RfSignal(0,0,dim,dim)

pressure_vals = []
for ind in range(LENGTH_OF_TEST//3):
    pressure_vals.append((ind/(LENGTH_OF_TEST//3)*10000)**.5)
pressure_vals.reverse()
pressure_vals.extend([0]*LENGTH_OF_TEST)


def main():
    # Clock to limit speed
    clock = pygame.time.Clock()

    upKey = 0
    downKey = 0
    leftKey = 0
    rightKey = 0
    spaceKey = 0

    out_report = False
    # track breakout end
    game_over = True
    #track fireball end
    GAME_ENDED = True
    # track score
    FUCKUPS = -2

    # Main program loop
    pygame.time.wait(1000)
    print("Start time: " + str(pygame.time.get_ticks()) + " milliseconds")
    counter = 0
    counter1 = 0
    counter2 = LENGTH_OF_TEST//5
    while counter < LENGTH_OF_TEST:  # If we are done (5 min), print game over
        counter += 1
        counter1 += 1
        counter2 += 1
        if game_over:
            FUCKUPS += 1
            player = create_blocks()
            game_over = False
        if GAME_ENDED:
            FUCKUPS += 1
            player1 = build_fire()
            GAME_ENDED = False

        # Limit to 30 fps
        clock.tick(30)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    upKey = 1
                if event.key == K_DOWN:
                    downKey = 1
                if event.key == K_LEFT:
                    leftKey = 1
                if event.key == K_RIGHT:
                    rightKey = 1
                if event.key == K_SPACE and spaceKey == 0:
                    spaceKey = 1
                    print("Report time: " + str(pygame.time.get_ticks()) + " milliseconds")
                if event.key == K_LSHIFT:
                    if pressure_vals[counter2] > pressure_vals[counter1]:
                        counter1 = 0
                    else:
                        counter2 = 0
                    print("Pressure error time: " + str(pygame.time.get_ticks()) + " milliseconds")

            if event.type == KEYUP:
                if event.key == K_UP:
                    upKey = 0
                if event.key == K_DOWN:
                    downKey = 0
                if event.key == K_LEFT:
                    leftKey = 0
                if event.key == K_RIGHT:
                    rightKey = 0
                if event.key == K_SPACE:
                    spaceKey = 0
                    question_surface.fill(BLACK)
                    radar_init(radar_surface, TEST_NUMBER)
        # Handle the player movement
        if upKey:
            player1.move(-PLAYERSPEED)
        if downKey:
            player1.move(PLAYERSPEED)
        if rightKey:
            player.move(PLAYERSPEED)
        if leftKey:
            player.move(-PLAYERSPEED)

        # step each game and get end status
        GAME_ENDED = update_fireball()
        game_over = update_breakout(game_over)

        update_radar(radar_surface, radar_back)

        if pressure_vals[counter1] < 20 and out_report is False:
            print("Zero gas time: " + str(pygame.time.get_ticks()) + " milliseconds")
            out_report = True
        pressure.update(pressure_surface, pressure_vals[counter1], int(pressure_vals[counter2]))
        engine.update(engine_surface, counter)
        airspeed.update(airspeed_surface, 20*math.cos(counter/40), 20*math.sin(counter/20))
        angle.update(angle_surface, counter, (LENGTH_OF_TEST-counter)**2, counter)

        if counter % (LENGTH_OF_TEST//10) == 0:
            question_surface.fill(BLACK)
            report = smallFont.render('Report:', 0, WHITE).convert()
            question = basicFont.render(comments[random.randint(0, 2)], 0, WHITE).convert()
            question_surface.blit(report, (40,20))
            question_surface.blit(question, (40, 50))
    print("End time: " + str(pygame.time.get_ticks()) + " milliseconds")
    print("Number of Errors: " + str(FUCKUPS))
    pygame.quit()

main()

