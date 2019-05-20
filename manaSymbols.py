from decimal import *

import mtgColors

def manaSymbols(deckCards):

	symbols = {}

	manaCost = ''

	for deckCardName in deckCards:
		deckCard = deckCards[deckCardName]
		if (deckCard.sideboard != deckCard.count):
			manaCost = manaCost + (deckCard.count - deckCard.sideboard) * deckCard.jsonData.get('mana_cost', '')

	# make {U/G} or {2/W} or {HW} symbols parsable.
	manaCost = manaCost.replace('/', '}{').replace('{H', '{')

	for symbol in mtgColors.colorCosts:
		symbols[symbol] = manaCost.count('{'+symbol+'}')

	totalSymbolCount = Decimal(sum(symbols.values()))
	percentSymbols = {}

	for symbol in mtgColors.colorCosts:
		percentSymbols[symbol] = (Decimal(100 * symbols[symbol]) / totalSymbolCount).quantize(Decimal('.1'), rounding=ROUND_DOWN)

	response = { "symbols": symbols, "percentSymbols": percentSymbols }

	return response

def printManaSymbolsToConsole(response):

	print('Mana symbols for deck:')

	symbols = response["symbols"]
	percentSymbols = response["percentSymbols"]

	for symbol in mtgColors.colorCosts:
		print (symbol + ' |' + '=' * symbols[symbol] + " " + str(symbols[symbol]) + " " + str(percentSymbols[symbol]) + '%')