from decimal import *
import console

import util
import mtgCardInCollectionObject
import cardListFormater

def getPrice(deckCard, count):
	return count * Decimal(deckCard.getProp('price'));

def missingCards(deckCards, collection, currency, oldDeck = None, threshold = None):

	response = {}

	shoppingList = {}

	haveList = {}

	haveInDeckAlreadyList = {}

	removeFromOldDeckList = dict()

	if (oldDeck is not None):
		for deckCardName in sorted(oldDeck, key=oldDeck.__getitem__):
			removeFromOldDeckList[oldDeck[deckCardName]] = oldDeck[deckCardName].count

	totalDeckCards = 0

	for deckCardName in sorted(deckCards, key=deckCards.__getitem__):
		deckCard = deckCards[deckCardName]
		totalDeckCards += deckCard.count
		#for each card in deck:
		neededAmount = deckCard.count

		if (oldDeck is not None):
			if (deckCardName in oldDeck):
				cardAlreadyInDeck = oldDeck[deckCard.name]
				if (cardAlreadyInDeck.count >= neededAmount):
					haveInDeckAlreadyList[deckCard] = neededAmount
					neededAmount = 0
				else:
					haveInDeckAlreadyList[deckCard] = cardInCollection.count
					neededAmount = neededAmount - cardInCollection.count
				removeFromOldDeckList[cardAlreadyInDeck] = neededAmount
				
		if (neededAmount > 0):
			if (deckCardName in collection):
				cardInCollection = collection[deckCard.name]
				if (cardInCollection.count >= neededAmount):
					haveList[deckCard] = neededAmount
				elif (cardInCollection.count <= 0):
					shoppingList[deckCard] = neededAmount
				elif (cardInCollection.count < neededAmount):
					haveList[deckCard] = cardInCollection.count
					shoppingList[deckCard] = neededAmount - cardInCollection.count
			else:
				shoppingList[deckCard] = neededAmount

	totalCount = 0
	totalPrice = Decimal(0)

	for deckCard in shoppingList:
		totalCount += shoppingList[deckCard]
		if (threshold is None or Decimal(deckCard.getProp('price')) >= Decimal(threshold)):
			totalPrice += getPrice(deckCard, shoppingList[deckCard])

	removeFromOldDeckList = {k: v for k, v in removeFromOldDeckList.items() if v > 0}

	response['totalCount'] = totalCount
	response['totalPrice'] = totalPrice
	response['threshold'] = threshold
	response['totalDeckCards'] = totalDeckCards
	response['shoppingList'] = shoppingList
	response['currency'] = currency
	response['haveList'] = haveList
	response['oldDeck'] = oldDeck is not None
	response['haveInDeckAlreadyList'] = haveInDeckAlreadyList
	response['removeFromOldDeckList'] = removeFromOldDeckList

	return response

def printMissingCardsToConsole(response):
	print ()

	if (response['totalDeckCards'] == 0):
		print ("Have: 100.00%")
	else:
		print ("Have: " + "{:3.2f}".format(100 * (response['totalDeckCards'] - response['totalCount']) / response['totalDeckCards']) + "%")

	if (len(response['haveInDeckAlreadyList']) > 0):

		print ()
		print ("Cards already in deck:")
		cardListFormater.printCardObjectList(cardListFormater.cardObjectCountMapToCardObjectMap(response['haveInDeckAlreadyList']), console.CGREEN)

	if (len(response['haveList']) > 0):
		
		print ()
		print ("Cards already in collection, not in deck:")
		print ()
		cardListFormater.printCardObjectList(cardListFormater.cardObjectCountMapToCardObjectMap(response['haveList']), console.CGREEN)


	if (len(response['removeFromOldDeckList']) > 0):

		print ()
		print (console.CRED + "Cards removed from deck:" + console.CEND)
		print ()
		cardListFormater.printCardObjectList(cardListFormater.cardObjectCountMapToCardObjectMap(response['removeFromOldDeckList']), console.CRED)


	if (len(response['shoppingList']) == 0):

		print ()
		print (console.CGREEN + "Nothing to buy." + console.CEND)

	else:

		print ()
		print (console.CRED + "Shopping list:" + console.CEND)
		print ()

		cardListFormater.printCardObjectList(cardListFormater.cardObjectCountMapToCardObjectMap(response['shoppingList']), console.CRED)

		if ("price" in mtgCardInCollectionObject.CardInCollection.args.print):
			print ()
			print ( console.CRED + 'Total shopping list price:' + console.CEND + " " + "{:3.2f}".format(response['totalPrice']) + util.currencyToGlyph(response['currency'] ))
			if (response['threshold'] is not None): 
				print ()
				print ('(Cards with price lower than ' + str(response['threshold']) + util.currencyToGlyph(response["currency"]) + ' were not inluded in total price.)')