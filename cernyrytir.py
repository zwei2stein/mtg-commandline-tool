import json
import os
import re
import requests
import sys

import console
import util

baseUrl = "http://cernyrytir.cz/index.php3"

clearCache = 'none'
cacheTimeout = 365
args = {}

def getCacheDir():
	baseDir = os.path.join(os.path.dirname(sys.argv[0]), ".cernyRytirCache")
	if (not os.path.exists(baseDir)):
		os.makedirs(baseDir)
	return baseDir

def flushCache():
	if (args.currency == 'czk'):
		try:
			shutil.rmtree(getCacheDir())
		except OSError as e:
			print ("Error where clearing cache directory at " + getCacheDir() + ": %s - %s." % (e.filename, e.strerror))

def initCache(collection):
	if (args.currency == 'czk'):
		lastLength = 0
		count = 1

		for card in collection:

			statusLine = 'Fetching cerny rytir price for (' + str(count) + '/' + str(len(collection)) + ', ...' + str(collection[card].sourceFile)[-50:-2]  + '): ' + card + " ..."

			count += 1
			currentLength = len(statusLine)
			if (currentLength < lastLength):
				statusLine = statusLine + (lastLength - currentLength) * ' '
			# newline before doing "status"
			if (lastLength == 0):
				sys.stdout.write('\n')
			lastLength = currentLength

			sys.stdout.write('\r' + statusLine)
			sys.stdout.flush()
			collection[card].getProp("price")
		doneMessage = ''
		sys.stdout.write('\r' + doneMessage + (lastLength - len(doneMessage)) * " " + '\r')
		sys.stdout.flush()

def getCardPrice(card):
	jsonFile = os.path.join(getCacheDir(), util.cleanFilename(card) + ".json")

	price = None

	if (os.path.exists(jsonFile)):

		with open(jsonFile, encoding='utf-8') as json_data:
			price = json.load(json_data)["price"]

	else:

		response = fetchCardPrice(card)

		if (response is not None):
			with open(jsonFile, 'w') as f:
				json.dump({"price": response, "name": card.name}, f)
		else:
			print(console.CRED +  "Price not found for '" + card.name + "' card at Cerny Rytir." + console.CEND)

		price = response

	if (price is None):
		price = 0

	return float(price)

def fetchCardPrice(card, page = 0, cheapestPrice = None):
	pageSize = 30

	# URL will not accept encoded ', it needs non-UTF8 ´
	name = card.getProp('name').replace('\'', '´').replace('\"', '„').encode("Windows-1252", "ignore")

	response = requests.post(baseUrl, data={'searchname': name, 'searchtype': 'card', 'akce': '3', 'limit': page * pageSize}, params={'searchname': name, 'searchtype': 'card', 'akce': '3', 'limit': page * pageSize})

	regex = '<font style="font-weight : bolder;">(.*?)</font>'

	items = re.findall(regex, response.text)

	names = items[0::3]
	prices = items[2::3]

	for name, price in zip(names, prices):

		ends = [' - foil', ' - lightly played', ' / lightly played', ' - played', ' / played', 
			' / non-english', ' - played / japanese', ' / japanese', ' - japanese', ' - non-english',
			' / chinese', ' / russian', ' - russian']

		for end in ends:
			name = name[::-1].replace(end[::-1], '', 1)[::-1]

		name = name.split(' (')[0]

		name = name.replace('´', '\'').replace('\x84', '\"')

		price = int(price.split('&')[0])

		if ((cheapestPrice == None or cheapestPrice > price) and name.lower() == card.getProp('name').lower()):
			cheapestPrice = price

	if (len(names) == pageSize and 'Nalezeno' in response.text):
		sys.stdout.write('.')
		sys.stdout.flush()
		return fetchCardPrice(card, page = page + 1, cheapestPrice = cheapestPrice)
	else:

		return cheapestPrice