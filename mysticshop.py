import re
import requests

import util

from priceSource import PriceSource

class MysticShop(PriceSource):

	def __init__(self, clearCache, cacheTimeout, smartFlush, priority):
		self.clearCache = clearCache
		self.cacheTimeout = cacheTimeout
		self.smartFlush = smartFlush
		self.sourceName = 'Mystic Shop'
		self.supportedCurrency = 'czk'
		self.cacheDir = '.mysticShopCache'
		self.priority = priority
		self.baseUrl = "http://mysticshop.cz/mtgshop.php"

	def fetchCardPrice(self, card, page = 0, cheapestPrice = None):

		response = requests.post(self.baseUrl, params={
			'name': card.name,
			'limit': 500,
			'p': page + 1})

		start = response.text.find('<tbody>')
		end = response.text.find('</tbody>', start + 1)
		
		regexRow = '<td class="detail"><b>(.+?)</b>'

		names = re.findall(regexRow, response.text[start:end]) 

		regexRow = '<td class="price2">([0-9]+),-</td>'

		prices = re.findall(regexRow, response.text[start:end]) 

		for name, price in zip(names, prices):

			price = int(price)

			if ((cheapestPrice == None or cheapestPrice > price) and name.lower() == card.name.lower()):
				cheapestPrice = price

		return cheapestPrice