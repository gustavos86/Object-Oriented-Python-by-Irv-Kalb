#  Dodger main program
#
# Instantiates 3 scenes, creates and starts the scene manager
#
#  Original version by Al Sweigart from his book "Invent With Python"
#    (concept, graphics, and sounds used by permission from Al Sweigart)

# 1 - Import packages
import pygame
import pyghelpers

from SceneSplash import *
from SceneHighScores import *
from ScenePlay import *

from Constants import *

# 2 - Define constants

# 3 - Initialize the world
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

# 4 - Load assets: image(s), sounds,  etc.

# 5 - Initialize variables
# Instantiate all scenes and store them in a list
sceneList = [SceneSplash(window),
             SceneHighScores(window),
             ScenePlay(window),
            ]

# Create the scene manager, passing in the scenes list and the FPS
oSceneMgr = pyghelpers.SceneMgr(sceneList, FRAMES_PER_SECOND)

# Tell the scene manager to start running
oSceneMgr.run()