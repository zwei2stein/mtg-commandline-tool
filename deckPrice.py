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

	response = {}

	response["currency"] = currency

	response["deckPrice"] = totalPrice - sideboardPrice
	response["sideboardPrice"] = sideboardPrice;
	response["totalPrice"] = totalPrice;

	return response

def printPricesToConsole(response):

	print ('Deck price:', str(response["deckPrice"]), util.currencyToGlyph(response["currency"]) )
	print ('Sideboard price:', str(response["sideboardPrice"]), util.currencyToGlyph(response["currency"]))
	print ( console.CRED + 'Total price:' + console.CEND, str(response["totalPrice"]), util.currencyToGlyph(response["currency"]))