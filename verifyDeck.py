import console

def verifyDeck(deckCards, libraryCards):

	shoppingList = {}

	for deckCardName in sorted(deckCards, key=deckCards.__getitem__):
		deckCard = deckCards[deckCardName]
		if (deckCardName in libraryCards):
			libraryCard = libraryCards[deckCard.name]
			if (libraryCard.count >= deckCard.count):
				print ("v ", str(deckCard.count), " ", console.CGREEN + deckCard.name + console.CEND)
			elif (libraryCard.count == 0):
				print ("x ", str(deckCard.count), " ",  console.CRED + deckCard.name + console.CEND)
				shoppingList[deckCard] = deckCard.count
			elif (libraryCard.count < deckCard.count):
				print ("v ", str(libraryCard.count), " ", deckCard.name)
				print ("x ", str(deckCard.count - libraryCard.count), " ", console.CRED + deckCard.name + console.CEND)
				shoppingList[deckCard] = deckCard.count - libraryCard.count
		else:
			print ("x ", str(deckCard.count), " ", console.CRED + deckCard.name + console.CEND)
			shoppingList[deckCard] = deckCard.count

	print ()

	print ( console.CGREEN + "Shopping list:" + console.CEND)

	print ()

	print ( console.CGREEN + "Main deck:" + console.CEND)

	for deckCard in sorted(shoppingList):
		if (deckCard.sideboard == 0):
			print ( shoppingList[deckCard], deckCard.name)

	print ( console.CGREEN + "Main deck + sideboard:" + console.CEND)

	for deckCard in sorted(shoppingList):
		if (deckCard.count != deckCard.sideboard and shoppingList[deckCard] > deckCard.count - deckCard.sideboard):
			print ( shoppingList[deckCard], deckCard.name, deckCard.count - deckCard.sideboard, "+" ,deckCard.sideboard)

	print ( console.CGREEN + "Sideboard:" + console.CEND)

	for deckCard in sorted(shoppingList):
		if (deckCard.count == deckCard.sideboard):
			print ( shoppingList[deckCard], deckCard.name)
