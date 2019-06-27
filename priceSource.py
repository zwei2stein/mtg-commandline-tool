import datetime
import json
import os
import shutil
import sys

import console
import util

class PriceSource:

	def getPriority(self):
		return self.priority

	def getSupportedCurrency(self):
		return self.supportedCurrency

	def flushCache(self):
		try:
			shutil.rmtree(self.getCacheDir())
		except OSError as e:
			print ("Error where clearing cache directory at " + self.getCacheDir() + ": %s - %s." % (e.filename, e.strerror))


	def getCacheDir(self):
		baseDir = os.path.join(os.path.dirname(sys.argv[0]), self.cacheDir)
		if (not os.path.exists(baseDir)):
			os.makedirs(baseDir)
		return baseDir

	def smartFlushCache(self):
		# 1) highest price is likely to be most volatile
		# 2) don't redownload on same day.

		cacheDir = self.getCacheDir()

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

	def initCache(self, collection):
		if (self.smartFlush):
			self.smartFlushCache()

		lastLength = 0
		count = 1

		for card in collection:

			statusLine = 'Fetching ' + self.sourceName + ' price for (' + str(count) + '/' + str(len(collection)) + ', ...' + str(collection[card].sourceFile)[-50:-2]  + '): ' + card + " ..."

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

	def getCardPrice(self, card):
		jsonFile = os.path.join(self.getCacheDir(), util.cleanFilename(card) + ".json")

		price = None

		if (os.path.exists(jsonFile)):
			fileAge = datetime.date.today() - datetime.date.fromtimestamp(os.path.getmtime(jsonFile))

			if (self.clearCache == 'always' or (self.clearCache == 'timeout' and fileAge.days > self.cacheTimeout) or (self.clearCache == 'price' and fileAge.days > 1)):
				price = self.fetchCardPriceMark(card, jsonFile)
			else:
				with open(jsonFile, encoding='utf-8') as json_data:
					price = json.load(json_data)["price"]

		else:

			price = self.fetchCardPriceMark(card, jsonFile)

		if (price is None):
			price = 0

		return float(price)

	def fetchCardPriceMark(self, card, jsonFile):

		response = self.fetchCardPrice(card)

		if (response is not None):
			with open(jsonFile, 'w') as f:
				json.dump({"price": response, "name": card.name}, f)
		else:
			print(console.CRED +  "Price not found for '" + card.name + "' card at " + self.sourceName + "." + console.CEND)

		price = response

		return price