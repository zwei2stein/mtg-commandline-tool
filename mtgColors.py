colorOrder = ['W', 'U', 'B', 'R', 'G', 'WU', 'WB', 'WR', 'WG', 'UB', 'UR', 'UG', 'BR', 'BG', 'RG', 'WUB', 'WUR', 'WUG', 'WBR', 'WBG', 'WRG', 'UBR', 'UBG', 'URG', 'BRG', 'WUBR', 'WUBG', 'WURG', 'WBRG', 'UBRG', 'WUBRG', 'C']

colorCosts = ['W', 'U', 'B', 'R', 'G', 'C']

def getDeckColorIdentity(deck):

	colors = set()

	for deckCardName in deck:
		deckCard = deck[deckCardName]
		colorIdentity = deckCard.jsonData.get('color_identity', 'C')
		colors.update(colorIdentity)

	return colors

def compareColorsString(colorString1, colorString2):
	index1 = -1
	index2 = -1
	for i in range(1, len(colorOrder)):
		if colorString1 == colorOrder[i]:
			index1 = i
		if colorString2 == colorOrder[i]:
			index2 = i
	return index1 > index2	

def colorIdentity2String(colorIdentity):
	if colorIdentity is None or len(colorIdentity) == 0:
		return 'C'
	return ''.join([c for c in 'WUBRG' if c in ''.join(colorIdentity)])

def compareColors(colorIdentity1, colorIdentity2):
	return compareColorsString(colorIdentity2String(colorIdentity1), colorIdentity2String(colorIdentity2))