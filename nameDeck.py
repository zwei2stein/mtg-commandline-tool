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

 #and the four-color nicknames chaos, aggression, altruism, growth, artifice are supported.

def nameDeck(deck):

	names = []

	colorNames = colorPairingNames[mtgColors.colorIdentity2String((mtgColors.getDeckColorIdentity(deck)))]

	deckFormat.printDetDeckFormatToConsole(deckFormat.getDeckFormat(deck))

	deckCreatureTypes.printnGetCreatureTypes(deckCreatureTypes.getCreatureTypes(deck))

	names.append(colorNames)

	response = {}

	response['names'] = names

	return response


def printnDeckNameToConsole(response):

	print ('Deck names:')

	for name in response['names']:
		print ('*', name)