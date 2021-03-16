from collections import deque
from random import shuffle

import cardListFormater


def drawCards(deck, count):
    shuffledDeck = deque()

    for card in deck:
        cardInDeck = deck[card]
        if (not cardInDeck.commander):
            for x in range(0, cardInDeck.count - cardInDeck.sideboard):
                shuffledDeck.append(cardInDeck.name)

    shuffle(shuffledDeck)

    drawnCards = []

    for x in range(0, count):
        if (len(shuffledDeck) > 0):
            drawnCards.append(shuffledDeck.popleft())
        else:
            print('Decked :(')
            break

    return drawnCards;


def printDrawCardsToConsole(drawnCards, context):
    print(str(len(drawnCards)) + ' cards drawn.')
    print('')

    cardListFormater.printCardObjectList(cardListFormater.cardListToCardObjectMap(drawnCards, context, 1), context)
