# Game class

import pygwidgets
from Constants import *
from Deck import *
from Card import *
import pygame

class Hand():
    CARD_OFFSET = 80

    def __init__(self, window, x, y):
        self.window = window
        self.cardsList = []

        self.x = x  # CARDS_LEFT = 75
        self.y = y  # CARDS_TOP = 350

    def drawCard(self, oDeck, reveal=True):
        oCard = oDeck.getCard()         # draw a new card from the Deck

        oCard.setLoc((self.x, self.y))  # set the location for the new card
        self.x += Hand.CARD_OFFSET      # increment the display offset for the next card
        
        if reveal:
            oCard.reveal()              # face up the card

        self.cardsList.append(oCard)    # append it to cards to be displayed

    def getHandScore(self):
        """
        If the total does not exceed 21 points, then the Ace is worth 11 points.
        However, if holding an Ace causes you to exceed 21 points in total, its value is reduced to 1 point.
        """
        aceFound = False
        score = 0

        for card in self.cardsList:
            if card.getRank() == "Ace":
                aceFound = True
            score += card.getValue()

        if aceFound and score > Game.BLACKJACK:
            score -= 10

        return score

    def draw(self):
        for card in self.cardsList:
            card.draw()

    def revealCard(self, index=-1):
        """
        Face up last card by default
        """
        if not len(self.cardsList):
            raise IndexError("No Cards in the Hand")
        
        self.cardsList[index].reveal()

class Game():
    CARDS_LEFT = 75
    CARDS_TOP  = 350

    BLACKJACK = 21

    def __init__(self, window):
        self.window = window
        black_jack_card_values = {"Ace":11, "2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8, "9":9, "10":10, "Jack":10, "Queen":10, "King":10}
        self.oDeck = Deck(self.window, rankValueDict=black_jack_card_values)

        self.messageText = pygwidgets.DisplayText(self.window, (80, 80), "", width=900, justified="center", fontSize=50, textColor=WHITE)

        self.playerHandScoreText = pygwidgets.DisplayText(self.window, (450, Game.CARDS_TOP-40), f"Hand Score: 0", fontSize=36, textColor=WHITE, justified="right")

        self.playerGamesWon = 0
        self.playerGamesWonText = pygwidgets.DisplayText(self.window, (Game.CARDS_LEFT+20, Game.CARDS_TOP-40), f"Player Wins: {self.playerGamesWon}", fontSize=36, textColor=WHITE, justified="right")

        self.dealerGamesWon = 0
        self.dealerGamesWonText = pygwidgets.DisplayText(self.window, (Game.CARDS_LEFT+20, Game.CARDS_TOP-240), f"Dealer Wins: {self.dealerGamesWon}", fontSize=36, textColor=WHITE, justified="right")

        self.loserSound = pygame.mixer.Sound("sounds/loser.wav")
        self.winnerSound = pygame.mixer.Sound("sounds/ding.wav")
        self.cardShuffleSound = pygame.mixer.Sound("sounds/cardShuffle.wav")

        self.reset()  # start a round of the game

    def reset(self):  # this method is called when a new round starts
        self.cardShuffleSound.play()
        self.oDeck.shuffle()

        self.messageText.setValue("")

        # New hands for player and dealer
        self.playerHand = Hand(self.window, Game.CARDS_LEFT, Game.CARDS_TOP)
        self.dealerHand = Hand(self.window, Game.CARDS_LEFT, Game.CARDS_TOP-200)
        
        # Get the dealer's Cards
        self.dealerHand.drawCard(self.oDeck, reveal=False)
        self.dealerHand.drawCard(self.oDeck)

        # Update the displayed Dealer Hand Score
        dealerHandScore = self.dealerHand.getHandScore()
        print(f"Dealer Hand Score: {dealerHandScore}")

        # Get initial two cards for the player
        self.playerHand.drawCard(self.oDeck)
        self.playerHand.drawCard(self.oDeck)

        # Update the displayed Player Hand Score
        playerHandScore = self.playerHand.getHandScore()  # update player hand score
        self.playerHandScoreText.setValue(f"Hand Score: {playerHandScore}") 

    def hitButtonAction(self):
        """
        1. Draw card for player
        2. Update the displayed Player Hand Score on the screen
        3. Check if the Game has ended
        """
        self.playerHand.drawCard(self.oDeck)              # draw a new card from the Deck

        playerHandScore = self.playerHand.getHandScore()  # update player hand score
        self.playerHandScoreText.setValue(f"Hand Score: {playerHandScore}") 

        return self.checkGameHasEnded(playerHandScore=self.playerHand.getHandScore(),
                                      dealerHandScore=self.dealerHand.getHandScore())

    def standButtonAction(self):
        """
        1. Face up first Dealer Card
        2. Draw additional cards for the dealer
        3. Update the displayed Dealer Hand Score on the console
        4. Check for Game Result
        """
        self.dealerHand.revealCard(0)

        while self.dealerHand.getHandScore() <= 17:
            self.dealerHand.drawCard(self.oDeck)

        dealerHandScore = self.dealerHand.getHandScore()
        print(f"Dealer Hand Score final: {dealerHandScore}")

        return self.checkGameHasEnded(playerHandScore=self.playerHand.getHandScore(),
                                       dealerHandScore=self.dealerHand.getHandScore(),
                                       standAction=True)  # check result

    def checkGameHasEnded(self, playerHandScore, dealerHandScore, standAction=False):
        playerWon  = False
        playerLost = False
        gameOver   = False

        if playerHandScore > Game.BLACKJACK:  # player points more than 21 ponts. Player lost
            self.dealerHand.revealCard(0)     # face up the first dealer card
            playerLost = True

        elif standAction and\
            dealerHandScore > Game.BLACKJACK:  # dealer points more than 21 ponts. Player won
            playerWon = True

        elif standAction and\
            (playerHandScore > dealerHandScore):  # player points more than dealer points. Player won
            playerWon = True

        elif standAction:  # player points equal or lower than dealer points. Player lost
            playerLost = True

        if playerWon:
            self.playerGamesWon += 1
            self.playerGamesWonText.setValue(f"Player Wins: {self.playerGamesWon}")
            self.messageText.setValue("You win!")
            self.winnerSound.play()
            gameOver = True
        elif playerLost:
            self.dealerGamesWon += 1
            self.dealerGamesWonText.setValue(f"Dealer Wins: {self.dealerGamesWon}")
            self.messageText.setValue("You lost")
            self.loserSound.play()
            gameOver = True

        if standAction:
            gameOver = True

        return gameOver

    def draw(self):
        self.playerHand.draw()
        self.dealerHand.draw()

        self.playerGamesWonText.draw()
        self.dealerGamesWonText.draw()
        self.playerHandScoreText.draw()
        self.messageText.draw()
