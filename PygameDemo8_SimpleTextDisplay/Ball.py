import pygame
from pygame.locals import *
import random

from pygame.surface import Surface

# Ball class
class Ball():
    def __init__(self, window: Surface):
        self.window = window  # remember the window, so we can draw later

        self.image = pygame.image.load('images/ball.png')
        # A rect is made up of (x, y, width, height)
        ballRect = self.image.get_rect()

        self.maxWidth  = self.window.get_width()  - ballRect.width
        self.maxHeight = self.window.get_height() - ballRect.height

        # Pick a random starting position
        self.x = random.randrange(0, self.maxWidth)
        self.y = random.randrange(0, self.maxHeight)

        # Choose a random speed between -4 and 4, but not zero,
        # in both the x and y directions
        speedsList = [-4, -3, -2, -1, 1, 2, 3, 4]
        self.xSpeed = random.choice(speedsList)
        self.ySpeed = random.choice(speedsList)

    def update(self):
        # Check for hitting a wall. If so, change that direction
        if (self.x < 0) or (self.x >= self.maxWidth):
            self.xSpeed = -self.xSpeed
        if (self.y < 0) or (self.y >= self.maxHeight):
            self.ySpeed = -self.ySpeed

        # Update the Ball's x and y, using the speed in two directions
        self.x += self.xSpeed
        self.y += self.ySpeed
    
    def draw(self):
        self.window.blit(self.image, (self.x, self.y))