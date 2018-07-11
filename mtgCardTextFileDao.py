import re
import os

import mtgCardInCollectionObject

def readCardFile(cardFile, cards):
	with open(cardFile, 'r') as f:
		lineCounter = 0
		for line in f:
			lineCounter += 1
			line = line.strip()
			if (line.lower().startswith("sideboard")):
				print ("Sideboard seaparator?")
				# has sideboard separator - it is likely a deck.
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
					name = re.sub(" \[[A-Z0-9][A-Z0-9][A-Z0-9]\]\Z", "", name, 1) # strip set tag from end i.e. [AKH]
					name = re.sub(" \([CURM]\)\Z", "", name, 1) # strip rarity from end i.e. (R)
					name = re.sub(" \([0-9]+\)\Z", "", name, 1) # strip collector number, etc...
					name = name.strip()
					if (name in cards):
						cards[name].add(count, cardFile)
#						print ("Duplicate card ", name, " merged" , count)
					else:
						cards[name] = mtgCardInCollectionObject.CardInCollection(name, count, cardFile)
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
			file.write(currencyToGlyph(mtgCardInCollectionObject.CardInCollection.args.currency))
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
				readCardFile(cardFile, cards)
			else:
				print ("Ignoring file '", cardFile, "'")