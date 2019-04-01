import re
from decimal import *

import mtgColors
import util

def landMana(deckCards):

	landSymbols = {}
	for symbol in mtgColors.colorCosts:
		landSymbols[symbol] = 0

	for deckCardName in deckCards:
		deckCard = deckCards[deckCardName]
		oracleText = util.getFullOracleText(deckCard)
		typeLine = util.getFullTypeLine(deckCard)

		matchLand = re.search('(\\b[lL]and\\b)', typeLine)
		if (matchLand):
			for symbol in mtgColors.colorCosts:
				match = re.search('[aA]dd {'+symbol+'}', oracleText)
				if (match):
					landSymbols[symbol] = landSymbols[symbol] + (deckCard.count - deckCard.sideboard)

	totalLandSymbolCount = Decimal(sum(landSymbols.values()))
	percentLandSymbols = {}

	getcontext().prec = 3

	for symbol in mtgColors.colorCosts:
		percentLandSymbols[symbol] = Decimal(100 * landSymbols[symbol]) / totalLandSymbolCount

	response = { "landSymbols": landSymbols, "percentLandSymbols": percentLandSymbols }

	return response

def printLandManaToConsole(response):

	print('Mana from lands for deck:')

	landSymbols = response["landSymbols"]
	percentLandSymbols = response["percentLandSymbols"]

	for symbol in mtgColors.colorCosts:
		print (symbol + ' |' + '=' * landSymbols[symbol] + " " + str(landSymbols[symbol]) + " " + str(percentLandSymbols[symbol]) + '%')