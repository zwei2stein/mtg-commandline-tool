import scryfall

import console

def search(query, collection):
	found = scryfall.search(query)

	for card in found:
		if (card in collection):
			collectionCard = collection[card]
			if (collectionCard.count > 0):
				print (console.CGREEN + card + console.CEND)
			else:
				print (console.CRED + card + console.CEND)
		else:
			print (console.CRED + card + console.CEND)