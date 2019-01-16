import re
from decimal import *

import mtgColors

def landMana(deckCards):

	landSymbols = {}
	for symbol in mtgColors.colorCosts:
		landSymbols[symbol] = 0

	for deckCardName in deckCards:
		deckCard = deckCards[deckCardName]
		oracleText = deckCard.jsonData.get('oracle_text', '')
		typeLine = deckCard.jsonData.get('type_line', '')

		for face in deckCard.jsonData.get('card_faces', []):
			oracleText = oracleText + '\n' + face.get('oracle_text', '')
			typeLine = typeLine + '\n' + face.get('type_line', '')

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