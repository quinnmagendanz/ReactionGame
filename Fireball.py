# /usr/bin/env python
"""
Student: Erick Franco
Assignment: 4
Class: CPSCI 386
Title: PyPong!
"""

import os, pygame, time, sys, pickle, random
from pygame.locals import *

DOWNRIGHT = 3
UPRIGHT = 9
UPLEFT = 7
DOWNLEFT = 1
# Color definitions
WHITE = (220, 220, 220)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
PLAYERSPEED = 7
numOfPlayers = 0

class Over:
    def __init__(self):
        self.over = False
    def kill(self):
        self.over = True
    def reset(self):
        self.over = False
GAME_ENDED = Over()
class Score:
    def __init__(self, count, diff):
        self.count = count
        self.diff = diff
    def inc(self):
        self.count += self.diff
    def dec(self):
        self.count -= self.diff * 5
    def get(self):
        return self.count
score = Score(80, 10)

def update_fireball():
    windowSurface.fill(WHITE)
    # Bounce the ball back if it hit
    if player1.rect.colliderect(ball.rect):
        ballSpeed = player1.collidedAt(ball)
        ball.setSpeed(ballSpeed)
        ball.collided()

    # Slow down boss speed on powerup hit
    if ball.rect.colliderect(powerup.rect):
        powerup.alive = 0
        boss.speed = 3
        score.inc()

    threshold = 80
    if score.get() > threshold:
        boss.appear(score.get() / threshold + 1)

    # Draw the player and ball
    sprites.update()
    if boss.isAlive():
        if boss.rect.colliderect(ball.rect):
            boss.hit()
        bossSprite.update()
        bossSprite.draw(windowSurface)
    sprites.draw(windowSurface)
    pygame.display.update()
    return GAME_ENDED.over

def build_fire():
    global boss
    global bossSprite
    global sprites

    GAME_ENDED.reset()

    # Loading Ball
    global ball
    ballSpeed = 1
    ball = Ball_fire()
    ball.setSpeed(ballSpeed)

    # Loading Powerup
    global powerup
    powerup = PowerUp()

    # Loading Players
    global player1
    player1 = Player_fire()
    player1.set(1)
    player2 = Player_fire()
    player2.set(2)

    # Loading boss
    boss = Boss()

    # start one player game
    sprites = pygame.sprite.RenderPlain((ball, player1, powerup))
    bossSprite = pygame.sprite.RenderPlain((boss))

    return player1

def fire_init(surface):
    global windowSurface
    global surface_height
    global surface_width
    windowSurface = surface
    surface_height = windowSurface.get_height()
    surface_width = windowSurface.get_width()


# functions to create our resources
# Taken from: http://www.pygame.org/docs/tut/chimp/chimp.py.html
def load_image(name, colorkey=None):
    fullname = os.path.join('images', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', fullname)
        raise SystemExit(message)
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()


# Define the ball class
class Ball_fire(pygame.sprite.Sprite):
    # The ball class
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image, self.rect = load_image('ball.bmp', -1)
        self.LRspeed = 5
        self.dir = DOWNRIGHT
        self.UDspeed = 1
        self.rect.topleft = 100, 100

    def update(self):
        global WINNING_PLAYER
        if self.dir == DOWNRIGHT:
            self.rect.move_ip(self.LRspeed, self.UDspeed)
        elif self.dir == UPRIGHT:
            self.rect.move_ip(self.LRspeed, self.UDspeed)
        elif self.dir == UPLEFT:
            self.rect.move_ip(-self.LRspeed, self.UDspeed)
        elif self.dir == DOWNLEFT:
            self.rect.move_ip(-self.LRspeed, self.UDspeed)

        if self.rect.top < 0:
            if self.dir == UPRIGHT:
                self.dir = DOWNRIGHT
            elif self.dir == UPLEFT:
                self.dir = DOWNLEFT
            self.UDspeed = -self.UDspeed
        elif self.rect.bottom > surface_height:
            if self.dir == DOWNRIGHT:
                self.dir = UPRIGHT
            elif self.dir == DOWNLEFT:
                self.dir = UPLEFT
            self.UDspeed = -self.UDspeed
        elif self.rect.right > surface_width:  # Added for testing single player
            if self.dir == UPRIGHT:
                self.dir = UPLEFT
            elif self.dir == DOWNRIGHT:
                self.dir = DOWNLEFT
            self.LRspeed = self.LRspeed + .5

            # Beyond 29 the ball doesn't bounce off players
            if self.LRspeed > 29:
                self.LRspeed = 29

        #check if still in bounds
        if self.rect.left < 0:
            GAME_ENDED.kill()


    def collided(self):

        if self.UDspeed < 0:
            if self.dir == DOWNRIGHT or self.dir == UPRIGHT:
                self.dir = UPLEFT
            else:
                self.dir = UPRIGHT
        else:
            if self.dir == DOWNRIGHT or self.dir == UPRIGHT:
                self.dir = DOWNLEFT
            else:
                self.dir = DOWNRIGHT
        self.LRspeed = self.LRspeed + .25
        # Beyond 29 the ball doesn't bounce off players
        if self.LRspeed > 29:
            self.LRspeed = 29

    def setSpeed(self, speed):
        self.UDspeed = speed


# End of class Ball


class Player_fire(pygame.sprite.Sprite):
    # The Player class
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image, self.rect = load_image('player.bmp', GREEN)

    def set(self, num):
        if num == 1:
            self.rect.topleft = 30, 150
        elif num == 2:
            self.image = pygame.transform.flip(self.image, 1, 0)
            self.rect.topright = surface_width - 30, 150
        else:
            print
            'GAME PLAYER NOT FOUND'
            pygame.quit()
            sys.exit()

    def update(self):
        nothing = 1

    def collidedAt(self, object):
        return ((object.rect.centery - self.rect.centery) / 5)

    def move(self, speed):
        newpos = self.rect.move(0, speed)
        if newpos.top > 0 and newpos.bottom < surface_height:
            self.rect = newpos


class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('powerup.bmp', GREEN)
        self.alive = 0

    def set(self):
        self.rect.topleft = surface_width // 2, random.randint(surface_width // 4, surface_width // 2)

    def update(self):
        if self.alive is 0:
            self.alive = 1
            self.set()


class Fireball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image, self.rect = load_image('fireball.bmp', GREEN)
        self.speed = -10
        self.alive = 0

    def update(self):
        if self.alive:
            self.rect.move_ip(self.speed, 0)
            if self.rect.right < 0:
                self.alive = 0
                self.kill()
            if self.rect.colliderect(player1.rect):
                GAME_ENDED.kill()

    def shoot(self, yCoord):
        self.alive = 1
        self.rect.centery = yCoord
        self.rect.right = surface_width - 20


class Boss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.fballSprites = pygame.sprite.RenderPlain()
        self.image, self.rect = load_image('boss.bmp', GREEN)
        self.fireball = []
        for i in range(1, 10):
            self.fireball.append(Fireball())
        self.speed = 5
        self.alive = 0
        self.health = 2
        self.rect.topright = surface_width, random.randint(1, surface_height)
        self.direction = 1
        self.fights = 0
        self.frequency = 9

    def update(self):
        if self.alive:
            if self.direction:
                self.rect.move_ip(0, self.speed)
                if self.rect.bottom > surface_height:
                    self.direction = 0
            else:
                self.rect.move_ip(0, -self.speed)
                if self.rect.top < 0:
                    self.direction = 1
            if self.fights:
                if random.randint(1, 50) == 1:
                    for fball in self.fireball:
                        if fball.alive == 0:
                            fball.shoot(self.rect.centery)
                            fball.add(self.fballSprites)
                            break
            self.fballSprites.update()
            self.fballSprites.draw(windowSurface)

    def appear(self, num):
        if self.alive == 0:
            self.alive = 1
            self.health = 2
            if num > 0:
                self.fights = 1
                self.frequency = num

    def isAlive(self):
        return self.alive

    def hit(self):
        self.health = self.health - 1
        ball.collided()
        if self.health < 1:
            self.alive = 0
            self.fballSprites.empty()
            score.dec()



