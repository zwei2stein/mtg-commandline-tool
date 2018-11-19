import scryfall
import mtgColors

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

	def __str__(self):
		return self.name

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

	def __gt__(self, cardInCollection):

		for sort in CardInCollection.args.sort:
			if (sort != 'color'):
				if (self.getProp(sort) != cardInCollection.getProp(sort)):
					return self.getProp(sort) > cardInCollection.getProp(sort)
			if (sort == 'color'):
				if (self.jsonData['color_identity'] != cardInCollection.jsonData['color_identity']):
					return mtgColors.compareColors(self.jsonData['color_identity'], cardInCollection.jsonData['color_identity'])
		
		# Default sort by name:

		return self.name > cardInCollection.name