import datetime
import json
import os
import re
import requests
import shutil
import sys

import console
import util

baseUrl = "https://www.najada.cz/cz/kusovky-mtg/omezit-500"

clearCache = 'none'
cacheTimeout = 365
smartFlush = False
args = {}

def getCacheDir():
	baseDir = os.path.join(os.path.dirname(sys.argv[0]), ".najadaCache")
	if (not os.path.exists(baseDir)):
		os.makedirs(baseDir)
	return baseDir

def flushCache():
	if (args.currency == 'czk'):
		try:
			shutil.rmtree(getCacheDir())
		except OSError as e:
			print ("Error where clearing cache directory at " + getCacheDir() + ": %s - %s." % (e.filename, e.strerror))

def smartFlushCache():
	# 1) highest price is likely to be most volatile
	# 2) don't redownload on same day.

	cacheDir = getCacheDir()

	maxPriceFile = None
	maxPrice = 0

	for dirpath, dirnames, files in os.walk(cacheDir):
		for file in files:
			jsonFile = os.path.join(dirpath, file)
			fileAge = datetime.date.today() - datetime.date.fromtimestamp(os.path.getmtime(jsonFile))
			if (fileAge.days > 0):
				with open(jsonFile, encoding='utf-8') as json_data:
					price = json.load(json_data)["price"]
					if (price > maxPrice):
						maxPrice = price
						maxPriceFile = jsonFile

	if (maxPriceFile is not None):
		os.remove(maxPriceFile)

def initCache(collection):
	if (args.currency == 'czk'):
		if (smartFlush):
			smartFlushCache()

		lastLength = 0
		count = 1

		for card in collection:

			statusLine = 'Fetching najada price for (' + str(count) + '/' + str(len(collection)) + ', ...' + str(collection[card].sourceFile)[-50:-2]  + '): ' + card + " ..."

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
		fileAge = datetime.date.today() - datetime.date.fromtimestamp(os.path.getmtime(jsonFile))

		if (clearCache == 'always' or (clearCache == 'timeout' and fileAge.days > cacheTimeout) or (clearCache == 'price' and fileAge.days > 1)):
			price = fetchCardPriceMark(card, jsonFile)
		else:
			with open(jsonFile, encoding='utf-8') as json_data:
				price = json.load(json_data)["price"]

	else:

		price = fetchCardPriceMark(card, jsonFile)

	if (price is None):
		price = 0

	return float(price)

def fetchCardPriceMark(card, jsonFile):

	response = fetchCardPrice(card)

	if (response is not None):
		with open(jsonFile, 'w') as f:
			json.dump({"price": response, "name": card.name}, f)
	else:
		print(console.CRED +  "Price not found for '" + card.name + "' card at Najada." + console.CEND)

	price = response

	return price

def fetchCardPrice(card, cheapestPrice = None):

	name = card.name

	#?Anchor=&RedirUrl=https%3A%2F%2Fwww.najada.cz%2Fcz%2Fkusovky-mtg%2F&Search=Gempalm+Polluter&Sender=Submit&MagicCardSet=-1#

	response = requests.post(baseUrl, data={
		'Anchor': 'EShopSearchArticles', 
		'RedirUrl': baseUrl, 
		'Search': name, 
		'Sender': 'Submit',
		'MagicCardSet': '-1' }, params={
		'Anchor': 'EShopSearchArticles', 
		'RedirUrl': baseUrl, 
		'Search': name, 
		'Sender': 'Submit',
		'MagicCardSet': '-1' })

	regexPrice = '<span class="v">([0-9]+)</span>'

	regexName = '<td class="tdTitle">(.*?)</td>'

	prices = re.findall(regexPrice, response.text)

	names = re.findall(regexName, response.text, flags=re.DOTALL) 

	prevName = None

	cleanHtml = re.compile('<.*?>')

	for name, price in zip(names, prices):

		name = re.sub(cleanHtml, '', name).strip()

		if (name == '&nbsp;'):
			name = prevName
		else:
			prevName = name

		price = int(price)

		if ((cheapestPrice == None or cheapestPrice > price) and name.lower() == card.getProp('name').lower()):
			cheapestPrice = price

	return cheapestPrice