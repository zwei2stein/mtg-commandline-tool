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
	for handler in handlers:
		if (handler.getSupportedCurrency() == currency):
			price = handler.getCardPrice(cardObject)
			if (price > 0):
				return price
	return 0