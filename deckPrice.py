from decimal import *
import console

import util

def deckPrice(deckCards, currency):

	totalPrice = Decimal(0)
	sideboardPrice = Decimal(0)

	for deckCardName in deckCards:
		deckCard = deckCards[deckCardName]
		totalPrice += ((deckCard.count - deckCard.sideboard) * Decimal(deckCard.jsonData.get(currency, "0.0")))
		sideboardPrice += (deckCard.sideboard * Decimal(deckCard.jsonData.get(currency, "0.0")))

	print ('Deck price:', str(totalPrice - sideboardPrice) + util.currencyToGlyph(currency))
	print ('Sideboard price:', str(sideboardPrice) + util.currencyToGlyph(currency))
	print ( console.CRED + 'Total price:' + console.CEND, str(totalPrice) + util.currencyToGlyph(currency))