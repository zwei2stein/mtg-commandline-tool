
def getIsDeckSingleton(deck):
	for deckCardName in deck:
		deckCard = deck[deckCardName]
		if (deckCard.count > 1 and not deckCard.jsonData.get('type_line', '').startswith('Basic Land')):
			return False
	return True

def printgetIsDeckSingletonToConsole(isDeckSingleton):
	if (isDeckSingleton):
		print("Deck is singleton.")
	else:
		print("Deck is not singleton.")

def getDeckCardCount(deck):
	count = 0
	sideboardCount = 0
	for deckCardName in deck:
		deckCard = deck[deckCardName]
		count += (deckCard.count - deckCard.sideboard)
		sideboardCount += deckCard.sideboard

	response = {"count": count, "sideboardCount": sideboardCount}

	return response

def printGetDeckCardCountToConsole(response):
	print ("Maindeck:", response["count"])
	print ("Sideboard:", response["sideboardCount"])