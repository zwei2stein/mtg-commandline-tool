from decimal import *
import console

import util
import mtgCardInCollectionObject

def getPrice(deckCard, count, currency):
	return count * Decimal(deckCard.jsonData.get(currency, "0.0"));

def missingCards(deckCards, libraryCards, currency):

	response = {}

	shoppingList = {}

	haveList = {}

	totalDeckCards = 0

	for deckCardName in sorted(deckCards, key=deckCards.__getitem__):
		deckCard = deckCards[deckCardName]
		totalDeckCards += deckCard.count
		if (deckCardName in libraryCards):
			libraryCard = libraryCards[deckCard.name]
			if (libraryCard.count >= deckCard.count):
				haveList[deckCard] = deckCard.count
			elif (libraryCard.count <= 0):
				shoppingList[deckCard] = deckCard.count
			elif (libraryCard.count < deckCard.count):
				haveList[deckCard] = libraryCard.count
				shoppingList[deckCard] = deckCard.count - libraryCard.count
		else:
			shoppingList[deckCard] = deckCard.count

	totalCount = 0
	totalPrice = Decimal(0)

	for deckCard in shoppingList:
		totalCount += shoppingList[deckCard]
		totalPrice += getPrice(deckCard, shoppingList[deckCard], currency)				

	response['totalCount'] = totalCount
	response['totalPrice'] = totalPrice
	response['totalDeckCards'] = totalDeckCards
	response['shoppingList'] = shoppingList
	response['currency'] = currency
	response['haveList'] = haveList

	return response

def printMissingCardsToConsole(response):

	shoppingList = response['shoppingList']
	haveList = response['haveList']

	print ()

	print ("Have: " + "{:3.2f}".format(100 * (response['totalDeckCards'] - response['totalCount']) / response['totalDeckCards']) + "%")

	for deckCard in sorted(haveList):
		if (deckCard.sideboard == 0):
			print (haveList[deckCard], console.CGREEN + str(deckCard) + console.CEND)

	print (console.CGREEN + "Main deck + sideboard:" + console.CEND)

	for deckCard in sorted(haveList):
		if (deckCard.count != deckCard.sideboard and haveList[deckCard] > deckCard.count - deckCard.sideboard):
			print (haveList[deckCard], console.CGREEN + str(deckCard) + console.CEND, str(deckCard.count - deckCard.sideboard) + "+" + str(deckCard.sideboard))

	print (console.CGREEN + "Sideboard:" + console.CEND)

	for deckCard in sorted(haveList):
		if (deckCard.count == deckCard.sideboard):
			print (haveList[deckCard], console.CGREEN + str(deckCard) + console.CEND)

	if (len(response['shoppingList']) == 0):

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

		print (console.CGREEN + "Main deck + sideboard:" + console.CEND)

		for deckCard in sorted(shoppingList):
			if (deckCard.count != deckCard.sideboard and shoppingList[deckCard] > deckCard.count - deckCard.sideboard):
				print (shoppingList[deckCard], deckCard, str(deckCard.count - deckCard.sideboard) + "+" + str(deckCard.sideboard))

		print ( console.CGREEN + "Sideboard:" + console.CEND)

		for deckCard in sorted(shoppingList):
			if (deckCard.count == deckCard.sideboard):
				print (shoppingList[deckCard], deckCard)


		if ("price" in mtgCardInCollectionObject.CardInCollection.args.print):
			print ()
			print ( console.CRED + 'Total shopping list price:' + console.CEND, str(response['totalPrice']) + util.currencyToGlyph(response['currency'] ))