import scryfall
import priceSourceHandler

import mtgColors
import sets
import util

cardProps = ['price', 'fullPrices', 'cheapestPriceSource', 'cmc', 'name', 'count', 'color', 'set', 'type', 'shortType', 'rarity']

rarityOrder = {
	'common' : 0,
	'uncommon' : 1,
	'rare' : 2,
	'mythic' : 3
}

shortTypeOrder = {
	'Creature' : 1,
	'Planeswalker' : 2,
	'Instant' : 3,
	'Sorcery' : 4,
	'Enchantment' : 5,
	'Artifact' : 6,
	'Land' : 7
}

def getRarityOrder(rarity):
	return rarityOrder[rarity]

def getShortTypeOrder(shortType):
	return shortTypeOrder[shortType]

class CardInCollection:

	args = None

	def __init__(self, name, count, sourceFile, jsonData = None, sideboard = 0, commander = False):
		self.name = name
		self.count = count
		self.sideboard = sideboard
		self.commander = commander
		self.sourceFile = []
		self.sourceFile.append(sourceFile)
		self._jsonData = jsonData
		self.propCache = {}

	def add(self, count, sourceFile, sideboard = 0, commander = False):
		self.count += count
		self.sideboard += sideboard
		if (commander):
			self.commander = commander
		if (sourceFile is not None):
			self.sourceFile.append(sourceFile)

	@property
	def jsonData(self):
		if self._jsonData is None:
			self._jsonData = scryfall.getCachedCardJson(self)
		return self._jsonData 

	def getDisplaySuffix(self):
		if (CardInCollection.args.print):
			suffix = " #"
			for prop in CardInCollection.args.print:
				suffix = suffix + " " + prop + ": " + str(self.getProp(prop))
				if (prop == "price"):
					suffix = suffix + util.currencyToGlyph(CardInCollection.args.currency)
			return suffix
		else:
			return ""

	def __str__(self):
		return self.name + self.getDisplaySuffix()

	def getProp(self, propName):
		if (propName not in self.propCache):
			self.propCache[propName] = self.getRawProp(propName)
		
		return self.propCache[propName]

	def getRawProp(self, propName):

		if (propName == 'cmc'):
			return self.jsonData["cmc"]
		if (propName == 'price'):
			return float(priceSourceHandler.getCardPrice(CardInCollection.args.currency, self))
		if (propName == 'fullPrices'):
			return priceSourceHandler.stringApparise(priceSourceHandler.apparise(CardInCollection.args.currency, self))
		if (propName == 'cheapestPriceSource'):
			return priceSourceHandler.stringMinPrices(priceSourceHandler.apparise(CardInCollection.args.currency, self))
		if (propName == 'count'):
			return self.count
		if (propName == 'name'):
			if (self.jsonData.get('card_faces', None) is not None):
				return self.jsonData['card_faces'][0]['name']
			else:
				return self.jsonData['name']
		if (propName == 'color'):
			return mtgColors.colorIdentity2String(self.jsonData['color_identity'])
		if (propName == 'set'):
			return self.jsonData["set"]
		if (propName == 'sideboard'):
			return self.sideboard > 0
		if (propName == 'mainboard'):
			return (self.count - self.sideboard) > 0
		if (propName == 'type'):
			return self.jsonData.get('type_line','').split("\u2014", 1)[0].strip()
		if (propName == 'shortType'):
			return self.jsonData.get('type_line','').split("\u2014", 1)[0].strip().split(" ")[-1]
		if (propName == 'rarity'):
			return self.jsonData["rarity"]
		if (propName == 'commander'):
			return self.commander

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

		for sort in CardInCollection.args.sort:
			if (sort == 'color'):
				if (self.jsonData['color_identity'] != cardInCollection.jsonData['color_identity']):
					return mtgColors.compareColors(self.jsonData['color_identity'], cardInCollection.jsonData['color_identity'])

			if (sort == 'rarity'):
				if (self.jsonData["rarity"] != cardInCollection.jsonData["rarity"]):
					return getRarityOrder(self.jsonData["rarity"]) > getRarityOrder(cardInCollection.jsonData["rarity"])

			if (sort == 'shortType'):
				if (self.getProp('shortType') != cardInCollection.getProp('shortType')):
					return getShortTypeOrder(self.getProp('shortType')) > getShortTypeOrder(cardInCollection.getProp('shortType'))

			if (sort == 'set'):
				if (self.jsonData["set"] != cardInCollection.jsonData["set"]):
					return sets.getSetOrder(self.jsonData["set"]) > sets.getSetOrder(cardInCollection.jsonData["set"])

			if (self.getProp(sort) != cardInCollection.getProp(sort)):
				return self.getProp(sort) > cardInCollection.getProp(sort)
			
		
		# Default sort by name:

		return self.name > cardInCollection.name