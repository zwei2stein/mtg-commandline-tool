from datetime import datetime

import humanize

def deckAge(deckCards):
    cardsPrintDates = []

    for deckCardName, deckCard in deckCards.items():
        cardsPrintDates.append(deckCard.getProp('age'))

    response = {"deckDate": max(cardsPrintDates)}

    return response


def printDeckAgeConsole(response):
    print('Latest deck card:', humanize.naturaldelta(response["deckDate"] - datetime.now(), months=True))
