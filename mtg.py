import argparse
import json
import os
import sys

import mtgCardTextFileDao
import mtgCardInCollectionObject
import deckAutocomplete

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

import scryfall

def main():

	configuration = {}
	with open(os.path.dirname(sys.argv[0]) + '/config.json') as json_data_file:
		configuration = json.load(json_data_file)

	parser = argparse.ArgumentParser(description='Process MTG card plain text lists (decks and collection)', epilog='version: 0.1')

	parser.add_argument('-cd', '--collectionDirectory', help='Sets root directory to scan for card collection. Default is \'' + configuration["collectionDirectory"] + '\' directory. Single file representing collection can be specified instead of directory.', type=str, default=configuration["collectionDirectory"] , required=False)
	parser.add_argument('-id', '--ignoreDecks', action='store_const', const='deck', default=None, help='Ignore files with \'deck\' in path. Usefull when you store decks along with your collection.')
	parser.add_argument('-fp', '--filePattern', type=str, default=configuration["filePattern"], help='Regular expression pattern for files that are considered part of collection. Default is \'' + configuration["filePattern"] + '\'')
	parser.add_argument('-c', '--currency', choices=['eur', 'usd', 'tix'], default=configuration["defaultCurrency"], help='Currency used for sorting by price and for output of price. Default \'' + configuration["defaultCurrency"] + '\'')

	parser.add_argument('-cache', '--cache', choices=['init', 'flush'], default=[], help='Manual cache control: \'init\' fetches all cards from collectin from scryfall to cache, \'flush\' clears cache directory.')

	parser.add_argument('-clearCache', '--clearCache', choices=['awlays', '4price', 'timeout', 'none'], default=configuration["scryfall"]["clearCache"],
			help='Determines how is caching from scrycall handled. \'always\' - always fetch fresh data. \'price\' - fetch data if price changes. \'timeout\' - fetch data if ' + str(configuration["scryfall"]["cacheTimeout"]) + ' days have passed. \'none\' - always use cached version. Default \''  +configuration["scryfall"]["clearCache"] + '\'')

	group = parser.add_mutually_exclusive_group(required = True)
	group.add_argument('-sl', '--saveList', help='Save consolidated list or print it to \'console\'', type=str)
	group.add_argument('-d', '--deck', help='Chooses deck file to work on, required for deck tools. If directory is specified, tool will work on each deck file found in directory', type=str)

	parser.add_argument('-pp', '--printPrice', action='store_true', help='Add price to output')
	parser.add_argument('-pc', '--printColor', action='store_true', help='Add color identity to output')
	parser.add_argument('-s', '--sort', nargs='*', choices=['price', 'cmc', 'name', 'count', 'color', 'set', 'type', 'shortType', 'rarity'], default=[], help='Sort list order by. Default \'name\'.')
	parser.add_argument('-g', '--group', nargs='*', choices=['price', 'cmc', 'name', 'count', 'color', 'set', 'type', 'shortType', 'rarity'], default=[], help='Group saved list by given parameter. Always groups sideboards together.')
	parser.add_argument('-fl', '--filterLegality', choices=['standard', 'future', 'frontier', 'modern', 'legacy', 'pauper', 'vintage', 'penny', 'commander', '1v1', 'duel', 'brawl'], default=None, help='Filter result list by format legality. Default is no filter.')
	parser.add_argument('-ft', '--filterType', default=None, help='Filter results by type line of card')

	parser.add_argument('-mc', '--missingCards', action='store_true', help='Prints cards missing from given deck file')
	parser.add_argument('-lt', '--listTokens', action='store_true', help='Prints tokens and counters for given deck file')
	parser.add_argument('-dp', '--deckPrice', action='store_true', help='Prints price of given deck file')
	parser.add_argument('-mcu', '--manaCurve', action='store_true', help='Prints mana curve of given deck file')
	parser.add_argument('-ms', '--manaSymbols', action='store_true', help='Prints mana symbols count in casting costs of given deck file')
	parser.add_argument('-lm', '--landMana', action='store_true', help='Prints mana source count of given deck file')
	parser.add_argument('-cc', '--cardCount', action='store_true', help='Gives total count of cards for deck')
	parser.add_argument('-is', '--isSingleton', action='store_true', help='Checks deck if it is singeton')
	parser.add_argument('-df', '--deckFormat', action='store_true', help='Prints formats in which is deck legal')
	parser.add_argument('-ct', '--deckCreatureTypes', action='store_true', help='Prints list of creature types in deck with their counts (not including possible tokens)')
	parser.add_argument('-draw', '--drawCards', default=None, help='Draw N cards from deck.', type=int)	
	parser.add_argument('-nd', '--nameDeck', action='store_true', help='Attempts to generate name for given deck')

	parser.add_argument('-diff', '--diff', help='Diffe deck with another deck.', type=str)

	args = parser.parse_args()

	if (args.group):
		if (args.sort):
			args.sort = args.group + args.sort
		else:
			args.sort = args.group


	mtgCardInCollectionObject.CardInCollection.args = args

	scryfall.clearCache = args.clearCache
	scryfall.cacheTimeout = configuration["scryfall"]["cacheTimeout"]

#	deckAutocomplete.deckAutocomplete("./meta/")

	cardCollection = {}
	if ((args.missingCards or args.saveList is not None) or args.cache == 'init'):
		mtgCardTextFileDao.readCardDirectory(args.collectionDirectory, cardCollection, args.ignoreDecks, args.filePattern)
		scryfall.initCache(cardCollection)

	decks = {}
	if (args.deckPrice or args.missingCards or args.listTokens or args.manaCurve or args.manaSymbols or args.landMana or args.nameDeck or args.cardCount or args.isSingleton or args.deckFormat or args.deckCreatureTypes or args.drawCards or args.diff):
		decks = mtgCardTextFileDao.readDeckDirectory(args.deck, decks, args.filePattern)
		for file in decks:
			scryfall.initCache(decks[file])

	if (args.cache):
		if (args.cache == 'flush'):
			scryfall.flushCache()
		if (args.cache == 'init'):
			scryfall.initCache(cardCollection)

	for file in decks:
		print (file + ":")
		deck = decks[file]

		if (args.missingCards):
			verifyDeck.verifyDeck(deck, cardCollection, args.printPrice, args.currency)
		if (args.listTokens):
			print('Listing tokens for deck:')
			listTokens.printTokensToConsole(listTokens.listTokens(deck))
		if (args.manaCurve):
			print('Mana curve for deck:')
			manaCurve.manaCurve(deck)
		if (args.manaSymbols):
			print('Mana symbols for deck:')
			manaSymbols.manaSymbols(deck)
		if (args.landMana):
			print('Mana from lands for deck:')
			landMana.landMana(deck)
		if (args.deckPrice):
			print('Price of deck:')
			deckPrice.printPricesToConsole(deckPrice.deckPrice(deck, args.currency))
		if (args.isSingleton):
			print('Singleton status:')
			deckStatistics.printgetIsDeckSingletonToConsole(deckStatistics.getIsDeckSingleton(deck))
		if (args.cardCount):
			print('Card count:')
			deckStatistics.printGetDeckCardCountToConsole(deckStatistics.getDeckCardCount(deck))
		if (args.deckFormat):
			print('Possible deck formats:')
			deckFormat.printDetDeckFormatToConsole(deckFormat.getDeckFormat(deck))
		if (args.nameDeck):
			nameDeck.printnDeckNameToConsole(nameDeck.nameDeck(deck))
		if (args.deckCreatureTypes):
			deckCreatureTypes.printnGetCreatureTypes(deckCreatureTypes.getCreatureTypes(deck))
		if (args.drawCards):
			drawCards.drawCards(deck, args.drawCards)
		if (args.diff):
			deck2 = mtgCardTextFileDao.readCardFileFromPath(args.diff, {}, True)
			deckDiff.diff(deck, deck2)

	if (args.saveList is not None):
		if (args.saveList == 'console'):
			mtgCardTextFileDao.saveCardFile(sys.stdout, cardCollection, args.group)		
		else:
			print ("Saving", args.saveList)
			file = open(args.saveList, 'w')
			mtgCardTextFileDao.saveCardFile(file, cardCollection, args.group)
			file.close()
			print ('Saved file ' + args.saveList)

main()