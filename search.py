import scryfall
import cardListFormater

import console


def search(query, collection, context):
	found = scryfall.search(query)

	have = []
	havenot = []

	for card in found:
		if (card in collection):
			collectionCard = collection[card]
			if (collectionCard.count > 0):
				have.append(collectionCard)
			else:
				havenot.append(card)
		else:
			havenot.append(card)

	if (len(have) > 0):
		print ('Have:')
		cardListFormater.printCardObjectList(cardListFormater.cardObjectListToCardObjectMap(have), context, color=console.CGREEN)

	if (len(have) > 0 and len(havenot) > 0):
		print ('')

	if (len(havenot) > 0):
		print ('Don\'t have:')
		cardListFormater.printCardObjectList(cardListFormater.cardListToCardObjectMap(havenot, context, 1), context, color=console.CRED)