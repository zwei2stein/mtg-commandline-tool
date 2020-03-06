import unicodedata
import string
import os
import sys

valid_filename_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)

progressAnimation = ['|', '/', '-', '\\']

def printProgress(progress):
	sys.stdout.write('\b')
	sys.stdout.write(progressAnimation[progress % len(progressAnimation)])
	sys.stdout.flush()

def cleanFilename(card, whitelist=valid_filename_chars, replace=' '):

	filename = card.name
	# replace spaces
	for r in replace:
		filename = filename.replace(r, '_')
	
	# keep only valid ascii chars
	cleaned_filename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore').decode()
	
	# keep only whitelisted chars
	return ''.join(c for c in cleaned_filename if c in whitelist)

def currencyToGlyph(currency):
	if (currency == 'eur'):
		return u'\u20ac'
	elif (currency == 'usd'):
		return '$'
	elif (currency == 'tix'):
		return 'tix'
	elif (currency == 'czk'):
		return 'kc'
	else:
		return ''