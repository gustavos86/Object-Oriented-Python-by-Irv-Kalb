# pygame demo 7 - SimpleButton test

# 1 - Import packages
import pygame
from pygame.locals import *
import sys
from SimpleButton import *

# 2 - Define constants
BLACK = (0, 0, 0)
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
FRAMES_PER_SECOND = 30

# 3 - Initialize the world
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
clock = pygame.time.Clock()

# 4 - Load assets; image(s), sound(s), etc.

# 5 - Initialize variables
# Create an instance of a SimpleButton
oButtonA = SimpleButton(window, (25, 30),
                             "images/buttonAUp.png",
                             "images/buttonADown.png")
oButtonB = SimpleButton(window, (150, 30),
                             "images/buttonBUp.png",
                             "images/buttonBDown.png")
oButtonC = SimpleButton(window, (275, 30),
                             "images/buttonCUp.png",
                             "images/buttonCDown.png")

# 6 - Loop forever
while True:

    # 7 - Check for and handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Pass the event to the button, see if it has been clicked on
        if oButtonA.handleEvent(event):
            print("User has clicked the button A.")
        elif oButtonB.handleEvent(event):
            print("User has clicked the button B.")
        elif oButtonC.handleEvent(event):
            print("User has clicked the button C.")
    # 8 - Do any "per frame" actions

    # 9 - Clear the window before drawing it again
    window.fill(BLACK)

    # 10 - Draw all window elements
    oButtonA.draw()
    oButtonB.draw()
    oButtonC.draw()

    # 11 - Update the window
    pygame.display.update()

    # 12 - Slow things down a bit
    clock.tick(FRAMES_PER_SECOND)  # make pygame wait