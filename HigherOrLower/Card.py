# Card class

import pygame
import pygwidgets

class Card():
    BACK_OF_CARD_IMAGE = pygame.image.load("images/BackOfCard.png")

    def __init__(self, window, rank, suit, value):
        self.window = window
        self.rank = rank
        self.suit = suit
        self.cardName = f"{rank} of {suit}"
        self.value = value
        fileName = f"images/{self.cardName}.png"
        # Set some starting location; use setLoc below to change
        self.images = pygwidgets.ImageCollection(window, (0, 0), {'front': fileName, 'back': Card.BACK_OF_CARD_IMAGE}, 'back')

    def conceal(self):
        self.images.replace('back')
    
    def reveal(self):
        self.images.replace('front')

    def getName(self):
        return self.cardName
    
    def getValue(self):
        return self.value
    
    def getRank(self):
        return self.rank
    
    def setLoc(self, loc):  # call the setLoc method of the ImageCollection
        self.images.setLoc(loc)

    def getLoc(self):  # get the location from the ImageCollection
        return self.images.getLoc()
    
    def draw(self):
        self.images.draw()

if __name__ == "__main__":
    pygame.init()
    window = pygame.display.set_mode([400, 400])
    oCard = Card(window, 'Ace', 'Spades', 1)
    oCard.draw()
    pygame.display.update()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False