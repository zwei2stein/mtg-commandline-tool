from najada import Najada
from cernyrytir import CernyRytir
from scryfallPriceSource import ScryfallPriceSource

handlers = []

def initPriceSource(clearCache, configuration):
	global handlers
	handlers = []
	if (configuration["najada"]["enabled"]):
		handlers.append(Najada(clearCache, configuration["najada"]["cacheTimeout"], configuration["najada"]["smartFlush"], configuration["najada"]["priority"]))
	if (configuration["cernyrytir"]["enabled"]):
		handlers.append(CernyRytir(clearCache, configuration["cernyrytir"]["cacheTimeout"], configuration["cernyrytir"]["smartFlush"], configuration["cernyrytir"]["priority"]))

	handlers.append(ScryfallPriceSource('tix'))
	handlers.append(ScryfallPriceSource('usd'))
	handlers.append(ScryfallPriceSource('eur'))

	handlers = sorted(handlers, key=lambda handler: handler.getPriority())

def getSupportedCurrencies():
	return ['usd', 'eur', 'tix', 'czk']

def flushCache():
	global handlers
	for handler in handlers:
		handler.flushCache()

def initCache(decksToInit):
	global handlers
	for handler in handlers:
		handler.initCache(decksToInit)

def getCardPrice(currency, cardObject):
	global handlers
	price = 0
	priceSourceCount = 0
	for handler in handlers:
		if (handler.getSupportedCurrency() == currency):
			addedPrice = handler.getCardPrice(cardObject)
			if (addedPrice > 0):
				price = price + addedPrice
				priceSourceCount = priceSourceCount + 1
	if (priceSourceCount > 0):
		return price / priceSourceCount
	else:
		return 0