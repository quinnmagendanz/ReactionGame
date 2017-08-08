"""
 This example shows having multiple balls bouncing around the screen at the
 same time. You can hit the space bar to spawn more balls.

 Sample Python/Pygame Programs
 Simpson College Computer Science
 http://programarcadegames.com/
 http://simpson.edu/computer-science/
"""

import pygame
import random

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class Ball(pygame.sprite.Sprite):
	"""
	Class to keep track of a ball's location and vector.
	"""

	def __init__(self, image, rect):
		pygame.sprite.Sprite.__init__(self)
		self.x = 0
		self.y = 0
		self.change_x = 0
		self.change_y = 0
		self.image = image
		self.rect = rect

	def update(self):
		# Move the ball's center
		self.x += self.change_x
		self.y += self.change_y
		self.rect.move_ip(self.change_x, self.change_y)

		# Bounce the self if needed
		ball_dist = ((self.y - radius) ** 2 + (self.x - radius) ** 2) ** .5
		if ball_dist > radius:
			if abs(self.x - radius) < abs(self.y - radius):
				self.change_y *= -1
				self.y += self.change_y
			else:
				self.change_x *= -1
				self.x += self.change_x


def make_ball(image, stationary, centered):
	"""
	Function to make a new, random ball.
	"""
	ball = Ball(image, image.get_rect())
	# Starting position of the ball.
	# Take into account the ball size so we don't spawn on the edge.
	if centered:
		ball.x = radius
		ball.y = radius
	else:
		ball.x = random.randrange(100, 2*radius - 100)
		ball.y = random.randrange(100, 2*radius - 100)
	ball.rect.move_ip(ball.x, ball.y)

	# Speed and direction of rectangle
	ball.change_x = 0 if stationary else [-1.2,-1,-.7,-.5,.5,.7,1,1.2][random.randint(0,7)]
	ball.change_y = 0 if stationary else [-1.2,-1,-.7,-.5,.5,.7,1,1.2][random.randint(0,7)]

	return ball


def radar_init(screen, option):
	global radius
	global ball_list
	global ball_group
	radius = screen.get_width()//2-25

	ball_group = pygame.sprite.RenderPlain()

	# load images for given test
	images = []
	if option == 3:
		main = pygame.image.load("images/Treatment 3/main.png")
		images.append(pygame.image.load("images/Treatment 3/SAM1.png"))
		images.append(pygame.image.load("images/Treatment 3/enemy.png"))
		images.append(pygame.image.load("images/Treatment 3/no radar.png"))
		images.append(pygame.image.load("images/Treatment 3/wingman.png"))

	elif option == 2:
		main = pygame.image.load("images/Treatment 2/main.png")
		images.append(pygame.image.load("images/Treatment 2/SAM1.png"))
		images.append(pygame.image.load("images/Treatment 2/enemy.png"))
		images.append(pygame.image.load("images/Treatment 2/no radar.png"))
		images.append(pygame.image.load("images/Treatment 2/wingman.png"))
	else:
		main = pygame.image.load("images/Treatment 1/main.png")
		images.append(pygame.image.load("images/Treatment 1/SAM1.png"))
		images.append(pygame.image.load("images/Treatment 1/enemy.png"))
		images.append(pygame.image.load("images/Treatment 1/no radar.png"))
		images.append(pygame.image.load("images/Treatment 1/wingman.png"))


	for ind in range(random.randint(0,5)+2):
		blip = random.randint(0,3)
		ball = make_ball(images[blip], True if blip == 0 else False, False)
		ball.add(ball_group)
	make_ball(main, True, True).add(ball_group)

	# -------- Main Program Loop -----------
def update_radar(screen, radar_back):
	# --- Logic
	ball_group.update()

	screen.blit(radar_back, (0, 0))
	# Draw the balls
	ball_group.draw(screen)

	# Go ahead and update the screen with what we've drawn.
	pygame.display.flip()
