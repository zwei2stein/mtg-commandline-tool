
def getIsDeckSingleton(deck):

	violatingCards = [] 

	for deckCardName in deck:
		deckCard = deck[deckCardName]

		oracleText = deckCard.getFullOracleText()
		if ("A deck can have any number of cards named" in oracleText):
			continue

		if (deckCard.count > 1 and not deckCard.jsonData.get('type_line', '').startswith('Basic Land')):
			violatingCards.append(deckCardName)

	response = {'violatingCards': violatingCards, 'isDeckSingleton': len(violatingCards) == 0}

	return response

def printgetIsDeckSingletonToConsole(response):
	print ('Singleton status:')
	if (response['isDeckSingleton']):
		print ("Deck is singleton.")
	else:
		print ("Deck is not singleton, violating cards are:")
		for card in response['violatingCards']:
			print ('\t* ' + card)

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
	print ('Card count:')
	print ("Commander:", response["commander"])
	print ("Maindeck:", response["count"])
	print ("Sideboard:", response["sideboardCount"])