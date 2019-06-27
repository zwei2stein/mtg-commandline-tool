import deckStatistics

import console

formatList = ["commander", "duel", "future", "legacy", "modern", "pauper", "penny", "standard", "vintage", "oldschool"]

singletonFormats = {
	"commander": True,
	"duel": True,
	"future": False,
	"legacy": False,
	"modern": False,
	"pauper": False,
	"penny": False,
	"standard": False,
	"vintage": False,
	"oldschool": False
}

requiresCommander = {
	"commander": True,
	"duel": True,
	"future": False,
	"legacy": False,
	"modern": False,
	"pauper": False,
	"penny": False,
	"standard": False,
	"vintage": False,
	"oldschool": False
}

minCardCount = {
	"commander": 100,
	"duel": 100,
	"future": 60,
	"legacy": 60,
	"modern": 60,
	"pauper": 60,
	"penny": 60,
	"standard": 60,
	"vintage": 60,
	"oldschool": 40
}

maxSideboardSize = {
	"commander": 0,
	"duel": 0,
	"future": 15,
	"legacy": 15,
	"modern": 15,
	"pauper": 15,
	"penny": 15,
	"standard": 15,
	"vintage": 15,
	"oldschool": 15
}

specificityOfFormat = {
	"standard": 10,
	"modern": 8,
	"pauper": 7,
	"penny": 6,
	"commander": 5,
	"EDH": 5,
	"duel": 4,
	"vintage": 2,
	"legacy": 1,
	"oldschool": 0,
	"future": -1
}

budgetPrice = {
	"standard": 50,
	"modern": 100,
	"pauper": 20,
	"penny": 5,
	"commander": 50,
	"duel": 100,
	"vintage": 500,
	"legacy": 500,
	"oldschool": 500,
	"future": -1
}

def canBeCommander(card):

	commanderLegality = card.jsonData.get('legalities', {}).get("commander", "not_legal")
	if (commanderLegality in ['not_legal', 'banned']):
		return False

	faceTypes = card.jsonData.get('type_line', '').split("//")
	faceType = faceTypes[0]
	typesSplit = faceType.strip().split("\u2014")
	if (len(typesSplit) > 1):
		if ("Creature" not in typesSplit[0] or "Legendary" not in typesSplit[0]):
			return False

	return True

def getDeckFormat(deck, watchFormat=None):

	invalidWatchCards = {}
	invalidWatchDeck = []

	formats = {
		"commander": True,
		"duel": True,
		"future": True,
		"legacy": True,
		"modern": True,
		"pauper": True,
		"penny": True,
		"standard": True,
		"vintage": True,
		"oldschool": True
	}

	for deckCardName in deck:
		deckCard = deck[deckCardName]
		legalities = deckCard.jsonData.get('legalities', {})
		for format in formats:
			# We assume that if legality infor is not available, then it is not legal
			legality = legalities.get(format, "not_legal")
			if (legality in ['not_legal', 'banned']):
				if (format == watchFormat):
					invalidWatchCards[deckCardName] = legality
				formats[format] = False

	isDeckSingleton = deckStatistics.getIsDeckSingleton(deck)['isDeckSingleton']
	deckCardCount = deckStatistics.getDeckCardCount(deck)

	for format in formats:
		if (not isDeckSingleton and singletonFormats[format] == True):
			if (format == watchFormat):
				invalidWatchDeck.append("not singleton")
			formats[format] = False
		if (deckCardCount["count"] + deckCardCount["commander"] < minCardCount[format] ):
			if (format == watchFormat):
				invalidWatchDeck.append("too few main deck cards")
			formats[format] = False
		if (requiresCommander[format] and deckCardCount["commander"] < 1):
			if (format == watchFormat):
				invalidWatchDeck.append("missing commander")
			formats[format] = False
		if (maxSideboardSize[format] < deckCardCount["sideboardCount"]):
			if (format == watchFormat):
				invalidWatchDeck.append("too many sideboard cards")
			formats[format] = False

	return {'formats': formats, 'invalidWatchCards': invalidWatchCards, 'invalidWatchDeck': invalidWatchDeck, 'watchFormat': watchFormat}

def printDetDeckFormatToConsole(response, onlyInspect = False):

	formats = response['formats']

	if (not onlyInspect):

		print("Deck valid for format:")
		for format in sorted(formats, key=lambda k: specificityOfFormat[k], reverse=True):
			if (formats[format]):
				print ("\t* ", console.CGREEN + format + console.CEND)

		print("Deck " + console.CRED + "not" + console.CEND + " valid for format:")
		for format in sorted(formats, key=lambda k: specificityOfFormat[k], reverse=True):
			if (not formats[format]):
				print ("\t* ", console.CRED + format +  console.CEND)

	watchFormat = response['watchFormat']

	if (watchFormat != None and formats[watchFormat] == False):
		print ('Deck is not valid in ' + watchFormat + ' format because:')
		for reason in response['invalidWatchDeck']:
			print ('\t* ' + console.CRED + reason + console.CEND)
		for card in response['invalidWatchCards']:
			print ('\t* ' + card + ' is ' + console.CRED + response['invalidWatchCards'][card] + console.CEND)
	elif (watchFormat != None and formats[watchFormat] == True):
		print ('Deck is valid in ' + watchFormat + ' format without issues.')