import scryfall

from priceSource import PriceSource

class ScryfallPriceSource(PriceSource):

	def __init__(self, supportedCurrency):
		self.sourceName = 'Scryfall'
		self.supportedCurrency = supportedCurrency
		self.priority = 5

	def getCardPrice(self, card):
		price = card.jsonData['prices'].get(self.supportedCurrency, "0.0")
		if (price is None):
			price = card.jsonData['prices'].get(self.supportedCurrency + '_foil', "0.0")
		if (price is None):
			price = 0
		return float(price)

	def flushCache(self):
		pass

	def initCache(self, decksToInit):
		pass