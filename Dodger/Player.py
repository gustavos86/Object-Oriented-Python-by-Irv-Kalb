# Player class
import pygwidgets
from Constants import *
import time
from pygame.mixer import Sound as PygameSound

class Player():
    PLAYABLE_STATE = "playable state"
    HIT_STATE = "hit state"

    HIT_STATE_DURATION = 2.5  # in seconds
    FRAMES_TO_BLINK_INTERVAL = 3  # Number of frames

    def __init__(self, window):
        self.window = window
        self.image = pygwidgets.Image(window,
                                      (-100, -100),
                                      "images/player.png")

        playerRect = self.image.getRect()
        self.maxX = WINDOW_WIDTH - playerRect.width
        self.maxY = GAME_HEIGHT  - playerRect.height

        # Sound to play when player is hit
        self.playerHitSound = None

        # State of the Player
        self.state = Player.PLAYABLE_STATE
        self.hitStartTime = 0.0
        self.nFramesElapsed = 0
        self.displayPlayer = True
        self.resetLives()  # reset lives to default

    def normalizeLocationOnDisplay(self, x, y):
        if x < 0:
            x = 0
        elif x > self.maxX:
            x = self.maxX
        elif y < 0:
            y = 0
        elif y > self.maxY:
            y = self.maxY

        return x, y

    # Every frame, move the Player icon to the mouse position
    # Limits the x- and y-coordinates to the game area of the window
    def update(self, x, y):
        # temporary invinsible due to Player was hit by a Baddie
        if self.state == Player.HIT_STATE:
            elapseTime = time.time() - self.hitStartTime
            if elapseTime >= Player.HIT_STATE_DURATION:
                self.state = Player.PLAYABLE_STATE

        # normalize location on display
        playerX, playerY = self.normalizeLocationOnDisplay(x, y)

        self.image.setLoc((playerX, playerY))
        return self.image.getRect()
    
    def draw(self):
        if self.state == Player.HIT_STATE:  # Toggle display player every N frames
            self.nFramesElapsed += 1
            if self.nFramesElapsed == Player.FRAMES_TO_BLINK_INTERVAL:
                self.displayPlayer = not self.displayPlayer
                self.nFramesElapsed = 0

            if self.displayPlayer:
                self.image.draw()

        elif self.state == Player.PLAYABLE_STATE:
            self.image.draw()

    def resetLives(self):
        self.lives = N_LIVES

    def setHitSound(self, hitSound):
        assert type(hitSound) == PygameSound
        self.playerHitSound = hitSound

    def hasPlayerlost(self):
        if self.lives < 0:
            return True
        else:
            return False

    def gotHit(self):
        """
        Player got hit

        1. Rest lives by one
        2. Play the Sound (if it was loaded)
        Optionally. Return if no more lives
        3. Set to the temporary invisible state
        4. Set a timer
        """
        if self.state == Player.PLAYABLE_STATE:
            self.lives -= 1

            if self.playerHitSound is not None:
                self.playerHitSound.play()

            if self.hasPlayerlost():  # Don't blink after having lost
                return

            self.state = Player.HIT_STATE
            self.hitStartTime = time.time()

    def getLives(self):
        if self.lives < 0:
            return 0

        return self.lives