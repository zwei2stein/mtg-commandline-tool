from decimal import *

from najada import Najada
from cernyrytir import CernyRytir
from blacklotus import BlackLotus
from scryfallPriceSource import ScryfallPriceSource
from priceSource import PriceNotFoundException
from tolarie import Tolarie

import util

handlers = []

errors = []

def initPriceSource(clearCache, configuration):
	global handlers
	handlers = []
	if (configuration["najada"]["enabled"]):
		handlers.append(Najada(clearCache, configuration["najada"]["cacheTimeout"], configuration["najada"]["smartFlush"], configuration["najada"]["priority"]))
	if (configuration["cernyrytir"]["enabled"]):
		handlers.append(CernyRytir(clearCache, configuration["cernyrytir"]["cacheTimeout"], configuration["cernyrytir"]["smartFlush"], configuration["cernyrytir"]["priority"]))
	if (configuration["blacklotus"]["enabled"]):
		handlers.append(BlackLotus(clearCache, configuration["blacklotus"]["cacheTimeout"], configuration["blacklotus"]["smartFlush"], configuration["blacklotus"]["priority"]))
	if (configuration["tolarie"]["enabled"]):
		handlers.append(Tolarie(clearCache, configuration["tolarie"]["cacheTimeout"], configuration["tolarie"]["smartFlush"], configuration["tolarie"]["priority"]))

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
	price = Decimal(0)
	priceSourceCount = 0
	for handler in handlers:
		if (handler.getSupportedCurrency() == currency):
			try:
				addedPrice = handler.getCardPrice(cardObject)
				if (addedPrice > 0):
					price += Decimal(addedPrice)
					priceSourceCount = priceSourceCount + 1
			except PriceNotFoundException as e:
				errors.append('Price for ' + cardObject.name + ' not found at ' + handler.sourceName )
	if (priceSourceCount > 0):
		return Decimal(price / priceSourceCount).quantize(Decimal('.01'), rounding=ROUND_UP)
	else:
		return Decimal(0)

	print(errors)

def apparise(cardObject, currency):
	global handlers

	prices = {}

	for handler in handlers:
		if (handler.getSupportedCurrency() == currency):
			try:
				prices[handler.sourceName] = handler.getCardPrice(cardObject)
			except PriceNotFoundException as e:
				errors.append('Price for ' + cardObject.name + ' not found at ' + handler.sourceName )

	response = {}
	response['card'] = cardObject
	response['prices'] = prices 
	response['errors'] = errors
	response["currency"] = currency
	
	return response

def printApparise(response):

	for source in response['prices']:
		print(source + ' ' + str(response['prices'][source]), util.currencyToGlyph(response["currency"]))

	for error in response['errors']: 
		print (error)
