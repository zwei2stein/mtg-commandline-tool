from decimal import *

from najada import Najada
from cernyrytir import CernyRytir
from blacklotus import BlackLotus
from scryfallPriceSource import ScryfallPriceSource
from priceSource import PriceNotFoundException
from priceSource import SourceUnreachableException
from tolarie import Tolarie
from mysticshop import MysticShop

import console
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
	if (configuration["mysticshop"]["enabled"]):
		handlers.append(MysticShop(clearCache, configuration["mysticshop"]["cacheTimeout"], configuration["mysticshop"]["smartFlush"], configuration["mysticshop"]["priority"]))

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
			except SourceUnreachableException as e:
				errors.append(handler.sourceName + ' is unreachable')
	if (priceSourceCount > 0):
		return Decimal(price / priceSourceCount).quantize(Decimal('.01'), rounding=ROUND_UP)
	else:
		return Decimal(0)

	print(errors)

def apparise(currency, cardObject):
	global handlers

	prices = {}

	minKey = []
	minPrice = None

	maxKey = []
	maxPrice = None

	for handler in handlers:
		if (handler.getSupportedCurrency() == currency):
			try:
				prices[handler.sourceName] = handler.getCardPrice(cardObject)

				if (minPrice is None):
					minKey.append(handler.sourceName)
					minPrice = prices[handler.sourceName]
				elif (minPrice == prices[handler.sourceName]):
					minKey.append(handler.sourceName)
				elif (minPrice > prices[handler.sourceName]):
					minKey = []
					minKey.append(handler.sourceName)
					minPrice = prices[handler.sourceName]

				if (maxPrice is None):
					maxKey.append(handler.sourceName)
					maxPrice = prices[handler.sourceName]
				elif (maxPrice == prices[handler.sourceName]):
					maxKey.append(handler.sourceName)
				elif (maxPrice < prices[handler.sourceName]):
					maxKey = []
					maxKey.append(handler.sourceName)
					maxPrice = prices[handler.sourceName]

			except PriceNotFoundException as e:
				errors.append('Price for ' + cardObject.name + ' not found at ' + handler.sourceName)
			except SourceUnreachableException as e:
				errors.append(handler.sourceName + ' is unreachable')

	response = {}
	response['min'] = minKey
	response['max'] = maxKey
	response['card'] = cardObject
	response['prices'] = prices 
	response['errors'] = errors
	response["currency"] = currency
	
	return response

def printApparise(response):

	for source in response['prices']:

		prefix = ''
		sufix = ''

		if (source in response['max']):
			prefix = console.CRED
			sufix = console.CEND
		if (source in response['min']):
			prefix = console.CGREEN
			sufix = console.CEND

		print(prefix + source + ' ' + str(response['prices'][source]) + util.currencyToGlyph(response["currency"]) + sufix)

	for error in response['errors']: 
		print (console.CRED + error + console.CEND)

def stringApparise(response):

	res = ''

	first = True

	for source in response['prices']:

		prefix = ''
		sufix = ''

		if (source in response['max']):
			prefix = console.CRED
			sufix = console.CEND
		if (source in response['min']):
			prefix = console.CGREEN
			sufix = console.CEND

		if (not first):
			res = res + ', '
		else:
			first = False

		res =  res + prefix + source + ': ' + str(response['prices'][source]) + util.currencyToGlyph(response["currency"]) + sufix

	return res

def stringMinPrices(response):

	res = ''

	first = True

	for source in sorted(response['min']):

		if (not first):
			res = res + ', '
		else:
			first = False

		res = res + source

	return res
	