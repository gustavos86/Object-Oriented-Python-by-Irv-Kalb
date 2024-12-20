# Balloon base clasas and 3 subclasses

import pygame
import random
from pygame.locals import *
import pygwidgets
from BalloonConstants import *
from abc import ABC, abstractmethod

class Balloon(ABC):
    popSoundLoaded = False
    popSound = None  # load when first balloon is created

    @abstractmethod
    def __init__(self, window, maxWidth, maxHeight, ID, oImage, size, nPoints, speedY):
        self.window = window
        self.ID = ID
        self.balloonImage = oImage
        self.size = size
        self.nPoints = nPoints
        self.speedY = speedY
        
        if not Balloon.popSoundLoaded:  # load first time only
            Balloon.popSound = pygame.mixer.Sound("sounds/balloonPop.wav")
            Balloon.popSoundLoaded = True
        
        balloonRect = self.balloonImage.getRect()
        self.width = balloonRect.width
        self.height = balloonRect.height
        # Position so baloon is within the width of the window
        # but below the bottom
        self.x = random.randrange(maxWidth - self.width)
        self.y = maxHeight + random.randrange(75)  # start below the window
        self.balloonImage.setLoc((self.x, self.y))

    def clickInside(self, mousePoint):
        myRect = pygame.Rect(self.x, self.y, self.width, self.height)
        if myRect.collidepoint(mousePoint):
            Balloon.popSound.play()
            return True, self.nPoints  # True here means it was hit
        else:
            return False, 0  # no hit, no points
        
    def update(self):
        self.y -= self.speedY  # update y position by speed
        self.balloonImage.setLoc((self.x, self.y))
        if self.y < -self.height:
            return BALLOON_MISSED  # balloon is off the top of the window
        else:
            return BALLOON_MOVING  # balloon is still moving
        
    def draw(self):
        self.balloonImage.draw()

    def __del__(self):
        print(f"{self.size} Balloon {self.ID} is going away")

class BalloonSmall(Balloon):
    balloonImage = pygame.image.load("images/redBalloonSmall.png")
    def __init__(self, window, maxWidth, maxHeight, ID):
        oImage = pygwidgets.Image(window, (0, 0), BalloonSmall.balloonImage)
        super().__init__(window, maxWidth, maxHeight, ID, oImage, 'Small', 30, 3.1)

class BalloonMedium(Balloon):
    balloonImage = pygame.image.load("images/redBalloonMedium.png")
    def __init__(self, window, maxWidth, maxHeight, ID):
        oImage = pygwidgets.Image(window, (0, 0), BalloonMedium.balloonImage)
        super().__init__(window, maxWidth, maxHeight, ID, oImage, 'Medium', 20, 2.2)

class BalloonLarge(Balloon):
    balloonImage = pygame.image.load("images/redBalloonLarge.png")
    def __init__(self, window, maxWidth, maxHeight, ID):
        oImage = pygwidgets.Image(window, (0, 0), BalloonLarge.balloonImage)
        super().__init__(window, maxWidth, maxHeight, ID, oImage, 'Large', 10, 1.5)

class MegaBalloon(Balloon):
    balloonImage3 = pygame.image.load("images/megaBalloon3.png")
    balloonImage2 = pygame.image.load("images/megaBalloon2.png")
    balloonImage1 = pygame.image.load("images/megaBalloon1.png")
    balloonImage0 = pygame.image.load("images/megaBalloon.png")

    def __init__(self, window, maxWidth, maxHeight, ID):
        self.balloonImageList = [pygwidgets.Image(window, (0, 0), MegaBalloon.balloonImage3),
                                 pygwidgets.Image(window, (0, 0), MegaBalloon.balloonImage2),
                                 pygwidgets.Image(window, (0, 0), MegaBalloon.balloonImage1),
                                 pygwidgets.Image(window, (0, 0), MegaBalloon.balloonImage0)]
        
        currentImage = self.balloonImageList.pop(0)
        super().__init__(window, maxWidth, maxHeight, ID, currentImage, 'Mega', 30, 7.0)

    def clickInside(self, mousePoint):
        myRect = pygame.Rect(self.x, self.y, self.width, self.height)
        if myRect.collidepoint(mousePoint):  # we hit the balloon
            
            if not len(self.balloonImageList):  # no more images to load means we can pop the balloon
                Balloon.popSound.play()
                return True, self.nPoints  # True here means popped and points
            else:
                # the baloon will not pop yet, we load the next image
                currentImage = self.balloonImageList.pop(0)
                self.balloonImage = currentImage

        return False, 0  # no hit or not yet popped, no points
