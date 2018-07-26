

def currencyToGlyph(currency):
	if (currency == 'eur'):
		return u'\u20ac'
	elif (currency == 'usd'):
		return '$'
	elif (currency == 'tix'):
		return 'tix'
	else:
		return ''