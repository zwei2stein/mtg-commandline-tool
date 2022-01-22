import functools
import os
import re
import sys

import console
import mtgCardInCollectionObject
import sets


def readCardFileFromPath(cardFile, cards, asDeck=False, context={}):
    with open(cardFile, 'r') as f:
        return readCardFile(f, cardFile, cards, asDeck, context)


def readCardFile(f, cardFile, cards, asDeck, context):
    isSideboard = False
    errorCount = 0
    lineCounter = 0
    isCommander = False
    for line in f:
        lineCounter += 1
        #		print (lineCounter, isSideboard)
        line = line.strip()
        if (line.lower().startswith("sideboard") or line.startswith("// Sideboard") or line.startswith(
                "// Outside the Game")):
            if (asDeck):
                #				print ("Sideboard found ", lineCounter)
                isSideboard = True
        elif (line.lower().startswith("commander") or line.startswith("// Commander")):
            if (asDeck):
                #				print ("Commander found")
                isCommander = True
        elif (line != "" and not (line.startswith("#") or line.startswith("TOTAL:"))):
            #				print ("'"+line+"'")
            splitLine = line.split(" ", 1)
            if (len(splitLine) == 2):
                count = 0
                try:
                    count = int(re.sub("[x]\Z", "", splitLine[0], 1))  # acceptable 1 and 1x
                except ValueError:
                    if errorCount == 0:
                        print()
                    errorCount += 1
                    print("Card list format error " + str(errorCount) + " in file '" + cardFile + "', line " + str(
                        lineCounter) + ", ignoring '" + line + "'")
                    continue
                name = splitLine[1]
                if '#' in name:
                    commentedName = name.split('#')
                    name = commentedName[0]
                # print ("comment", commentedName[1:])
                if ' / ' in name:
                    name = re.sub(' / ', ' // ', name, 1)

                setName = None

                match = re.search(" \[([A-Z0-9]{3,5})\]\Z", name)
                if (match):
                    setName = match.string[match.start(1):match.end(1)].lower()

                name = re.sub(" \[[A-Za-z0-9]{3,5}\]\Z", "", name, 1)  # strip set tag from end i.e. [AKH]
                name = re.sub(" \([CURM]\)\Z", "", name, 1)  # strip rarity from end i.e. (R)
                name = re.sub(" - Full Art", "", name, 1)  # strip full card notice
                name = re.sub(" \([0-9]+\)\Z", "", name, 1)  # strip collector number, etc...
                name = re.sub(" \([0-9A-Za-z ]+\)\Z", "", name,
                              1)  # strip showcase marker, artist marker, other markers
                name = name.strip()
                # Normalize name from scryfall data.
                # Multifaced cards that are here normalized to name of first face.
                # In case there are mixed namings in files (common for pathways)
                temporaryCard = mtgCardInCollectionObject.CardInCollection(name, count, cardFile)
                name = temporaryCard.getJsonName()

                sideboardCount = 0
                if (isSideboard):
                    sideboardCount = count
                if (name in cards):
                    cards[name].add(count, cardFile, sideboardCount, isCommander, setName)
                else:
                    cards[name] = mtgCardInCollectionObject.CardInCollection(name, count, cardFile,
                                                                             temporaryCard.jsonData,
                                                                             sideboardCount, isCommander, setName, {},
                                                                             context)
                isCommander = False
    return cards


def saveCardFile(file, cards, sorts, context, diffFormat=False, color=None):
    hasSideboard = functools.reduce((lambda x, v: x or v.getProp('sideboard')), cards.values(), False)

    hasCommander = functools.reduce((lambda x, v: x or v.getProp('commander')), cards.values(), False)

    if (hasCommander):
        file.write('\n')
        saveCardFileSlice(file, {k: v for (k, v) in cards.items() if v.getProp('commander')}, [], diffFormat, context,
                          prependTextToCardLine='Commander:\n',
                          color=color)
        file.write('\n')
        file.write('# Main deck:')
        file.write('\n')
    if (hasSideboard):
        saveCardFileSlice(file,
                          {k: v for (k, v) in cards.items() if (v.getProp('mainboard') and not v.getProp('commander'))},
                          sorts, diffFormat, context, sideboard=False, color=color)
        file.write('\n')
        file.write('Sideboard:')
        file.write('\n')
        saveCardFileSlice(file,
                          {k: v for (k, v) in cards.items() if (v.getProp('sideboard') and not v.getProp('commander'))},
                          sorts, diffFormat, context, sideboard=True, color=color)
    else:
        saveCardFileSlice(file, {k: v for (k, v) in cards.items() if not v.getProp('commander')}, sorts, diffFormat,
                          context, color=color)


def saveCardFileSlice(file, cards, sorts, diffFormat, context, sideboard=False, prependTextToCardLine=None, color=None):
    lastGroup = {}

    for sort in sorts:
        lastGroup[sort] = None

    for card in sorted(cards, key=cards.__getitem__):

        groupReset = False

        for sort in sorts:
            if (groupReset):
                lastGroup[sort] = None

            if (lastGroup[sort] is None or lastGroup[sort] != cards[card].getProp(sort)):
                file.write('\n')
                file.write("# ")
                if (len(sorts) > 1):
                    file.write(sort.capitalize())
                    file.write(" - ")
                if (sort == 'set'):
                    file.write(sets.get_set_name(cards[card].getProp(sort)))
                else:
                    file.write(str(cards[card].getProp(sort)))
                file.write(':\n')

                lastGroup[sort] = cards[card].getProp(sort)
                groupReset = True

        if (context.filterLegality is not None):
            if (cards[card].jsonData['legalities'][context.filterLegality] != 'legal'):
                continue

        if (context.filterType is not None):
            if (not (context.filterType in cards[card].jsonData['type_line'])):
                continue

        printCard(file, cards[card], sideboard, diffFormat, prependTextToCardLine=prependTextToCardLine, color=color)


def printCard(file, card, sideboard, diffFormat, prependTextToCardLine=None, color=None):
    count = 0
    if (sideboard):
        if (card.count < card.sideboard):
            count = card.sideboard - card.count
        else:
            count = card.sideboard
    else:
        count = card.count - card.sideboard

    if prependTextToCardLine is not None:
        file.write(prependTextToCardLine)

    if (diffFormat):
        for x in range(count):
            printCardLine(file, 1, card)
    else:
        printCardLine(file, count, card, color=color)


def printCardLine(file, count, card, color=None):
    file.write(str(count))
    file.write(" ")
    if (color is not None):
        file.write(color)
    file.write(card.getProp('fullName'))
    if (color is not None):
        file.write(console.CEND)
    file.write(card.getDisplaySuffix())
    file.write('\n')


def readCardDirectory(path, cards, ignoreDecks, cardListfilePattern, context):
    if (os.path.isfile(path)):
        print("Reading single file '", path, "'")
        readCardFileFromPath(path, cards, asDeck=True, context=context)
    elif (os.path.isdir(path)):
        print("Reading directory ", path)

        lastLength = 0
        count = 1

        for root, dirs, files in os.walk(path):
            for file in files:
                cardFile = os.path.join(root, file)
                match = re.search(cardListfilePattern, cardFile)
                if (match and (ignoreDecks is None or ignoreDecks not in cardFile.lower())):
                    statusLine = "Reading file #" + str(count) + " '" + cardFile + "'..."

                    count += 1
                    currentLength = len(statusLine)
                    if (currentLength < lastLength):
                        statusLine = statusLine + (lastLength - currentLength) * ' '
                    lastLength = currentLength

                    sys.stdout.write('\r' + statusLine)
                    sys.stdout.flush()
                    readCardFileFromPath(cardFile, cards, asDeck=False, context=context)
                else:
                    print("Ignoring file '", cardFile, "'")
        doneMessage = "Done reading '" + path + "'"
        sys.stdout.write('\r' + doneMessage + (lastLength - len(doneMessage)) * " " + '\n')
        sys.stdout.flush()
    else:
        print("'" + path + "' is not a file or directory.")

    return cards


def readDeckDirectory(path, decks, cardListfilePattern, context):
    if (os.path.isfile(path)):
        print("Reading single file '", path, "'")
        decks[path] = readCardFileFromPath(path, {}, asDeck=True, context=context)
    elif (os.path.isdir(path)):
        print("Reading directory ", path)

        lastLength = 0
        count = 1

        for root, dirs, files in os.walk(path):
            for file in files:
                cardFile = os.path.join(root, file)
                match = re.search(cardListfilePattern, cardFile)
                if (match):
                    if sys.stdin and sys.stdin.isatty():
                        statusLine = "Reading file #" + str(count) + " '" + cardFile + "'..."

                        currentLength = len(statusLine)
                        if (currentLength < lastLength):
                            statusLine = statusLine + (lastLength - currentLength) * ' '
                        lastLength = currentLength

                        sys.stdout.write('\r' + statusLine)
                        sys.stdout.flush()

                    decks[cardFile] = readCardFileFromPath(cardFile, {}, asDeck=True, context=context)
                else:
                    print("Ignoring file '", cardFile, "'")

        doneMessage = "Done reading '" + path + "'"
        sys.stdout.write('\r' + doneMessage + (lastLength - len(doneMessage)) * " " + '\n')
        sys.stdout.flush()
    else:
        print("'" + os.path.abspath(path) + "' is not a file or directory.")

    return decks
