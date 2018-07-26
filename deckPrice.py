from decimal import *

import util

def deckPrice(deckCards, currency):

	totalPrice = Decimal(0)
	sideboardPrice = Decimal(0)

	for deckCardName in deckCards:
		deckCard = deckCards[deckCardName]
		totalPrice += Decimal(deckCard.jsonData.get(currency, "0.0"))
		if (deckCard.sideboard):
			sideboardPrice += Decimal(deckCard.jsonData.get(currency, "0.0"))

	print ('Deck price:', str(totalPrice - sideboardPrice), util.currencyToGlyph(currency))
	print ('Sideboard price:', str(sideboardPrice), util.currencyToGlyph(currency))
	print ('Total price:', str(totalPrice), util.currencyToGlyph(currency))