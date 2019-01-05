from decimal import *
import console

import util
import mtgCardInCollectionObject

def getPrice(deckCard, count, currency):
	return count * Decimal(deckCard.jsonData.get(currency, "0.0"));

def missingCards(deckCards, libraryCards, currency):

	shoppingList = {}

	totalDeckCards = 0

	for deckCardName in sorted(deckCards, key=deckCards.__getitem__):
		deckCard = deckCards[deckCardName]
		totalDeckCards += deckCard.count
		if (deckCardName in libraryCards):
			libraryCard = libraryCards[deckCard.name]
			if (libraryCard.count >= deckCard.count):
				print ("v ", str(deckCard.count), " ", console.CGREEN + str(deckCard) + console.CEND)
			elif (libraryCard.count <= 0):
#				print ("x ", str(deckCard.count), " ",  console.CRED + deckCard.name + console.CEND)
				shoppingList[deckCard] = deckCard.count
			elif (libraryCard.count < deckCard.count):
				print ("v ", str(libraryCard.count), " ", str(deckCard))
#				print ("x ", str(deckCard.count - libraryCard.count), " ", console.CRED + deckCard.name + console.CEND)
				shoppingList[deckCard] = deckCard.count - libraryCard.count
		else:
#			print ("x ", str(deckCard.count), " ", console.CRED + deckCard.name + console.CEND)
			shoppingList[deckCard] = deckCard.count

	totalCount = 0

	for deckCard in shoppingList:
		totalCount += shoppingList[deckCard]

	print ()

	print ("Have: " + "{:3.2f}".format(100 * (totalDeckCards - totalCount) / totalDeckCards) + "%")

	if (len(shoppingList) == 0):

		print ()

		print (console.CGREEN + "Nothing to buy." + console.CEND)

	else:

		print ()

		print (console.CRED + "Shopping list:" + console.CEND)

		print ()

		print (console.CGREEN + "Main deck:" + console.CEND)

		totalPrice = Decimal(0)

		for deckCard in sorted(shoppingList):
			if (deckCard.sideboard == 0):
				print (shoppingList[deckCard], deckCard)
				totalPrice += getPrice (deckCard, shoppingList[deckCard], currency)

		print (console.CGREEN + "Main deck + sideboard:" + console.CEND)

		for deckCard in sorted(shoppingList):
			if (deckCard.count != deckCard.sideboard and shoppingList[deckCard] > deckCard.count - deckCard.sideboard):
				print (shoppingList[deckCard], deckCard, str(deckCard.count - deckCard.sideboard) + "+" + str(deckCard.sideboard))
				totalPrice += getPrice (deckCard, shoppingList[deckCard], currency)

		print ( console.CGREEN + "Sideboard:" + console.CEND)

		for deckCard in sorted(shoppingList):
			if (deckCard.count == deckCard.sideboard):
				print (shoppingList[deckCard], deckCard)
				totalPrice += getPrice (deckCard, shoppingList[deckCard], currency)


		if ("price" in mtgCardInCollectionObject.CardInCollection.args.print):
			print ()
			print ( console.CRED + 'Total shopping list price:' + console.CEND, str(totalPrice) + util.currencyToGlyph(currency))