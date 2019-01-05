import scryfall
import mtgColors
import sets
import util

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

	def __init__(self, name, count, sourceFile, jsonData = None, sideboard = False):
		self.name = name
		self.count = count
		if (sideboard):
			self.sideboard = count
		else:
			self.sideboard = 0
		self.sourceFile = []
		self.sourceFile.append(sourceFile)
		self._jsonData = jsonData

	def add(self, count, sourceFile, sideboard = False):
		self.count += count
		if (sideboard):
			self.sideboard += count
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
		if (propName == 'cmc'):
			return self.jsonData["cmc"]
		if (propName == 'price'):
			return float(self.jsonData.get(CardInCollection.args.currency, "0.0"))
		if (propName == 'count'):
			return self.count
		if (propName == 'name'):
			return self.name
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