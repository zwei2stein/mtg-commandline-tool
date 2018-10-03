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

import mtgCardTextFileDao

def main():

	confoguration = {}
	with open(os.path.dirname(sys.argv[0]) + '/config.json') as json_data_file:
		configuration = json.load(json_data_file)

	parser = argparse.ArgumentParser(description='Process MTG card plain text lists (decks and collection)', epilog='version: 0.1')

	parser.add_argument('-cd', '--collectionDirectory', help='Sets root directory to scan for card collection. Default is \'' + configuration["collectionDirectory"] + '\' directory.', type=str, default=configuration["collectionDirectory"] , required=False)
	parser.add_argument('-id', '--ignoreDecks', action='store_const', const='deck', default=None, help='Ignore files with \'deck\' in path')
	parser.add_argument('-c', '--currency', choices=['eur', 'usd', 'tix'], default=configuration["defaultCurrency"], help='Currency used for sorting by price and for output of price. Default \'' + configuration["defaultCurrency"] + '\'')

	parser.add_argument('-sl', '--saveList', help='Save consolidated list', type=str, required=False)

	parser.add_argument('-pp', '--printPrice', action='store_true', help='Add price to output')
	parser.add_argument('-pc', '--printColor', action='store_true', help='Add color identity to output')
	parser.add_argument('-s', '--sort', nargs='*', choices=['price', 'cmc', 'name', 'count', 'color'], default=[], help='Sort list order by. Default \'name\'')
	parser.add_argument('-fl', '--filterLegality', choices=['standard', 'future', 'frontier', 'modern', 'legacy', 'pauper', 'vintage', 'penny', 'commander', '1v1', 'duel', 'brawl'], default=None, help='Filter result list by format legality. Default is no filter.')
	parser.add_argument('-ft', '--filterType', default=None, help='Filter results by type line of card')

	parser.add_argument('-d', '--deck', help='Sets deck file to work on, required for deck tools', type=str, required=False)

	parser.add_argument('-vd', '--verifyDeck', action='store_true', help='Prints cards missing from given deck file')
	parser.add_argument('-lt', '--listTokens', action='store_true', help='Prints tokens and counters for given deck file')
	parser.add_argument('-dp', '--deckPrice', action='store_true', help='Prints price of given deck file')
	parser.add_argument('-mc', '--manaCurve', action='store_true', help='Prints mana curve of given deck file')
	parser.add_argument('-ms', '--manaSymbols', action='store_true', help='Prints mana symbols count in casting costs of given deck file')
	parser.add_argument('-lm', '--landMana', action='store_true', help='Prints mana source count of given deck file')
	parser.add_argument('-cc', '--cardCount', action='store_true', help='Gives total couunt of cards for deck')
	parser.add_argument('-is', '--isSingleton', action='store_true', help='Checks deck if it is singeton')
	parser.add_argument('-df', '--deckFormat', action='store_true', help='Prints formats in which is deck legal')
	parser.add_argument('-nd', '--nameDeck', action='store_true', help='Attempts to generate name for given deck')

	args = parser.parse_args()

	mtgCardInCollectionObject.CardInCollection.args = args

#	deckAutocomplete.deckAutocomplete("./meta/")

	cardCollection = {}
	if (args.verifyDeck or args.saveList is not None):
		mtgCardTextFileDao.readCardDirectory(args.collectionDirectory, cardCollection, args.ignoreDecks)

	deck = {}
	if (args.deckPrice or args.verifyDeck or args.listTokens or args.manaCurve or args.manaSymbols or args.landMana or args.nameDeck or args.cardCount or args.isSingleton or args.deckFormat):
		deck = mtgCardTextFileDao.readCardFileFromPath(args.deck, {}, True)

	if (args.verifyDeck):
		print('Verifying deck cards in collection:')
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
	if (args.saveList is not None):
		mtgCardTextFileDao.saveCardFile(args.saveList, cardCollection)

main()