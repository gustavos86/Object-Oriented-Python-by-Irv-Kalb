#  Play scene - the main game play scene

import pygame
import pygwidgets
import pyghelpers
from Constants import *

from Player import *
from Goodies import *
from Baddies import *

def showCustomYesNoDialog(theWindow, theText):
    oDialogBackground = pygwidgets.Image(theWindow, (40, 250),
                                            'images/dialog.png')
    oPromptDisplayText = pygwidgets.DisplayText(theWindow, (0, 290),
                                            theText, width=WINDOW_WIDTH,
                                            justified='center', fontSize=36)

    oYesButton = pygwidgets.CustomButton(theWindow, (320, 370),
                                            'images/gotoHighScoresNormal.png',
                                            over='images/gotoHighScoresOver.png',
                                            down='images/gotoHighScoresDown.png',
                                            disabled='images/gotoHighScoresDisabled.png')

    oNoButton = pygwidgets.CustomButton(theWindow, (62, 370),
                                            'images/noThanksNormal.png',
                                            over='images/noThanksOver.png',
                                            down='images/noThanksDown.png',
                                            disabled='images/noThanksDisabled.png')

    choiceAsBoolean = pyghelpers.customYesNoDialog(theWindow,
                                            oDialogBackground, oPromptDisplayText,
                                            oYesButton, oNoButton)
    return choiceAsBoolean

BOTTOM_RECT = (0,
               GAME_HEIGHT + 1,
               WINDOW_WIDTH,
               WINDOW_HEIGHT - GAME_HEIGHT)
STATE_WAITING = "waiting"
STATE_PLAYING = "playing"
STATE_GAME_OVER = "game over"

class ScenePlay(pyghelpers.Scene):
    def __init__(self, window):
        self.window = window
        self.controlsBackground = pygwidgets.Image(self.window,
                                                   (0, GAME_HEIGHT),
                                                   "images/controlsBackground.jpg")
        self.quitButton = pygwidgets.CustomButton(self.window,
                                                  (30, GAME_HEIGHT + 90),
                                                  up="images/quitNormal.png",
                                                  down="images/quitDown.png",
                                                  over="images/quitOver.png",
                                                  disabled="images/quitDisabled.png")
        self.highScoresButton = pygwidgets.CustomButton(self.window,
                                                       (190, GAME_HEIGHT + 90),
                                                       up="images/gotoHighScoresNormal.png",
                                                       down="images/gotoHighScoresDown.png",
                                                       over="images/gotoHighScoresOver.png",
                                                       disabled="images/gotoHighScoresDisabled.png")
        self.startButton = pygwidgets.CustomButton(self.window,
                                                  (450, GAME_HEIGHT + 90),
                                                  up="images/startNormal.png",
                                                  down="images/startDown.png",
                                                  over="images/startOver.png",
                                                  disabled="images/startDisabled.png",
                                                  enterToActivate=True)
        self.soundCheckBox = pygwidgets.TextCheckBox(self.window,
                                                     (430, GAME_HEIGHT + 17),
                                                     "Background music",
                                                     True,
                                                     textColor=WHITE)
        self.gameOverImage = pygwidgets.Image(self.window,
                                              (140, 180),
                                              "images/gameOver.png")
        self.titleText = pygwidgets.DisplayText(self.window,
                                                (70, GAME_HEIGHT + 17),
                                                "Lives:       Bombs:       Score:       High Score:",
                                                fontSize=24,
                                                textColor=WHITE)
        self.livesText = pygwidgets.DisplayText(self.window,
                                                 (80, GAME_HEIGHT + 47),
                                                 "0",
                                                 fontSize=36,
                                                 textColor=WHITE,
                                                 justified="right")
        self.bombsText = pygwidgets.DisplayText(self.window,
                                                 (160, GAME_HEIGHT + 47),
                                                 "0",
                                                 fontSize=36,
                                                 textColor=WHITE,
                                                 justified="right")
        self.scoreText = pygwidgets.DisplayText(self.window,
                                                 (235, GAME_HEIGHT + 47),
                                                 "0",
                                                 fontSize=36,
                                                 textColor=WHITE,
                                                 justified="right")
        self.highScoreText = pygwidgets.DisplayText(self.window,
                                                    (310, GAME_HEIGHT + 47),
                                                    "",
                                                    fontSize=36,
                                                    textColor=WHITE,
                                                    justified="right")
        
        pygame.mixer.music.load("sounds/background.mid")
        pygame.mixer.music.set_volume(0.2)
        self.dingSound = pygame.mixer.Sound("sounds/ding.wav")
        self.gameOverSound = pygame.mixer.Sound("sounds/gameOver.wav")
        self.explosionSound = pygame.mixer.Sound("sounds/explosion.wav")
        self.explosionSound.set_volume(1.0)

        self.oPlayer = Player(self.window)
        self.oPlayer.hitSound = pygame.mixer.Sound("sounds/buzz.wav")
        self.oPlayer.noBombsSound = pygame.mixer.Sound("sounds/no_bombs.wav")
        self.oPlayer.noBombsSound.set_volume(0.2)

        self.oBaddieMgr = BaddieMgr(self.window)
        self.oGoodieMgr = GoodieMgr(self.window)

        self.highestHighScore = 0
        self.lowestHighScore = 0

        self.backgroundMusic = True
        self.score = 0
        self.playingState = STATE_WAITING
    
    def getSceneKey(self):
        return SCENE_PLAY

    def handleInputs(self, eventsList, keyPressedList):
        if self.playingState == STATE_PLAYING:
            # The player starts with a small number of bombs that
            # can be detonated when the player is in a bind,
            # eliminating all Baddies in close proximity around the Player icon.
            # The count of bombs is decremented each time one is used, until it reaches zero.
            for event in eventsList:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.oPlayer.bombs:
                            self.explosionSound.play()
                            mouseX, mouseY = pygame.mouse.get_pos()
                            playerX, playerY = self.oPlayer.normalizeLocationOnDisplay(mouseX, mouseY)
                            self.oBaddieMgr.destroyAllBaddiesWithinDetonationArea(playerX, playerY)
                            self.oPlayer.bombs -= 1
                            self.bombsText.setValue(self.oPlayer.bombs)
                        else:
                            self.oPlayer.noBombsSound.play()

        for event in eventsList:
            if self.startButton.handleEvent(event):
                self.reset()
                self.playingState = STATE_PLAYING

            if self.highScoresButton.handleEvent(event):
                self.goToScene(SCENE_HIGH_SCORES)

            if self.soundCheckBox.handleEvent(event):
                self.backgroundMusic = self.soundCheckBox.getValue()

            if self.quitButton.handleEvent(event):
                self.quit()

    def draw(self):
        self.window.fill(BLACK)

        # Tell the managers to draw all the Baddies and Goodies
        self.oBaddieMgr.draw()
        self.oGoodieMgr.draw()

        # Tell the Player to draw itself
        self.oPlayer.draw()

        # Draw all the info at the bottom of the window
        self.controlsBackground.draw()
        self.titleText.draw()
        self.livesText.draw()
        self.bombsText.draw()
        self.scoreText.draw()
        self.highScoreText.draw()
        self.soundCheckBox.draw()
        self.quitButton.draw()
        self.highScoresButton.draw()
        self.startButton.draw()

        if self.playingState == STATE_GAME_OVER:
            self.gameOverImage.draw()

    def enter(self, data):
        self.getHiAndLowScores()

    def leave(self):
        pygame.mixer.music.stop()

    def reset(self):  # start a new game
        self.score = 0
        self.scoreText.setValue(self.score)
        self.getHiAndLowScores()

        # Tell the managers to reset themselves
        self.oBaddieMgr.reset()
        self.oGoodieMgr.reset()
        self.oPlayer.resetLives()
        self.livesText.setValue(self.oPlayer.lives)
        self.bombsText.setValue(self.oPlayer.bombs)

        if self.backgroundMusic:
            pygame.mixer.music.play(-1, 0.0)
        
        self.startButton.disable()
        self.highScoresButton.disable()
        self.soundCheckBox.disable()
        self.quitButton.disable()

        pygame.mouse.set_visible(False)

    def getHiAndLowScores(self):
        """
        Ask the High Scores scene for a dict of scores
        that looks like this:

        {"highest": highestScore, "lowest": lowestScore}
        """
        infoDict = self.request(SCENE_HIGH_SCORES, HIGH_SCORES_DATA)

        self.highestHighScore = infoDict["highest"]
        self.highScoreText.setValue(self.highestHighScore)
        self.lowestHighScore = infoDict["lowest"]

    def update(self):
        if self.playingState != STATE_PLAYING:
            return  # only update when playing
        
        # Move the Player to the mouse position, get back its rect
        mouseX, mouseY = pygame.mouse.get_pos()
        playerRect = self.oPlayer.update(mouseX, mouseY)

        # Tell the GoodieMgr to move all Goodies
        # Returns the number of Goodies that the Player contacted
        nGoodiesHist = self.oGoodieMgr.update(playerRect)
        if nGoodiesHist > 0:
            self.dingSound.play()
            self.score += (nGoodiesHist * POINTS_FOR_GOODIE)

        # Tell the BaddieMgr to move all the Baddies
        # Returns the number of Baddies that fell off the bottom
        nBaddiesEvaded = self.oBaddieMgr.update()
        self.score += (nBaddiesEvaded * POINTS_FOR_BADDIE_EVADED)
        self.scoreText.setValue(self.score)

        # Check if the Player had hit the Baddie
        if self.oBaddieMgr.hasPlayerHitBaddie(playerRect):
            self.oPlayer.gotHit()  # player was hit by a Baddie
            self.livesText.setValue(self.oPlayer.lives)

        if self.oPlayer.hasPlayerlost():  # Player has lost
            pygame.mouse.set_visible(True)
            pygame.mixer.music.stop()

            self.gameOverSound.play()
            self.playingState = STATE_GAME_OVER
            self.draw()  # force drawing of game over message
        
            if self.score > self.lowestHighScore:
                scoreString = f"Your score: {self.score}\n"
                if self.score > self.highestHighScore:
                    dialogText = (f"{scoreString} is a new high score, CONGRATULATIONS!")
                else:
                    dialogText = (f"{scoreString} gets you on the high scores list.")
                
                result = showCustomYesNoDialog(self.window, dialogText)
                if result:  # navigate
                    self.goToScene(SCENE_HIGH_SCORES, self.score)
        
        self.startButton.enable()
        self.highScoresButton.enable()
        self.soundCheckBox.enable()
        self.quitButton.enable()
