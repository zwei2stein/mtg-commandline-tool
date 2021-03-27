from datetime import datetime

import humanize

import scryfall
import sets


def deckAge(deckCards):
    cardsPrintDates = []

    for deckCardName, deckCard in deckCards.items():

        cardPrintings = scryfall.searchByCard(deckCard)

        printDates = []

        for cardPrinting in cardPrintings:
            printDates.append(sets.getSetDate(cardPrinting["set"]))

        cardsPrintDates.append(min(printDates))

    response = {"deckDate": max(cardsPrintDates)}

    return response


def printDeckAgeConsole(response):
    print('Latest deck card:', humanize.naturaldelta(response["deckDate"] - datetime.now(), months=True))
