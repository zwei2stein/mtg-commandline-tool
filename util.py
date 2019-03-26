

def currencyToGlyph(currency):
	if (currency == 'eur'):
		return u'\u20ac'
	elif (currency == 'usd'):
		return '$'
	elif (currency == 'tix'):
		return 'tix'
	else:
		return ''

def getFullOracleText(card):
	oracleText = card.jsonData.get('oracle_text', '')
	for face in card.jsonData.get('card_faces', []):
		oracleText = oracleText + '\n' + face.get('oracle_text', '')
	
	return oracleText