import re

def manaCurve(deckCards):

	curve = {}

	for deckCardName in deckCards:
		deckCard = deckCards[deckCardName]
		cmc = deckCard.jsonData.get('cmc', 0.0)
		typeLine = deckCard.jsonData.get('type_line','')
		match = re.search('(\\b[lL]and\\b)', typeLine)
		if (not match):
			if (cmc not in curve):
				curve[cmc] = deckCard.count
			else:
				curve[cmc] = curve[cmc] + deckCard.count

	for cmc in sorted(curve.keys()):
		print (cmc, '=' * curve[cmc], curve[cmc])