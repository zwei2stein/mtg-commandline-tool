import scryfall

from priceSource import PriceSource


class ScryfallPriceSource(PriceSource):

    def __init__(self, supportedCurrency, clearCache, cacheTimeout, smartFlush, priority):
        self.clearCache = clearCache
        self.cacheTimeout = cacheTimeout
        self.smartFlush = smartFlush
        self.sourceName = 'Scryfall'
        self.supportedCurrency = supportedCurrency
        self.cacheDir = '.scryfallPriceCache' + self.supportedCurrency
        self.priority = priority

    def fetchCardPrice(self, card, page=0, cheapestPrice=None):

        foundCards = scryfall.searchByCard(card)

        minPrice = None

        for uniquePrinting in foundCards:

            price = uniquePrinting['prices'].get(self.supportedCurrency, None)
            if price is None:
                price = uniquePrinting['prices'].get(self.supportedCurrency + '_foil', None)
            if price is None:
                price = None

            if price is not None:
                if minPrice is None:
                    minPrice = float(price)
                else:
                    minPrice = min(minPrice, float(price))

        return minPrice
