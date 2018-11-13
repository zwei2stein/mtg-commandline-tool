from collections import deque
from random import shuffle


def drawCards(deck, count, scry=False):
	shuffledDeck = deque()

	for card in deck:
	   	cardInDeck = deck[card]
	   	for x in range(0, cardInDeck.count):
	   	  	shuffledDeck.append(cardInDeck.name)

	shuffle(shuffledDeck)

	drawCardsShuffledDeck(shuffledDeck, count, scry)

def drawCardsShuffledDeck(shuffledDeck, count, scry):

	print("Drawn (" + str(count) + ")")

	for x in range(0, count):
		if (len(shuffledDeck) > 0):
			print ('\t', shuffledDeck.popleft())
		else:
			print ('Decked')
			break

	if (scry):
		if (len(shuffledDeck) > 0):
			print("Scry:")
			print ('\t', shuffledDeck.popleft())