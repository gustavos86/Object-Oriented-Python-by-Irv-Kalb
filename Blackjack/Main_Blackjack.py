# Higher or Lower - pygame version
# Main program

# 1 - Import packages
import pygwidgets
import pygame
from pygame.locals import *
from Constants import *
from Game import *
import sys

# 2 - Define constants

# 3 - Initialize the world
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

# 4 - Load assets: image(s), sounds, etc.
background    = pygwidgets.Image(window, (0, 0), "images/blackjack_background.png")
newGameButton = pygwidgets.TextButton(window, (20, 530), "New Game", width=100, height=45)
hitButton     = pygwidgets.TextButton(window, (340, 520), "Hit", width=120, height=55)
standButton   = pygwidgets.TextButton(window, (540, 520), "Stand", width=120, height=55)
quitButton    = pygwidgets.TextButton(window, (880, 530), "Quit", width=100, height=45)

# 5 - Initialize variables
oGame = Game(window)

# 6 - Loop forever
while True:
    # 7 - Check for and handle events
    for event in pygame.event.get():
        # check if the event is the user clicking the close box
        if (event.type == pygame.QUIT) or (event.type == KEYDOWN and event.key == K_ESCAPE) or (quitButton.handleEvent(event)):
            pygame.quit()
            sys.exit()

        if newGameButton.handleEvent(event):
            oGame.reset()
            hitButton.enable()
            standButton.enable()

        if hitButton.handleEvent(event):
            gameOver = oGame.hitButtonAction()
            if gameOver:
                hitButton.disable()
                standButton.disable()

        if standButton.handleEvent(event):
            oGame.standButtonAction()  # game is over
            hitButton.disable()
            standButton.disable()

    # 8 - Do any "per frame" actions

    # 9 - Clear the window
    background.draw()

    # 10 - Draw all window elements
    # Tell the game to draw itself
    oGame.draw()
    # Draw remaining user interface components
    newGameButton.draw()
    hitButton.draw()
    standButton.draw()
    quitButton.draw()

    # 11 - Update the window
    pygame.display.update()

    # 12 - Slow things down a bit
    clock.tick(FRAMES_PER_SECOND)  # make pygame wait