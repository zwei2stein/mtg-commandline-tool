def verifyDeck(deckCards, libraryCards):

	CRED = '\033[91m'
	CGREEN = '\033[92m'
	CEND = '\033[0m'
	

	for deckCardName in deckCards:
		deckCard = deckCards[deckCardName]
		if (deckCardName in libraryCards):
			libraryCard = libraryCards[deckCard.name]
			if (libraryCard.count >= deckCard.count):
				print ("v ", str(deckCard.count), " ", CGREEN + deckCard.name + CEND)
			elif (libraryCard.count == 0):
				print ("x ", str(deckCard.count), " ",  CRED + deckCard.name + CEND)
			elif (libraryCard.count < deckCard.count):
				print ("v ", str(libraryCard.count), " ", deckCard.name)
				print ("x ", str(deckCard.count - libraryCard.count), " ", CRED + deckCard.name + CEND)
		else:
			print ("x ", str(deckCard.count), " ", CRED + deckCard.name + CEND)