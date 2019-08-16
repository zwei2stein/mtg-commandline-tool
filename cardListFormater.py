import sys

import mtgCardInCollectionObject
import mtgCardTextFileDao

from pprint import pprint

# ['Shock'] -> {'Shock': CardInCollection(Shock)}
def cardListToCardObjectMap(cardList, defaultCount = 1):
	cardObjectList = cardListToCardObjectList(cardList, defaultCount = defaultCount)
	cardObjectMap = cardObjectListToCardObjectMap(cardObjectList)
	return cardObjectMap

# [CardInCollection(Shock)] -> {'Shock': CardInCollection(Shock)}
def cardObjectListToCardObjectMap(cardObjectList):
	map = {}
	for card in cardObjectList:
		if (card.name in map):
			map[card.name].add(card.count, card, card.sideboard, card.commander)
		else:
			map[card.name] = card
	return map

# ['Shock'] -> [CardInCollection(Shock)]
def cardListToCardObjectList(cardList,  defaultCount = 1):
	return list(map(lambda name: mtgCardInCollectionObject.CardInCollection(name, defaultCount, None, None, 0, False), cardList))

# {'Shock': 1} -> {'Shock': CardInCollection(Shock)}
def cardCountMapToCardObjectMap(cardCountMap):
	return {x: mtgCardInCollectionObject.CardInCollection(x, cardCountMap[x], None, None, 0, False) for x in cardCountMap}

# {CardInCollection(Shock): 1} ->  {'Shock': CardInCollection(Shock)}
def cardObjectCountMapToCardObjectMap(cardObjectCountMap):
	return  {card.name: mtgCardInCollectionObject.CardInCollection(card.name, cardObjectCountMap[card], None, None, card.sideboard, card.commander) for card in cardObjectCountMap}

def printCardObjectList(cardList, color=None):
	sorts = mtgCardInCollectionObject.CardInCollection.args.group
	mtgCardTextFileDao.saveCardFile(sys.stdout, cardList, sorts, diffFormat=False, color=color)