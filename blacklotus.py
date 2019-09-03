from decimal import *
import base64
import re
import requests

import datetime

from priceSource import PriceSource

class BlackLotus(PriceSource):

	def __init__(self, clearCache, cacheTimeout, smartFlush, priority):
		self.clearCache = clearCache
		self.cacheTimeout = cacheTimeout
		self.smartFlush = smartFlush
		self.sourceName = 'Black Lotus'
		self.supportedCurrency = 'czk'
		self.cacheDir = '.blackLotusCache'
		self.priority = priority
		self.baseUrl = "http://www.blacklotus.cz/magic-vyhledavani/"

	def fetchCardPrice(self, card, page = 0, cheapestPrice = None):

		search = base64.b64encode(bytes('nazev;' + card.name + ';popis;;15;0;4;0;7;0;from13;;to13;;from14;;to14;;from12;;to12;;pricemin;;pricemax;;6;0', encoding = 'utf-8'))

		response = requests.get(self.baseUrl, params={
			'page': 'search', 
			'search': search, 
			'catid': 3,
			'sortmode': 7,
			'depmode': 1,
			'pageno': page + 1})

		start = response.text.find('<tbody>')
		end = response.text.find('</tbody>', start + 1)
		
		regexRow = 'title="(.+?)">.+?</a></h2></td><td class="cenasdph">([0-9,]+)&nbsp;'

		names = re.findall(regexRow, response.text[start:end]) 

		for name, price in names:

			name = name.split(' // ')[0]
			name = name.strip()

			ends = [' - RELEASE FOIL SP', ' - RELEASE FOIL', ' - NON ENG ITA', ' - NON ENG SPA', ' - FOIL ZENDIKAR EXPEDITIONS', ' - FTV FOIL', ' - NON ENG RUS', ' - NON ENG JAP', ' - NON ENG GER SP', ' - NON ENG GER', ' - NON ENG CHI SP', ' - NON ENG CHI', ' - FOIL NON-ENG CHI', ' - FOIL', ' - HP', ' - SP',
				' - PRERELEASE FOIL', ' - PRERELEASE PROMO', ' - PRERELEASE PROMO FOIL', ' - PROMO FOIL', ' - GAMEDAY FOIL', ' - FNM FOIL', 'PDS FOIL', ' FOIL']
 
			for end in ends:
				name = name[::-1].replace(end[::-1], '', 1)[::-1]

			price = float(price.replace(',', '.'))

			if ((cheapestPrice == None or cheapestPrice > price) and name.lower() == card.getProp('name').lower()):
				cheapestPrice = price

		return cheapestPrice