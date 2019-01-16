import re

def manaCurve(deckCards):

	curve = {}

	for deckCardName in deckCards:
		deckCard = deckCards[deckCardName]
		cmc = deckCard.jsonData.get('cmc', 0.0)
		typeLine = deckCard.jsonData.get('type_line','')
		matchLand = re.search('(\\b[lL]and\\b)', typeLine)
		if (not matchLand):
			if (cmc not in curve):
				curve[cmc] = deckCard.count - deckCard.sideboard
			else:
				curve[cmc] = curve[cmc] + deckCard.count - deckCard.sideboard

	response = { "curve": curve }

	return response

def printManaCurveToConsole(response):

	curve = response["curve"]

	print('Mana curve for deck:')

	for cmc in sorted(curve.keys()):
		print (str(cmc) + '=' * curve[cmc], curve[cmc])