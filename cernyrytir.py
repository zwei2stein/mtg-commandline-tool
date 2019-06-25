import re
import requests

from priceSource import PriceSource

class CernyRytir(PriceSource):

	def __init__(self, clearCache, cacheTimeout, smartFlush, priority):
		self.clearCache = clearCache
		self.cacheTimeout = cacheTimeout
		self.smartFlush = smartFlush
		self.sourceName = 'Cerny Rytir'
		self.supportedCurrency = 'czk'
		self.cacheDir = '.cernyRytirCache'
		self.priority = priority
		self.baseUrl = "http://cernyrytir.cz/index.php3"

	def fetchCardPrice(self, card, page = 0, cheapestPrice = None):
		pageSize = 30

		# URL will not accept encoded ', it needs non-UTF8 ´
		name = card.getProp('name').replace('\'', '´').replace('\"', '„').encode("Windows-1252", "ignore")

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

			if ((cheapestPrice == None or cheapestPrice > price) and name.lower() == card.getProp('name').lower()):
				cheapestPrice = price

		if (len(names) == pageSize and 'Nalezeno' in response.text):
			sys.stdout.write('.')
			sys.stdout.flush()
			return self.fetchCardPrice(card, page = page + 1, cheapestPrice = cheapestPrice)
		else:

			return cheapestPrice