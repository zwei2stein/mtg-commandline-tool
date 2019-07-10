import scryfall

import console

def search(query, collection):
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

	for card in have:
		print (str(card.count) + " " + console.CGREEN + card.name + console.CEND)

	if (len(have) > 0):
		print ('Don\'t have:')

	for card in havenot:
		print ("0 " + console.CRED + card + console.CEND)