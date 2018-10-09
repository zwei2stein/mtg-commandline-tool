import deckStatistics

import console

def getDeckFormat(deck):

	formats = {
        "1v1": True,
        "brawl": True,
        "commander": True,
        "duel": True,
        "frontier": True,
        "future": True,
        "legacy": True,
        "modern": True,
        "pauper": True,
        "penny": True,
        "standard": True,
        "vintage": True
    }

	singletonFormats = {
        "1v1": True,
        "brawl": True,
        "commander": True,
        "duel": True,
        "frontier": False,
        "future": False,
        "legacy": False,
        "modern": False,
        "pauper": False,
        "penny": False,
        "standard": False,
        "vintage": False
    }

	minCardCount = {
        "1v1": 100,
        "brawl": 60,
        "commander": 100,
        "duel": 100,
        "frontier": 60,
        "future": 60,
        "legacy": 60,
        "modern": 60,
        "pauper": 60,
        "penny": 60,
        "standard": 60,
        "vintage": 60
    }

	for deckCardName in deck:
		deckCard = deck[deckCardName]
		legalities = deckCard.jsonData.get('legalities', 'C')
		
		for format in formats:
			if (legalities[format] == 'not_legal'):
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