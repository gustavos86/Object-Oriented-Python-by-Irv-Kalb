from Game import *
from Card import *

pygame.init()
window = pygame.display.set_mode((0, 0))

def prueba1():
    hand = Hand(0, 0)

    card1 = Card(window, "Ace", "Diamonds", 11)
    hand.cardsList = [card1]

    assert hand.getHandScore() == 11

def prueba2():
    hand = Hand(0, 0)

    card1 = Card(window, "Ace", "Diamonds", 11)
    card2 = Card(window, "Ace", "Club", 11)
    hand.cardsList = [card1, card2]

    assert hand.getHandScore() == 12

def prueba2():
    hand = Hand(0, 0)

    card1 = Card(window, "Ace", "Diamonds", 11)
    card2 = Card(window, "Ace", "Club", 11)
    hand.cardsList = [card1, card2]

    assert hand.getHandScore() == 12

def prueba3():
    hand = Hand(0, 0)

    card1 = Card(window, "Ace", "Diamonds", 11)
    card2 = Card(window, "Ace", "Club", 11)
    card3 = Card(window, "Ace", "Hearts", 11)
    hand.cardsList = [card1, card2, card3]

    assert hand.getHandScore() == 13

def prueba4():
    hand = Hand(0, 0)

    card1 = Card(window, "Ace", "Diamonds", 11)
    card2 = Card(window, "Ace", "Club", 11)
    card3 = Card(window, "Ace", "Hearts", 11)
    card4 = Card(window, "Ace", "Spades", 11)
    hand.cardsList = [card1, card2, card3, card4]

    assert hand.getHandScore() == 14

def prueba5():
    hand = Hand(0, 0)

    card1 = Card(window, "Ace", "Diamonds", 11)
    card2 = Card(window, "6", "Club", 6)
    card3 = Card(window, "Ace", "Hearts", 11)
    hand.cardsList = [card1, card2, card3]

    assert hand.getHandScore() == 18

prueba1()
prueba2()
prueba3()
prueba4()
prueba5()
print("Todas las pruebas fueron exitosas")