import re
import os
import sys
import functools

import mtgCardInCollectionObject
import mtgColors

import util

def readCardFileFromPath(cardFile, cards, asDeck=False):
	with open(cardFile, 'r') as f:
		return readCardFile(f, cardFile, cards, asDeck)

def readCardFile(f, cardFile, cards, asDeck):

	isSideboard = False

	lineCounter = 0
	for line in f:
		lineCounter += 1
		line = line.strip()
		if (line.lower().startswith("sideboard")):
			if (asDeck):
				print ("Sideboard found")
				isSideboard = True
		elif (line != "" and not line.lower().startswith("#")):
#				print ("'"+line+"'")
			splitLine = line.split(" ", 1)
			if (len(splitLine) == 2):
				count = 0
				try:
					count = int(re.sub("[x]\Z", "", splitLine[0], 1)) # acceptable 1 and 1x
				except ValueError:
					print ("Bad line format in file '" + cardFile + "', line " + str(lineCounter) + ", ignoring '" + line + "'")
					continue
				name = splitLine[1]
				if ('#' in name):
					commentedName = name.split('#')
					name = commentedName[0]
					print ("comment", commentedName[1:])
				name = re.sub(" \[[A-Z0-9]{3,4}\]\Z", "", name, 1) # strip set tag from end i.e. [AKH]
				name = re.sub(" \([CURM]\)\Z", "", name, 1) # strip rarity from end i.e. (R)
				name = re.sub(" \([0-9]+\)\Z", "", name, 1) # strip collector number, etc...
				name = name.strip()
				if (name in cards):
					cards[name].add(count, cardFile, isSideboard)
				else:
					cards[name] = mtgCardInCollectionObject.CardInCollection(name, count, cardFile, None, isSideboard)
	return cards

def saveCardFile(file, cards, sorts, diffFormat=False):

	hasSideboard = functools.reduce((lambda x, v: x or v.getProp('sideboard')), cards.values(), False)

	if (hasSideboard):
		saveCardFileSlice(file, {k:v for (k,v) in cards.items() if v.getProp('mainboard')}, sorts, diffFormat, sideboard = False)
		file.write('\n')
		file.write('Sideboard:')
		file.write('\n')
		saveCardFileSlice(file, {k:v for (k,v) in cards.items() if v.getProp('sideboard')}, sorts, diffFormat, sideboard = True)
	else:
		saveCardFileSlice(file, cards, sorts, diffFormat)

def saveCardFileSlice(file, cards, sorts, diffFormat, sideboard = False):

	lastGroup = {}
	
	for sort in sorts:
		lastGroup[sort] = None

	for card in sorted(cards, key=cards.__getitem__):

		groupReset = False

		for sort in sorts:
			if (groupReset):
				lastGroup[sort] = None

			if (lastGroup[sort] == None or lastGroup[sort] != cards[card].getProp(sort)):
				file.write('\n')
				file.write("# ")
				if (len(sorts) > 1):
					file.write(sort.capitalize())
					file.write(" - ")
				file.write(str(cards[card].getProp(sort)))
				file.write(':\n')

				lastGroup[sort] = cards[card].getProp(sort)
				groupReset = True

		if (mtgCardInCollectionObject.CardInCollection.args.filterLegality is not None):
			if (cards[card].jsonData['legalities'][args.filterLegality] != 'legal'):
				continue

		if (mtgCardInCollectionObject.CardInCollection.args.filterType is not None):
			if (not (mtgCardInCollectionObject.CardInCollection.args.filterType in cards[card].jsonData['type_line'])):
				continue

		printCard(file, cards[card], sideboard, diffFormat)



def printCard(file, card, sideboard, diffFormat):

	count = 0
	if (sideboard):
		count = card.sideboard
	else:
		count = card.count - card.sideboard

	if (diffFormat):
		for x in range(count):
			printCardLine(file, 1, card)	
	else:
		printCardLine(file, count, card)

def printCardLine(file, count, card):
	file.write(str(count))
	file.write(" ")
	file.write(str(card))
	if (mtgCardInCollectionObject.CardInCollection.args.printPrice):
		file.write("# ")
		file.write(card.jsonData.get(mtgCardInCollectionObject.CardInCollection.args.currency, "0.0"))
		file.write(util.currencyToGlyph(mtgCardInCollectionObject.CardInCollection.args.currency))
	if (mtgCardInCollectionObject.CardInCollection.args.printColor):
		file.write("# ")
		file.write(mtgColors.colorIdentity2String(card.jsonData['color_identity']))
	file.write('\n')

def readCardDirectory(path, cards, ignoreDecks, cardListfilePattern):
	if (os.path.isfile(path)):
		print ("Reading signle file '", path, "'")
		readCardFileFromPath(path, cards, asDeck=True)
	elif (os.path.isdir(path)):
		print ("Reading directory ", path)
		for root, dirs, files in os.walk(path):
			for file in files:
				cardFile = os.path.join(root, file)
				match = re.search(cardListfilePattern, cardFile)
				if (match and (ignoreDecks is None or ignoreDecks not in cardFile.lower())):
					print ("Reading file '", cardFile, "'")
					readCardFileFromPath(cardFile, cards)
				else:
					print ("Ignoring file '", cardFile, "'")
	else:
		print ("'" + path + "' is not a file or directory.")