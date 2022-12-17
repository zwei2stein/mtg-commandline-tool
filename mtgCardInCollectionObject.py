import mtgColors
from price_source import priceSourceHandler
import scryfall
import sets
import util

cardProps = ['price', 'fullPrices', 'cheapestPriceSource', 'cmc', 'name', 'fullName', 'count', 'color', 'set', 'type', 'shortType',
             'rarity', 'age']

globalCardProps = ['price', 'fullPrices', 'cheapestPriceSource', 'cmc', 'name', 'fullName','color', 'type', 'shortType', 'rarity',
                   'age']

rarityOrder = {
    'common': 0,
    'uncommon': 1,
    'rare': 2,
    'mythic': 3
}

shortTypeOrder = {
    'Creature': 1,
    'Planeswalker': 2,
    'Instant': 3,
    'Sorcery': 4,
    'Enchantment': 5,
    'Artifact': 6,
    'Land': 7
}

globalCache = {}

globalPriceCache = {}


def getRarityOrder(rarity):
    return rarityOrder[rarity]


def getShortTypeOrder(shortType):
    return shortTypeOrder[shortType]


class CardInCollection:

    def __init__(self, name, count, sourceFile, jsonData=None, sideboard=0, commander=False, setName=None,
                 propCache=None, context=None):
        self.techName = name
        self.count = count
        self.sideboard = sideboard
        self.commander = commander
        self.sourceFile = []
        self.sourceFile.append(sourceFile)
        self._jsonData = jsonData
        if (propCache is not None):
            self.propCache = propCache
        else:
            self.propCache = {}
        self.setName = {}
        if (setName is not None):
            self.setName[setName] = count
        self.context = context

    def add(self, count, sourceFile, sideboard=0, commander=False, setName=None):
        self.count += count
        self.sideboard += sideboard
        if (commander):
            self.commander = commander
        if (sourceFile is not None):
            self.sourceFile.append(sourceFile)
        if (setName is not None):
            if (setName in self.setName):
                self.setName[setName] = self.setName[setName] + count
            else:
                self.setName[setName] = count

    @property
    def jsonData(self):
        if self._jsonData is None:
            self._jsonData = scryfall.getCachedCardJson(self)
        return self._jsonData

    @property
    def name(self):
        return self.getJsonName()

    def getJsonName(self):
        if self.jsonData.get('card_faces', None) is not None:
            return self.jsonData['card_faces'][0]['name']
        else:
            return self.jsonData['name']

    def getDisplaySuffix(self):
        if (self.context.print):
            suffix = " #"
            for prop in self.context.print:
                suffix = suffix + " " + prop + ": " + str(self.getProp(prop))
                if (prop == "price"):
                    suffix = suffix + util.currencyToGlyph(self.context.currency)
            return suffix
        else:
            return ""

    def __str__(self):
        return self.name + self.getDisplaySuffix()

    def getProp(self, propName):

        propValue = None

        if propName == 'price':
            if self.name not in globalPriceCache:
                globalPriceCache[self.name] = {}
            if self.context.currency not in globalPriceCache[self.name]:
                globalPriceCache[self.name][self.context.currency] = self.getRawProp(propName)
            propValue = globalPriceCache[self.name][self.context.currency]
        elif propName in globalCardProps:
            if self.name not in globalCache:
                globalCache[self.name] = {}
            if propName not in globalCache[self.name]:
                globalCache[self.name][propName] = self.getRawProp(propName)
            propValue = globalCache[self.name][propName]
        else:
            if propName not in self.propCache:
                self.propCache[propName] = self.getRawProp(propName)
            propValue = self.propCache[propName]

        return propValue

    def getRawProp(self, propName):

        if propName == 'cmc':
            return self.jsonData["cmc"]
        elif propName == 'price':
            return float(priceSourceHandler.getCardPrice(self.context.currency, self))
        elif propName == 'fullPrices':
            return priceSourceHandler.stringApparise(priceSourceHandler.apparise(self.context.currency, self))
        elif propName == 'cheapestPriceSource':
            return priceSourceHandler.stringMinPrices(priceSourceHandler.apparise(self.context.currency, self))
        elif propName == 'count':
            return self.count
        elif propName == 'name':
            self.getJsonName()
        elif propName == 'fullName':
            return self.jsonData["name"]
        elif propName == 'color':
            return mtgColors.colorIdentity2String(self.jsonData['color_identity'])
        elif propName == 'set':
            if (len(self.setName) > 0):
                return max(self.setName, key=self.setName.get)
            else:
                return self.jsonData.get('set', '')
        elif propName == 'sideboard':
            return self.sideboard > 0
        elif propName == 'mainboard':
            return (self.count - self.sideboard) > 0
        elif propName == 'type':
            return self.jsonData.get('type_line', '').split("\u2014", 1)[0].strip()
        elif propName == 'shortType':
            return self.jsonData.get('type_line', '').split("\u2014", 1)[0].strip().split(" ")[-1]
        elif propName == 'rarity':
            return self.jsonData["rarity"]
        elif propName == 'commander':
            return self.commander
        elif propName == 'age':
            cardPrintings = scryfall.searchByCard(self)
            printDates = []
            for cardPrinting in cardPrintings:
                printDates.append(sets.get_set_date(cardPrinting["set"]))
            return min(printDates)

    def getFullOracleText(self):
        oracleText = self.jsonData.get('oracle_text', '')
        for face in self.jsonData.get('card_faces', []):
            oracleText = oracleText + '\n' + face.get('oracle_text', '')

        return oracleText

    def getFullTypeLine(self):
        typeLine = self.jsonData.get('type_line', '')
        for face in self.jsonData.get('card_faces', []):
            typeLine = typeLine + '\n' + face.get('type_line', '')

        return typeLine

    def __gt__(self, cardInCollection):

        for sort in self.context.sort:
            if sort == 'color':
                if (self.jsonData['color_identity'] != cardInCollection.jsonData['color_identity']):
                    return mtgColors.compareColors(self.jsonData['color_identity'],
                                                   cardInCollection.jsonData['color_identity'])

            elif sort == 'rarity':
                if (self.jsonData["rarity"] != cardInCollection.jsonData["rarity"]):
                    return getRarityOrder(self.jsonData["rarity"]) > getRarityOrder(cardInCollection.jsonData["rarity"])

            elif sort == 'shortType':
                if (self.getProp('shortType') != cardInCollection.getProp('shortType')):
                    return getShortTypeOrder(self.getProp('shortType')) > getShortTypeOrder(
                        cardInCollection.getProp('shortType'))

            elif sort == 'set':
                if (self.jsonData["set"] != cardInCollection.jsonData["set"]):
                    return sets.get_set_order(self.jsonData["set"]) > sets.get_set_order(cardInCollection.jsonData["set"])

            if (self.getProp(sort) != cardInCollection.getProp(sort)):
                return self.getProp(sort) > cardInCollection.getProp(sort)

        # Default sort by name:

        return self.name > cardInCollection.name
