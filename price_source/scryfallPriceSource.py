import scryfall

from price_source.priceSource import PriceSource


class ScryfallPriceSource(PriceSource):

    def __init__(self, base_cache_dir, supportedCurrency, clearCache, cacheTimeout, smartFlush, priority):
        super().__init__(base_cache_dir, '.scryfallPriceCache' + supportedCurrency)
        self.clearCache = clearCache
        self.cacheTimeout = cacheTimeout
        self.smartFlush = smartFlush
        self.sourceName = 'Scryfall'
        self.supportedCurrency = supportedCurrency
        self.priority = priority

    def fetch_card_price(self, card, page=0, cheapestPrice=None):

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
