import re
import requests

from priceSource import PriceSource

class Najada(PriceSource):

	def __init__(self, clearCache, cacheTimeout, smartFlush, priority):
		self.clearCache = clearCache
		self.cacheTimeout = cacheTimeout
		self.smartFlush = smartFlush
		self.sourceName = 'Najada'
		self.supportedCurrency = 'czk'
		self.cacheDir = '.najadaCache'
		self.priority = priority
		self.baseUrl = "https://www.najada.cz/cz/kusovky-mtg/omezit-500"

	def fetchCardPrice(self, card, page = 0, cheapestPrice = None):

		name = card.name

		response = requests.post(self.baseUrl, data={
			'Anchor': 'EShopSearchArticles', 
			'RedirUrl': self.baseUrl, 
			'Search': name, 
			'Sender': 'Submit',
			'MagicCardSet': '-1' }, params={
			'Anchor': 'EShopSearchArticles', 
			'RedirUrl': self.baseUrl, 
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