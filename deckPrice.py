from decimal import *

import console
import util


def deckPrice(deckCards, currency, threshold=None):
    totalPrice = Decimal(0)
    sideboardPrice = Decimal(0)
    commanderPrice = Decimal(0)

    for deckCardName in deckCards:
        deckCard = deckCards[deckCardName]
        if (threshold is None or Decimal(deckCard.getProp('price')) >= Decimal(threshold)):
            totalPrice += ((deckCard.count - deckCard.sideboard) * Decimal(deckCard.getProp('price')))
            sideboardPrice += (deckCard.sideboard * Decimal(deckCard.getProp('price')))
        if (deckCard.commander):
            commanderPrice += Decimal(deckCard.getProp('price'))

    deckPrice = totalPrice - (sideboardPrice + commanderPrice)

    response = {"threshold": threshold, "currency": currency,
                "deckPrice": deckPrice.quantize(Decimal('.01'), rounding=ROUND_DOWN),
                "sideboardPrice": sideboardPrice.quantize(Decimal('.01'), rounding=ROUND_DOWN),
                "totalPrice": totalPrice.quantize(Decimal('.01'), rounding=ROUND_DOWN),
                "commanderPrice": commanderPrice.quantize(Decimal('.01'), rounding=ROUND_DOWN)}

    return response


def printPricesToConsole(response):
    print('Price of deck:')

    if (response["commanderPrice"] > 0):
        print('Commander:', str(response["commanderPrice"]), util.currencyToGlyph(response["currency"]))
    print('Deck:', str(response["deckPrice"]), util.currencyToGlyph(response["currency"]))
    if (response["sideboardPrice"] > 0):
        print('Sideboard:', str(response["sideboardPrice"]), util.currencyToGlyph(response["currency"]))
    print(console.CRED + 'Total:' + console.CEND, str(response["totalPrice"]),
          util.currencyToGlyph(response["currency"]))

    if response['threshold'] is not None:
        print()
        print('(Cards with price lower than ' + str(response['threshold']) + util.currencyToGlyph(
            response["currency"]) + ' were not included in total price.)')
