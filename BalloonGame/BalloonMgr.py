# BalloonMgr class

import pygame
import random
from pygame.locals import *
import pygwidgets
from BalloonConstants import *
from Balloon import *

# BaloonMgr manages a list of Balloon objects
class BalloonMgr():
    def __init__(self, window, maxWidth, maxHeight):
        self.window = window
        self.maxWidth = maxWidth
        self.maxHeight = maxHeight
        self.numberOfInitialBalloons = 0

    def start(self):
        self.balloonList = []
        self.nPopped = 0
        self.nMissed = 0
        self.score = 0

        for balloonNum in range(0, N_BALLONS):
            randomBalloonClass = random.choice((BalloonSmall, BalloonMedium, BalloonLarge))
            oBalloon = randomBalloonClass(self.window, self.maxWidth, self.maxHeight, balloonNum)
            self.balloonList.append(oBalloon)
        self.balloonList.append(MegaBalloon(self.window, self.maxWidth, self.maxHeight, N_BALLONS))  # adding one MegaBallook
        self.numberOfInitialBalloons = len(self.balloonList)

    def handleEvent(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Go 'reversed' so topmost balloon gets popped
            for oBalloon in reversed(self.balloonList):
                wasHit, nPoints = oBalloon.clickInside(event.pos)

                if wasHit and nPoints > 0:
                    self.balloonList.remove(oBalloon)  # remove this balloon
                    self.nPopped += 1
                    self.score += nPoints
                    return  # no need to check others

    def update(self):
        for oBalloon in self.balloonList:
            status = oBalloon.update()
            if status == BALLOON_MISSED:
                # Balloon went off the top, remove it
                self.balloonList.remove(oBalloon)
                self.nMissed += 1

    def getScore(self):
        return self.score
    
    def getCountPopped(self):
        return self.nPopped
    
    def getCountMissed(self):
        return self.nMissed
    
    def getCountBalloonsInMotion(self):
        return len(self.balloonList)
    
    def getNumberOfInitialBalloons(self):
        return self.numberOfInitialBalloons

    def draw(self):
        for oBalloon in self.balloonList:
            oBalloon.draw()
