"""
 Sample Breakout Game

 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/
"""

# --- Import libraries used for this program

import math
import pygame

# Size of break-out blocks
block_width = 23
block_height = 15
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (20, 20, 20)


def break_init(surface):
    global screen
    screen = surface


def update_breakout(game_over):
    # Update the ball and player position as long
    # as the game is not over.
    if not game_over:
        # Update the player and ball positions
        game_over = ball.update()
        screen.fill(BLACK)

    # See if the ball hits the player paddle
    if pygame.sprite.spritecollide(player, balls, False):
        # The 'diff' lets you try to bounce the ball left or right
        # depending where on the paddle you hit it
        diff = (player.rect.x + player.width / 2) - (ball.rect.x + ball.width / 2)

        # Set the ball's y position in case
        # we hit the ball on the edge of the paddle
        ball.rect.y = screen.get_height() - player.rect.height - ball.rect.height - 1
        ball.bounce(diff)

    # Check for collisions between the ball and the blocks
    deadblocks = pygame.sprite.spritecollide(ball, blocks, True)

    # If we actually hit a block, bounce the ball
    if len(deadblocks) > 0:
        ball.bounce(0)

        # Game ends if all the blocks are gone
        if len(blocks) == 0:
            game_over = True

    # Draw Everything
    allsprites.draw(screen)

    # Flip the screen and show what we've drawn
    pygame.display.flip()

    return game_over

    # --- Create blocks
def create_blocks():
    # breakout init
    global ball
    global player
    global allsprites
    global blocks
    global balls
    # Clear the screen
    screen.fill(BLACK)
    # Create sprite lists
    blocks = pygame.sprite.Group()
    balls = pygame.sprite.Group()
    allsprites = pygame.sprite.Group()

    # Create the player paddle object
    player = Player_break()
    allsprites.add(player)

    # Create the ball
    ball = Ball_break()
    allsprites.add(ball)
    balls.add(ball)

    # The top of the block (y position)
    top = 20

    # Number of blocks to create
    blockcount = screen.get_width()//(block_width + 2)
    # Five rows of blocks
    for row in range(5):
        # 32 columns of blocks
        for column in range(0, blockcount):
            # Create a block (color,x,y)
            block = Block(GREEN, column * (block_width + 2) + 1, top)
            blocks.add(block)
            allsprites.add(block)
        # Move the top of the next row down
        top += block_height + 2

    return player

class Block(pygame.sprite.Sprite):
    """This class represents each block that will get knocked out by the ball
    It derives from the "Sprite" class in Pygame """

    def __init__(self, color, x, y):
        """ Constructor. Pass in the color of the block,
            and its x and y position. """

        # Call the parent class (Sprite) constructor
        super().__init__()

        # Create the image of the block of appropriate size
        # The width and height are sent as a list for the first parameter.
        self.image = pygame.Surface([block_width, block_height])

        # Fill the image with the appropriate color
        self.image.fill(color)

        # Fetch the rectangle object that has the dimensions of the image
        self.rect = self.image.get_rect()

        # Move the top left of the rectangle to x,y.
        # This is where our block will appear..
        self.rect.x = x
        self.rect.y = y


class Ball_break(pygame.sprite.Sprite):
    """ This class represents the ball
        It derives from the "Sprite" class in Pygame """

    # Speed in pixels per cycle
    speed = 4.0

    # Floating point representation of where the ball is
    x = 0.0
    y = 180.0

    # Direction of ball (in degrees)
    direction = 200

    width = 10
    height = 10

    # Constructor. Pass in the color of the block, and its x and y position
    def __init__(self):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Create the image of the ball
        self.image = pygame.Surface([self.width, self.height])

        # Color the ball
        self.image.fill(WHITE)

        # Get a rectangle object that shows where our image is
        self.rect = self.image.get_rect()

        # Get attributes for the height/width of the screen
        self.screenheight = screen.get_height()
        self.screenwidth = screen.get_width()

    def bounce(self, diff):
        """ This function will bounce the ball
            off a horizontal surface (not a vertical one) """

        self.direction = (180 - self.direction) % 360
        self.direction -= diff

    def update(self):
        """ Update the position of the ball. """
        # Sine and Cosine work in degrees, so we have to convert them
        direction_radians = math.radians(self.direction)

        # Change the position (x and y) according to the speed and direction
        self.x += self.speed * math.sin(direction_radians)
        self.y -= self.speed * math.cos(direction_radians)

        # Move the image to where our x and y are
        self.rect.x = self.x
        self.rect.y = self.y

        # Do we bounce off the top of the screen?
        if self.y <= 0:
            self.bounce(0)
            self.y = 1

        # Do we bounce off the left of the screen?
        if self.x <= 0:
            self.direction = (360 - self.direction) % 360
            self.x = 1

        # Do we bounce of the right side of the screen?
        if self.x > self.screenwidth - self.width:
            self.direction = (360 - self.direction) % 360
            self.x = self.screenwidth - self.width - 1

        # Did we fall off the bottom edge of the screen?
        if self.y > self.screenheight:
            return True
        else:
            return False


class Player_break(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the
    player controls. """

    def __init__(self):
        """ Constructor for Player. """
        # Call the parent's constructor
        super().__init__()

        self.width = 75
        self.height = 15
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill((WHITE))

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.screenheight = screen.get_height()
        self.screenwidth = screen.get_width()

        self.rect.x = 0
        self.rect.y = self.screenheight - self.height

    def update(self):
        pass

    def move(self, speed):
        newpos = self.rect.move(speed, 0)
        if newpos.left > 0 and newpos.right < screen.get_width():
            self.rect = newpos

