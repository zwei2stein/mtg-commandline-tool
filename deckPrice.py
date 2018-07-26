from decimal import *

import util

def deckPrice(deckCards, currency):

	totalPrice = Decimal(0)

	for deckCardName in deckCards:
		deckCard = deckCards[deckCardName]
		totalPrice += Decimal(deckCard.jsonData.get(currency, "0.0"))

	print ('Total price:', str(totalPrice), util.currencyToGlyph(currency))