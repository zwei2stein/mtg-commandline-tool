import console

def verifyDeck(deckCards, libraryCards):

	for deckCardName in sorted(deckCards, key=deckCards.__getitem__):
		deckCard = deckCards[deckCardName]
		if (deckCardName in libraryCards):
			libraryCard = libraryCards[deckCard.name]
			if (libraryCard.count >= deckCard.count):
				print ("v ", str(deckCard.count), " ", console.CGREEN + deckCard.name + console.CEND)
			elif (libraryCard.count == 0):
				print ("x ", str(deckCard.count), " ",  console.CRED + deckCard.name + console.CEND)
			elif (libraryCard.count < deckCard.count):
				if	(libraryCard.count < (deckCard.count - deckCard.sideboard))
					print ("v ", str(libraryCard.count), " ", deckCard.name)
					print ("x ", str(deckCard.count - libraryCard.count), " ", console.CRED + deckCard.name + console.CEND)
				elif (libraryCard.count == (deckCard.count - deckCard.sideboard))
					print ("v ", str(libraryCard.count), " ", deckCard.name)
					print ("x ", str(deckCard.count - libraryCard.count), " ", console.CRED + deckCard.name + console.CEND)
				elif (libraryCard.count > (deckCard.count - deckCard.sideboard))
					print ("v ", str(libraryCard.count), " ", deckCard.name)
					print ("x ", str(deckCard.count - libraryCard.count), " ", console.CRED + deckCard.name + console.CEND)
		else:
			print ("x ", str(deckCard.count), " ", console.CRED + deckCard.name + console.CEND)