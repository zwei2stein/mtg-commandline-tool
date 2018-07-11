from decimal import *

import mtgColors

def manaSymbols(deckCards):

	symbols = {}

	manaCost = ''

	for deckCardName in deckCards:
		deckCard = deckCards[deckCardName]
		manaCost = manaCost + deckCard.jsonData.get('mana_cost', '')

	# make {U/G} or {2/W} or {HW} symbols parsable.
	manaCost = manaCost.replace('/', '}{').replace('{H', '{')

	for symbol in mtgColors.colorCosts:
		symbols[symbol] = manaCost.count('{'+symbol+'}')

	getcontext().prec = 3

	totalSymbolCount = Decimal(sum(symbols.values()))
	percentSymbols = {}

	for symbol in mtgColors.colorCosts:
		percentSymbols[symbol] = Decimal(100 * symbols[symbol]) / totalSymbolCount

	for symbol in mtgColors.colorCosts:
		print (symbol, '|' + '=' * symbols[symbol], symbols[symbol], str(percentSymbols[symbol]) + '%')