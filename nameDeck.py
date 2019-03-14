import mtgColors
import deckFormat
import deckCreatureTypes

colorPairingNames = {
 'W': ['White', 'Monowhite', 'Mono-white'],
 'U': ['Blue', 'Monoblue', 'Mono-blue'],
 'B': ['Black', 'Monoblack', 'Mono-black'],
 'R': ['Red', 'Monored', 'Mono-red'],
 'G': ['Green', 'Monogreen', 'Mono-green'],
 'WU': ['Azorius', 'White/Blue', 'White-Blue', 'WU'],
 'WB': ['Orzhov', 'White/Black', 'White-Black', 'WB'],
 'WR': ['Boros', 'White/Red', 'White-Red', 'WR'],
 'WG': ['Selesnya', 'White/Green', 'White-Green', 'WG'],
 'UB': ['Dimir', 'Blue/Black', 'Blue-Black', 'UB'],
 'UR': ['Izzet', 'Blue/Red', 'Blue-Red', 'UR'],
 'UG': ['Simic', 'Blue/Green', 'Blue-Green', "UG"],
 'BR': ['Rakdos', 'Black/Red', 'Black-Red', 'BR'],
 'BG': ['Golgari', 'Black/Green', 'Black-Green', 'BG'],
 'RG': ['Gruul', 'Red/Green', 'Red-Green', 'RG'],
 'WUB': ['Esper', 'WUB'],
 'WUR': ['Jeskai', 'WUR', 'Raka'],
 'WUG': ['Bant', 'WUG'],
 'WBR': ['Mardu', 'WBR', 'Borzhov', 'Dega'],
 'WBG': ['Abzan', 'WBG', 'Necra'],
 'WRG': ['Naya', 'WRG'],
 'UBR': ['Grixis', 'UBR'],
 'UBG': ['Sultai', 'UBG', 'Ana'],
 'URG': ['Temur', 'URG', 'Grizzet', 'Ceta'],
 'BRG': ['Jund', 'BRG'],
 'WUBR': ['WUBR', 'Artifice'],
 'WUBG': ['WUBG', 'Growth'],
 'WURG': ['WURG', 'Altruism'],
 'WBRG': ['WBRG', 'Aggression'],
 'UBRG': ['UBRG', 'Chaos'],
 'WUBRG': ['Prismatic', '5-Color', 'Multicolor', 'Rainbow', 'Domain'],
 'C': ['Colorless', 'Eldrazi', 'Monobrown', 'Diamond']}

keywords = []

def getKeywords(deck):

	keywords = {}

	for deckCardName in deck:
		deckCard = deck[deckCardName]

		oracleText = deckCard.jsonData.get('oracle_text', '')

		for face in deckCard.jsonData.get('card_faces', []):
			oracleText = oracleText + '\n' + face.get('oracle_text', '')

		

	return creatureTypeCounts

def getTribalNames(deck):

	creatureTypes = deckCreatureTypes.getCreatureTypes(deck)

	creatureCount = deckCreatureTypes.getCreatureCount(deck)

	maxCount = 0
	commonTypes = []
	for creatureType in creatureTypes:
		if creatureTypes[creatureType] > maxCount and creatureTypes[creatureType] > creatureCount * 2:
			maxCount = creatureTypes[creatureType]
			commonTypes = []
		if creatureTypes[creatureType] == maxCount:
			commonTypes.append(creatureType)


	return commonTypes

def nameDeck(deck):

	names = []

	colorNames = colorPairingNames[mtgColors.colorIdentity2String((mtgColors.getDeckColorIdentity(deck)))]

	tribalNames = getTribalNames(deck)

	deckFormat.printDetDeckFormatToConsole(deckFormat.getDeckFormat(deck))

	names.append(colorNames)
	names.append(tribalNames)

	response = {}

	response['names'] = names

	return response


def printnDeckNameToConsole(response):

	print ('Deck names:')

	for name in response['names']:
		print ('*', name)