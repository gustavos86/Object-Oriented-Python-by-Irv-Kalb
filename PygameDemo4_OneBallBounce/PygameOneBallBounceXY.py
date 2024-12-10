# pygame demo 4(a) - one image, bounce around the window using (x, y) coords

# 1 - import packagegs
import pygame
from pygame.locals import *
import sys
import random

# 2 - Define constants
BLACK = (0, 0, 0)
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
FRAMES_PER_SECOND = 30
BALL_WIDTH_HEIGHT = 100
N_PIXELS_TO_MOVE = 3

# 3 - initialize the world
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

# 4 - Load assets: image(s), sounds, etc.
ballImage = pygame.image.load("images/ball.png")

# 5 - Initialize variables
MAX_WIDTH = WINDOW_WIDTH - BALL_WIDTH_HEIGHT
MAX_HEIGHT = WINDOW_HEIGHT - BALL_WIDTH_HEIGHT

ballX = random.randrange(MAX_WIDTH)
ballY = random.randrange(MAX_HEIGHT)

xSpeed = N_PIXELS_TO_MOVE
ySpeed = N_PIXELS_TO_MOVE


# 6 - Loop forever
while True:

    # 7 - Check for and handle events
    for event in pygame.event.get():
        # Clicked the close button? Quit pygame and end the program
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 8 - Do any "per frame" actions
    if (ballX < 0) or (ballX >= MAX_WIDTH):
        xSpeed = -xSpeed  # reverse X direction
    if (ballY < 0) or (ballY >= MAX_HEIGHT):
        ySpeed = -ySpeed  # reverse Y direction

    # Update the ball's location, using the speed in two directions
    ballX = ballX + xSpeed
    ballY = ballY + ySpeed
    
    # 9 - Clear the window before drawing it again
    window.fill(BLACK)

    # 10 - Draw all window elements
    window.blit(ballImage, (ballX, ballY))  # draw the ball

    # 11- Update hte window
    pygame.display.update()

    # 12 - Slow things down a bit
    clock.tick(FRAMES_PER_SECOND)  # make pygame wait