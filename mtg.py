import argparse
import json
import os
import sys
from http import HTTPStatus

import mtgCardTextFileDao
import mtgCardInCollectionObject
import mtgDeckObject
#import deckAutocomplete

import listTokens
import verifyDeck
import deckPrice
import manaCurve
import manaSymbols
import landMana
import nameDeck
import deckStatistics
import deckFormat
import deckCreatureTypes
import drawCards
import deckDiff
import search

import scryfall

import priceSourceHandler

def main():

	configuration = {}
	with open(os.path.dirname(sys.argv[0]) + '/config.json') as json_data_file:
		configuration = json.load(json_data_file)

	parser = argparse.ArgumentParser(description='Process MTG card plain text lists (decks and collection)', epilog='version: 0.1')

	parser.add_argument('-cd', '--collectionDirectory', help='Sets root directory to scan for card collection. Default is \'' + configuration["collectionDirectory"] + '\' directory. Single file representing collection can be specified instead of directory.', type=str, default=configuration["collectionDirectory"] , required=False)
	parser.add_argument('-id', '--ignoreDecks', action='store_const', const='deck', default=None, help='Ignore files with \'deck\' in path. Usefull when you store decks along with your collection.')
	parser.add_argument('-fp', '--filePattern', type=str, default=configuration["filePattern"], help='Regular expression pattern for files that are considered part of collection. Default is \'' + configuration["filePattern"] + '\'')
	parser.add_argument('-c', '--currency', choices=priceSourceHandler.getSupportedCurrencies(), default=configuration["defaultCurrency"], help='Currency used for sorting by price and for output of price. Default \'' + configuration["defaultCurrency"] + '\'')
	parser.add_argument('-pt', '--priceThreshold', type=int, help='When calculating total sum of prices of cards, cards will be included only if their price is higher than value of this parameter.')

	parser.add_argument('-cache', '--cache', choices=['init', 'flush', 'auto'], default=configuration["defaultCache"], help='Manual cache control: \'init\' fetches all cards from collectin from scryfall to cache, \'flush\' clears cache directory, \'auto\' does nothing.')

	parser.add_argument('-clearCache', '--clearCache', choices=['awlays', 'price', 'timeout', 'none'], default=configuration["scryfall"]["clearCache"],
			help='Determines how is caching from scrycall handled. \'always\' - always fetch fresh data. \'price\' - fetch data if price changes. \'timeout\' - fetch data if ' + str(configuration["scryfall"]["cacheTimeout"]) + ' days have passed. \'none\' - always use cached version. Default \''  +configuration["scryfall"]["clearCache"] + '\'')

	group = parser.add_mutually_exclusive_group(required = True)
	group.add_argument('-sl', '--saveList', help='Save consolidated collection or print it to \'console\'', type=str)
	group.add_argument('-d', '--deck', help='Chooses deck file to work on, required for deck tools. If directory is specified, tool will work on each deck file found in directory', type=str)
	group.add_argument('-search', '--search', default=None, type=str, help='Search your collection with scryfall. Use scryfall search string')
	group.add_argument('-apr', '--appraise', default=None, type=str, help='Print price of card in all sources in given currency')


	parser.add_argument('-p', '--print', nargs='*',choices=mtgCardInCollectionObject.cardProps, default=[], help='Add given atributes to card printout')
	parser.add_argument('-s', '--sort', nargs='*', choices=mtgCardInCollectionObject.cardProps, default=[], help='Sort list order by. Default \'name\'.')
	parser.add_argument('-g', '--group', nargs='*', choices=mtgCardInCollectionObject.cardProps, default=[], help='Group saved list by given parameter. Always groups sideboards together.')
	parser.add_argument('-fl', '--filterLegality', choices=deckFormat.formatList, default=None, help='Filter result list by format legality. Default is no filter.')
	parser.add_argument('-ft', '--filterType', default=None, help='Filter results by type line of card')

	parser.add_argument('-mc', '--missingCards', action='store_true', help='Prints cards missing from given deck file')
	parser.add_argument('-lt', '--listTokens', action='store_true', help='Prints tokens and counters for given deck file')
	parser.add_argument('-pp', '--printPretty', action='store_true', help='Prints neatly formated deck for given deck file')
	parser.add_argument('-dp', '--deckPrice', action='store_true', help='Prints price of given deck file')
	parser.add_argument('-mcu', '--manaCurve', action='store_true', help='Prints mana curve of given deck file')
	parser.add_argument('-ms', '--manaSymbols', action='store_true', help='Prints mana symbols count in casting costs of given deck file')
	parser.add_argument('-lm', '--landMana', action='store_true', help='Prints mana source count of given deck file')
	parser.add_argument('-cc', '--cardCount', action='store_true', help='Gives total count of cards for deck')
	parser.add_argument('-is', '--isSingleton', action='store_true', help='Checks deck if it is singeton')

	parser.add_argument('-df', '--deckFormat', action='store_true', help='Prints formats in which is deck legal')
	parser.add_argument('-dfi', '--deckFormatInspect', choices=deckFormat.formatList, default=None, help='Show detailed information about why deck does not meet format criteria.')

	parser.add_argument('-ct', '--deckCreatureTypes', action='store_true', help='Prints list of creature types in deck with their counts (not including possible tokens)')
	parser.add_argument('-draw', '--drawCards', default=None, help='Draw N cards from deck.', type=int)
	parser.add_argument('-nd', '--nameDeck', action='store_true', help='Attempts to generate name for given deck')

	parser.add_argument('-diff', '--diff', help='Difference of deck with another deck.', type=str)
	parser.add_argument('-update', '--update', '-upgrade', '--upgrade', help='New deck list to be updated into', type=str)


	args = parser.parse_args()

	if (args.group):
		if (args.sort):
			args.sort = args.group + args.sort
		else:
			args.sort = args.group

	scryfall.clearCache = args.clearCache
	scryfall.cacheTimeout = configuration["scryfall"]["cacheTimeout"]

	priceSourceHandler.initPriceSource(args.clearCache, configuration["priceSources"])

	cardCollection = {}
	if ((args.missingCards is not None or args.update is not None or args.saveList is not None or args.search is not None) or args.cache == 'init'):
		mtgCardTextFileDao.readCardDirectory(args.collectionDirectory, cardCollection, args.ignoreDecks, args.filePattern, args)

	decks = {}
	if (args.deckPrice or args.missingCards or args.update or args.listTokens or args.manaCurve or args.manaSymbols or args.landMana or args.nameDeck or args.cardCount or args.isSingleton or args.deckFormat or args.deckFormatInspect or args.deckCreatureTypes or args.drawCards or args.diff or args.printPretty):
		decks = mtgCardTextFileDao.readDeckDirectory(args.deck, decks, args.filePattern, args)

	ready = True

	if (args.cache):
		if (args.cache == 'flush'):
			scryfall.flushCache()
			priceSourceHandler.flushCache()
		if (args.cache == 'init'):
			cardsToInitCache = {}
			cardsToInitCache.update(cardCollection)
			decksToInit = {}
			for file in decks:
				decksToInit.update(decks[file])
			cardsToInitCache.update(decksToInit)
			try:
				scryfall.initCache(cardsToInitCache)
			except scryfall.CardRetrievalError as e:
				if (e.errorCode == 404):
					print ("Card " + e.cardName + " not found on scryfall, aborting.")
				elif (e.errorCode >= 500):
					print ("Scryfall server error " + str(e.errorCode) + " - " + HTTPStatus(e.errorCode).phrase + " for card " + e.cardName + ", aborting.")
				else:
					print ("Unexpected error " + str(e.errorCode) + " - " + HTTPStatus(e.errorCode).phrase + " for card " + e.cardName + ", aborting.")
				ready = False
			priceSourceHandler.initCache(decksToInit)
			if (args.appraise is not None):
				appraiseCards = {}
				appraiseCards[args.appraise] = mtgCardInCollectionObject.CardInCollection(args.appraise, 1, None, None, 0, False, None, None, args)
				priceSourceHandler.initCache(appraiseCards)

	if (ready):

		for file in decks:
			print (file + ":")
			deck = decks[file]

			if (args.missingCards):
				verifyDeck.printMissingCardsToConsole(verifyDeck.missingCards(deck, cardCollection, args.currency, None, args.priceThreshold), args)
			if (args.update):
				deck2 = mtgCardTextFileDao.readCardFileFromPath(args.update, {}, True, args)
				verifyDeck.printMissingCardsToConsole(verifyDeck.missingCards(deck, cardCollection, args.currency, deck2, args.priceThreshold), args)
			if (args.listTokens):
				listTokens.printTokensToConsole(listTokens.listTokens(deck))
			if (args.manaCurve):
				manaCurve.printManaCurveToConsole(manaCurve.manaCurve(deck))
			if (args.manaSymbols):
				manaSymbols.printManaSymbolsToConsole(manaSymbols.manaSymbols(deck))
			if (args.landMana):
				landMana.printLandManaToConsole(landMana.landMana(deck))
			if (args.deckPrice):
				deckPrice.printPricesToConsole(deckPrice.deckPrice(deck, args.currency, args.priceThreshold))
			if (args.isSingleton):
				deckStatistics.printgetIsDeckSingletonToConsole(deckStatistics.getIsDeckSingleton(deck))
			if (args.cardCount):
				deckStatistics.printGetDeckCardCountToConsole(deckStatistics.getDeckCardCount(deck))
			if (args.deckFormat or args.deckFormatInspect):
				deckFormat.printDetDeckFormatToConsole(deckFormat.getDeckFormat(deck, args.deckFormatInspect), only_inspect= not args.deckFormat)
			if (args.nameDeck):
				nameDeck.printnDeckNameToConsole(nameDeck.nameDeck(deck))
			if (args.deckCreatureTypes):
				deckCreatureTypes.printnGetCreatureTypes(deckCreatureTypes.getCreatureTypes(deck))
			if (args.drawCards):
				drawCards.printDrawCardsToConsole(drawCards.drawCards(deck, args.drawCards), args)
			if (args.diff):
				deck2 = mtgCardTextFileDao.readCardFileFromPath(args.diff, {}, True, args)
				deckDiff.diff(deck, deck2, args)
			if (args.printPretty):
				originalSorts = args.sort
				args.sort = mtgDeckObject.prettyPrintSort
				formatedFileName = file + ".formated.txt"
				formatedFile = open(formatedFileName, 'w')
				mtgCardTextFileDao.saveCardFile(formatedFile, deck, mtgDeckObject.prettyPrintGroups, args)
				formatedFile.close()
				print ("Saved", formatedFileName)
				args.sort = originalSorts

		if (args.saveList is not None):
			if (args.saveList == 'console'):
				mtgCardTextFileDao.saveCardFile(sys.stdout, cardCollection, args.group, args)
			else:
				print ("Saving", args.saveList)
				savedFile = open(args.saveList, 'w')
				mtgCardTextFileDao.saveCardFile(savedFile, cardCollection, args.group, args)
				savedFile.close()
				print ('Saved file ' + args.saveList)

		if (args.search is not None):
			search.search(args.search, cardCollection, args)

		if (args.appraise is not None):
			priceSourceHandler.printApparise(priceSourceHandler.apparise(args.currency, mtgCardInCollectionObject.CardInCollection(args.appraise, 1, None, None, 0, False, None, None, args)))

main()