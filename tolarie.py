import re

import requests

from priceSource import PriceSource


class Tolarie(PriceSource):

    def __init__(self, clearCache, cacheTimeout, smartFlush, priority):
        self.clearCache = clearCache
        self.cacheTimeout = cacheTimeout
        self.smartFlush = smartFlush
        self.sourceName = 'Tolarie'
        self.supportedCurrency = 'czk'
        self.cacheDir = '.tolarieCache'
        self.priority = priority
        self.baseUrl = "https://tolarie.cz/koupit_karty/"

    def fetchCardPrice(self, card, page=0, cheapestPrice=None):

        response = requests.get(self.baseUrl, params={
            'name': card.name,
            'stored': 'on', 'o': 'price_order', 'od': 'a'})

        start = response.text.find('<table class="kusovky">')
        end = response.text.find('</table>', start + 1)

        regexRow = 'class="product_name">(.+?)</'

        names = re.findall(regexRow, response.text[start:end])

        regexRow = '(?:<td class="td_price">\\s*<span class="product_price">([0-9]+) Kč</span>\\s*</td>)|(?:<td class="td_price">\\s*</td>)'

        prices = re.findall(regexRow, response.text[start:end], flags=re.DOTALL)

        for name, price in zip(names, prices):

            if price != '':

                name = name.replace('&#39;', '\'')
                name = name.split('(')[0].strip()
                name = name.split('#')[0].strip()

                price = int(price)

                if (cheapestPrice is None or cheapestPrice > price) and name.lower() == card.name.lower():
                    cheapestPrice = price

        return cheapestPrice
