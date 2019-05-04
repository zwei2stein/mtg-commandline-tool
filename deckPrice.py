from decimal import *
import console

import util

def deckPrice(deckCards, currency):

	totalPrice = Decimal(0)
	sideboardPrice = Decimal(0)
	commanderPrice = Decimal(0)

	for deckCardName in deckCards:
		deckCard = deckCards[deckCardName]
		totalPrice += ((deckCard.count - deckCard.sideboard) * Decimal(deckCard.getProp('price')))
		sideboardPrice += (deckCard.sideboard * Decimal(deckCard.getProp('price')))
		if (deckCard.commander):
			commanderPrice += Decimal(deckCard.getProp('price'))

	deckPrice = totalPrice - (sideboardPrice + commanderPrice)

	response = { "currency": currency, "deckPrice": deckPrice, "sideboardPrice": sideboardPrice, "totalPrice": totalPrice, "commanderPrice": commanderPrice }
	
	return response

def printPricesToConsole(response):

	print('Price of deck:')

	if (response["commanderPrice"] > 0):
		print ('Commander:', str(response["commanderPrice"]), util.currencyToGlyph(response["currency"]))
	print ('Deck:', str(response["deckPrice"]), util.currencyToGlyph(response["currency"]) )
	if (response["sideboardPrice"] > 0):
		print ('Sideboard:', str(response["sideboardPrice"]), util.currencyToGlyph(response["currency"]))
	print ( console.CRED + 'Total:' + console.CEND, str(response["totalPrice"]), util.currencyToGlyph(response["currency"]))