import re
import requests

import util

from price_source.priceSource import PriceSource

class CernyRytir(PriceSource):

	def __init__(self, base_cache_dir, clearCache, cacheTimeout, smartFlush, priority):
		super().__init__(base_cache_dir, '.cernyRytirCache')
		self.clearCache = clearCache
		self.cacheTimeout = cacheTimeout
		self.smartFlush = smartFlush
		self.sourceName = 'Cerny Rytir'
		self.supportedCurrency = 'czk'
		self.priority = priority
		self.baseUrl = "http://cernyrytir.cz/index.php3"

	def fetch_card_price(self, card, page = 0, cheapestPrice = None):
		pageSize = 30

		# URL will not accept encoded ', it needs non-UTF8 ´
		name = card.name.replace('\'', '´').replace('\"', '„').encode("Windows-1252", "ignore")

		response = requests.post(self.baseUrl, data={'searchname': name, 'searchtype': 'card', 'akce': '3', 'limit': page * pageSize}, params={'searchname': name, 'searchtype': 'card', 'akce': '3', 'limit': page * pageSize})

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

			if ((cheapestPrice == None or cheapestPrice > price) and name.lower() == card.name.lower()):
				cheapestPrice = price

		if (len(names) == pageSize and 'Nalezeno' in response.text):
			util.printProgress(page)
			return self.fetch_card_price(card, page =page + 1, cheapestPrice = cheapestPrice)
		else:

			return cheapestPrice