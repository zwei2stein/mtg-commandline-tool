import argparse

import mtgCardTextFileDao
import mtgCardInCollectionObject
import deckAutocomplete

import listTokens
import verifyDeck
import deckPrice
import manaCurve
import manaSymbols
import landMana

import mtgCardTextFileDao

def locateCard(card, libraryCards):
	if libraryCards[card] is not None:
		print(libraryCards[card].name)	
		for file in libraryCards[card].sourceFile:
			print(file)		

def main():

	parser = argparse.ArgumentParser(description='Process MTG card lists (decks and collection)')
	parser.add_argument('-id', '--ignoreDecks', action='store_const', const='deck', default=None, help='Ignore files with \'deck\' in path')
	parser.add_argument('-c', '--currency', choices=['eur', 'usd', 'tix'], default='eur', help='Currency used for sorting by price and for output of price. Default \'eur\'')

	parser.add_argument('-pp', '--printPrice', action='store_true', help='Add price to output')
	parser.add_argument('-pc', '--printColor', action='store_true', help='Add color identity to output')
	parser.add_argument('-s', '--sort', nargs='*', choices=['price', 'cmc', 'name', 'count', 'color'], default=[], help='Sort list order by. Default \'name\'')
	parser.add_argument('-fl', '--filterLegality', choices=['standard', 'future', 'frontier', 'modern', 'legacy', 'pauper', 'vintage', 'penny', 'commander', '1v1', 'duel', 'brawl'], default=None, help='Filter result list by format legality. Default is no filter.')
	parser.add_argument('-ft', '--filterType', default=None, help='Filter results by type line of card')

	parser.add_argument('-d', '--deck', help='Sets deck file to work on', type=str, required=False)

	parser.add_argument('-vd', '--verifyDeck', action='store_true', help='Prints cards missing from given deck file')
	parser.add_argument('-lt', '--listTokens', action='store_true', help='Prints tokens for given deck file')
	parser.add_argument('-dp', '--deckPrice', action='store_true', help='Prints price of given deck file')
	parser.add_argument('-mc', '--manaCurve', action='store_true', help='Prints mana curve of given deck file')
	parser.add_argument('-ms', '--manaSymbols', action='store_true', help='Prints mana symbols count of given deck file')
	parser.add_argument('-lm', '--landMana', action='store_true', help='Prints land mana count of given deck file')

	parser.add_argument('-lc', '--locateCard', help='Prints file(s) in which card is located', type=str, required=False)
	parser.add_argument('-sl', '--saveList', help='Save consolidates list', type=str, required=False)

	parser.add_argument('-collection', '--collection', help='Sets root directory to scan for card collection. Default is current directory.', type=str, default='.', required=False)

	args = parser.parse_args()

	mtgCardInCollectionObject.CardInCollection.args = args

#	deckAutocomplete.deckAutocomplete("./meta/")

	cardCollection = {}
	if (args.verifyDeck or args.locateCard is not None or args.saveList is not None):
		mtgCardTextFileDao.readCardDirectory(args.collection, cardCollection, args.ignoreDecks)

	deck = {}
	if (args.deckPrice or args.verifyDeck or args.listTokens or args.manaCurve or args.manaSymbols or args.landMana):
		deck = mtgCardTextFileDao.readCardFile(args.deck, {}, True)

	if (args.verifyDeck):
		print('Verifying deck cards in collection:')
		verifyDeck.verifyDeck(deck, cardCollection, args.printPrice, args.currency)
	if (args.listTokens):
		print('Listing tokens for deck:')
		listTokens.listTokens(deck)
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
		deckPrice.deckPrice(deck, args.currency)
	if (args.locateCard is not None):
		locateCard(args.locateCard, cardCollection)
	if (args.saveList is not None):
		mtgCardTextFileDao.saveCardFile(args.saveList, cardCollection)

main()