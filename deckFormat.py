import deckStatistics

import console

def getDeckFormat(deck):

	formats = {
        "commander": True,
        "duel": True,
        "frontier": True,
        "future": True,
        "legacy": True,
        "modern": True,
        "pauper": True,
        "penny": True,
        "standard": True,
        "vintage": True,
        "oldschool": True
    }

	singletonFormats = {
        "commander": True,
        "duel": True,
        "frontier": False,
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
        "frontier": 60,
        "future": 60,
        "legacy": 60,
        "modern": 60,
        "pauper": 60,
        "penny": 60,
        "standard": 60,
        "vintage": 60,
        "oldschool": 40
    }

	for deckCardName in deck:
		deckCard = deck[deckCardName]
		legalities = deckCard.jsonData.get('legalities', 'C')
		print (deckCardName)
		print (legalities)
		for format in formats:
			# We assume that if legality infor is not available, then it is not legal
			legality = legalities.get(format, "not_legal")
			if (legality in ['not_legal', 'banned']):
				formats[format] = False

	isDeckSingleton = deckStatistics.getIsDeckSingleton(deck)
	deckCardCount = deckStatistics.getDeckCardCount(deck)

	for format in formats:
		if (not isDeckSingleton and singletonFormats[format] == True):
			formats[format] = False
		if (deckCardCount["count"] < minCardCount[format] ):
			formats[format] = False

	return formats

def printDetDeckFormatToConsole(formats):
	print("Deck valid for format:")
	for format in sorted(formats):
		if (formats[format]):
			print ("\t*", console.CGREEN + format + console.CEND)

	print("Deck " + console.CRED + "not" + console.CEND + " valid for format:")
	for format in sorted(formats):
		if (not formats[format]):
			print ("\t*", console.CRED + format +  console.CEND)