import requests

from price_source.priceSource import PriceSource


class Najada(PriceSource):

    def __init__(self, base_cache_dir, clearCache, cacheTimeout, smartFlush, priority):
        super().__init__(base_cache_dir, '.najadaCache')
        self.clearCache = clearCache
        self.cacheTimeout = cacheTimeout
        self.smartFlush = smartFlush
        self.sourceName = 'Najada'
        self.supportedCurrency = 'czk'
        self.priority = priority
        self.baseUrl = "https://najada.games/api/v1/najada2/catalog/mtg-singles/"

    def fetch_card_price(self, card, page=0, cheapest_price=None):

        name = card.name

        response = requests.get(self.baseUrl,
                                params={
                                    'o': '-price',
                                    'offset': page,
                                    'q': name,
                                    'Sender': 'Submit',
                                    'in_stock': 'true',
                                    'limit': 100,
                                    'category': 4,
                                    'article_price_min': 0,
                                    'article_price_max': 10000000})

        json = response.json()

        for result in json.get('results', []):
            name = result.get('name', result.get('localized_name', ''))
            if name.lower() == card.name.lower():
                for article in result.get('articles', []):
                    price = int(article.get('regular_price_czk', article.get('effective_price_czk', 0.0)))
                    if (cheapest_price is None or cheapest_price > price) and name.lower() == card.name.lower():
                        cheapest_price = price

        return cheapest_price
