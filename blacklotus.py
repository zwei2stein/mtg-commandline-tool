import re

import requests

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
        self.baseUrl = "https://www.blacklotus.cz/vyhledavani/"

    def fetchCardPrice(self, card, page=0, cheapestPrice=None):

        name = card.name

        response = requests.get(self.baseUrl, params={
            'string': name})

        start = response.text.find('<div id="products-found" class="search-results">')
        end = response.text.find('<footer id="footer">', start + 1)

        regex_row = '<span data-micro="name">\n(.+?)</span>'

        regex_prices = 'data-micro-price="([0-9.]+)"'

        names = re.findall(regex_row, response.text[start:end], re.MULTILINE)

        prices = re.findall(regex_prices, response.text[start:end], re.MULTILINE)

        for name, price in zip(names, prices):

            name = name.split(' // ')[0]
            name = name.strip()

            ends = [' - RELEASE FOIL SP', ' - RELEASE FOIL', ' - NON ENG ITA', ' - NON ENG SPA',
                    ' - FOIL ZENDIKAR EXPEDITIONS', ' - FTV FOIL', ' - NON ENG RUS', ' - NON ENG JAP',
                    ' - NON ENG GER SP', ' - NON ENG GER', ' - NON ENG CHI SP', ' - NON ENG CHI', ' - FOIL NON-ENG CHI',
                    ' - FOIL', ' - HP', ' - SP',
                    ' - PRERELEASE FOIL', ' - PRERELEASE PROMO', ' - PRERELEASE PROMO FOIL', ' - PROMO FOIL',
                    ' - GAMEDAY FOIL', ' - FNM FOIL', 'PDS FOIL', ' FOIL']

            for end in ends:
                name = name[::-1].replace(end[::-1], '', 1)[::-1]

            price = float(price)

            if cheapestPrice is None or cheapestPrice > price and name.lower() == card.name.lower():
                cheapestPrice = price

        return cheapestPrice
