import cardListFormater

from collections import deque
from random import shuffle

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
			print ('Decked :(')
			break

	return drawnCards;


def printManaSymbolsToConsole(drawnCards):

	print(str(len(drawnCards)) + ' cards drawn.')
	print('')

	cardListFormater.printCardObjectList(cardListFormater.cardListToCardObjectMap(drawnCards, 1))