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

		match = re.search('(\\b[lL]and\\b)', typeLine)
		if (match):
			for symbol in mtgColors.colorCosts:
				match = re.search('[aA]dd {'+symbol+'}', oracleText)
				if (match):
					landSymbols[symbol] = landSymbols[symbol] + deckCard.count

	totalLandSymbolCount = Decimal(sum(landSymbols.values()))
	percentLandSymbols = {}

	for symbol in mtgColors.colorCosts:
		percentLandSymbols[symbol] = Decimal(100 * landSymbols[symbol]) / totalLandSymbolCount

	for symbol in mtgColors.colorCosts:
		print (symbol, '|' + '=' * landSymbols[symbol], landSymbols[symbol], str(percentLandSymbols[symbol]) + '%')