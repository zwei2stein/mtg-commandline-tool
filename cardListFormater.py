import sys

import mtgCardInCollectionObject
import mtgCardTextFileDao


# ['Shock'] -> {'Shock': CardInCollection(Shock)}
def cardListToCardObjectMap(cardList, context, defaultCount=1):
    cardObjectList = cardListToCardObjectList(cardList, context, defaultCount=defaultCount)
    cardObjectMap = cardObjectListToCardObjectMap(cardObjectList)
    return cardObjectMap


# [CardInCollection(Shock)] -> {'Shock': CardInCollection(Shock)}
def cardObjectListToCardObjectMap(cardObjectList):
    card_map = {}
    for card in cardObjectList:
        if card.name in card_map:
            card_map[card.name].add(card.count, card, card.sideboard, card.commander, card.getProp('set'))
        else:
            card_map[card.name] = card
    return card_map


# ['Shock'] -> [CardInCollection(Shock)]
def cardListToCardObjectList(cardList, context, defaultCount=1):
    return list(map(
        lambda name: mtgCardInCollectionObject.CardInCollection(name, defaultCount, None, None, 0, False, None, None,
                                                                context), cardList))


# {'Shock': 1} -> {'Shock': CardInCollection(Shock)}
def cardCountMapToCardObjectMap(cardCountMap, context):
    return {x: mtgCardInCollectionObject.CardInCollection(x, cardCountMap[x], None, None, 0, False, None, None, context)
            for x in cardCountMap}


# {CardInCollection(Shock): 1} ->  {'Shock': CardInCollection(Shock)}
def cardObjectCountMapToCardObjectMap(cardObjectCountMap):
    return {card.name: mtgCardInCollectionObject.CardInCollection(card.name, cardObjectCountMap[card], None, None,
                                                                  card.sideboard, card.commander, card.getProp('set'),
                                                                  card.propCache, card.context) for card in
            cardObjectCountMap}

def printCardObjectList(cardList, context, color=None):
    mtgCardTextFileDao.saveCardFile(sys.stdout, cardList, context.group, context, diffFormat=False, color=color)

