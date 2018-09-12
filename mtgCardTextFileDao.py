import re
import os

import mtgCardInCollectionObject

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
		elif (line != ""):
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
				name = re.sub(" \[[A-Z0-9][A-Z0-9][A-Z0-9]\]\Z", "", name, 1) # strip set tag from end i.e. [AKH]
				name = re.sub(" \([CURM]\)\Z", "", name, 1) # strip rarity from end i.e. (R)
				name = re.sub(" \([0-9]+\)\Z", "", name, 1) # strip collector number, etc...
				name = name.strip()
				if (name in cards):
					cards[name].add(count, cardFile, isSideboard)
				else:
					cards[name] = mtgCardInCollectionObject.CardInCollection(name, count, cardFile, None, isSideboard)
	return cards

def saveCardFile(cardFile, cards):
	print("Saving", cardFile) 
	file = open(cardFile, 'w') 
	for card in sorted(cards, key=cards.__getitem__):

		if (mtgCardInCollectionObject.CardInCollection.args.filterLegality is not None):
			if (cards[card].jsonData['legalities'][args.filterLegality] != 'legal'):
				continue

		if (mtgCardInCollectionObject.CardInCollection.args.filterType is not None):
			if (not (mtgCardInCollectionObject.CardInCollection.args.filterType in cards[card].jsonData['type_line'])):
				continue

		file.write(str(cards[card]))
		if (mtgCardInCollectionObject.CardInCollection.args.printPrice):
			file.write(" ")
			file.write(cards[card].jsonData.get(mtgCardInCollectionObject.CardInCollection.args.currency, "0.0"))
			file.write(util.currencyToGlyph(mtgCardInCollectionObject.CardInCollection.args.currency))
		if (mtgCardInCollectionObject.CardInCollection.args.printColor):
			file.write(" ")
			file.write(mtgColors.colorIdentity2String(cards[card].jsonData['color_identity']))
		file.write('\n')
	file.close()
	print ('Saved file ' + cardFile)

def readCardDirectory(path, cards, ignoreDecks):
	print ("Reading directory ", path)
	for root, dirs, files in os.walk(path):
		for file in files:
			cardFile = os.path.join(root, file)
			if (cardFile.endswith(".txt") and (ignoreDecks is None or ignoreDecks not in cardFile.lower())):
				print ("Reading file '", cardFile, "'")
				readCardFileFromPath(cardFile, cards)
			else:
				print ("Ignoring file '", cardFile, "'")