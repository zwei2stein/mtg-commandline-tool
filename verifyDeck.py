from decimal import *
import console

import util

def outputPrice(deckCard, count, printPrice, currency):
	if (printPrice):
		price = count * Decimal(deckCard.jsonData.get(currency, "0.0"));
		print ("", str(price) + util.currencyToGlyph(currency))
		return price
	else:
		print ()
		return Decimal(0)

def verifyDeck(deckCards, libraryCards, printPrice, currency):

	shoppingList = {}

	for deckCardName in sorted(deckCards, key=deckCards.__getitem__):
		deckCard = deckCards[deckCardName]
		if (deckCardName in libraryCards):
			libraryCard = libraryCards[deckCard.name]
			if (libraryCard.count >= deckCard.count):
				print ("v ", str(deckCard.count), " ", console.CGREEN + deckCard.name + console.CEND)
			elif (libraryCard.count == 0):
#				print ("x ", str(deckCard.count), " ",  console.CRED + deckCard.name + console.CEND)
				shoppingList[deckCard] = deckCard.count
			elif (libraryCard.count < deckCard.count):
				print ("v ", str(libraryCard.count), " ", deckCard.name)
#				print ("x ", str(deckCard.count - libraryCard.count), " ", console.CRED + deckCard.name + console.CEND)
				shoppingList[deckCard] = deckCard.count - libraryCard.count
		else:
#			print ("x ", str(deckCard.count), " ", console.CRED + deckCard.name + console.CEND)
			shoppingList[deckCard] = deckCard.count

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
				print (shoppingList[deckCard], deckCard.name, end='')
				totalPrice += outputPrice (deckCard, shoppingList[deckCard], printPrice, currency)

		print (console.CGREEN + "Main deck + sideboard:" + console.CEND)

		for deckCard in sorted(shoppingList):
			if (deckCard.count != deckCard.sideboard and shoppingList[deckCard] > deckCard.count - deckCard.sideboard):
				print (shoppingList[deckCard], deckCard.name, str(deckCard.count - deckCard.sideboard) + "+" + str(deckCard.sideboard), end='')
				totalPrice += outputPrice (deckCard, shoppingList[deckCard], printPrice, currency)

		print ( console.CGREEN + "Sideboard:" + console.CEND)

		for deckCard in sorted(shoppingList):
			if (deckCard.count == deckCard.sideboard):
				print (shoppingList[deckCard], deckCard.name, end='')
				totalPrice += outputPrice (deckCard, shoppingList[deckCard], printPrice, currency)


		if (printPrice):
			print ()
			print ( console.CRED + 'Total shopping list price:' + console.CEND, str(totalPrice) + util.currencyToGlyph(currency))