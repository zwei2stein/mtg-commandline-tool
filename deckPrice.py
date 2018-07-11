from decimal import *

def deckPrice(deckCards, currency):

	totalPrice = Decimal(0)

	for deckCardName in deckCards:
		deckCard = deckCards[deckCardName]
		totalPrice += Decimal(deckCard.jsonData.get(currency, "0.0"))

	print ('Total price:', str(totalPrice), currencyToGlyph(currency))


def currencyToGlyph(currency):
	if (currency == 'eur'):
		return u'\u20ac'
	elif (currency == 'usd'):
		return '$'
	elif (currency == 'tix'):
		return 'tix'
	else:
		return ''