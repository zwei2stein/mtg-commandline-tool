
def getIsDeckSingleton(deck):
	for deckCardName in deck:
		deckCard = deck[deckCardName]
		if (deckCard.count > 1 and not deckCard.jsonData.get('type_line', '').startswith('Basic Land')):
			return False
	return True

def printgetIsDeckSingletonToConsole(isDeckSingleton):
	print ('Singleton status:')
	if (isDeckSingleton):
		print ("Deck is singleton.")
	else:
		print ("Deck is not singleton.")

def getDeckCardCount(deck):
	count = 0
	sideboardCount = 0
	commander = 0
	for deckCardName in deck:
		deckCard = deck[deckCardName]
		count += (deckCard.count - deckCard.sideboard)
		sideboardCount += deckCard.sideboard
		if (deckCard.commander):
			commander += deckCard.count
			count -= (deckCard.count - deckCard.sideboard)


	response = { "count": count, "sideboardCount": sideboardCount, "commander": commander }

	return response

def printGetDeckCardCountToConsole(response):
	print( 'Card count:')
	print ("Commander:", response["commander"])
	print ("Maindeck:", response["count"])
	print ("Sideboard:", response["sideboardCount"])