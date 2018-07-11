import scryfall

class CardInCollection:

	args = None

	def __init__(self, name, count, sourceFile, jsonData = None):
		self.name = name
		self.count = count
		self.sourceFile = []
		self.sourceFile.append(sourceFile)
		self._jsonData = jsonData

	def add(self, count, sourceFile):
		self.count += count
		self.sourceFile.append(sourceFile)

	@property
	def jsonData(self):
		if self._jsonData is None:
			self._jsonData = scryfall.getCachedCardJson(self)
		return self._jsonData 

	def __str__(self):
		return str(self.count) + " " + self.name #+ " " + self.jsonData["mana_cost"]

	def __gt__(self, cardInCollection):

		for sort in CardInCollection.args.sort:
			if (sort == 'cmc'):
				if (self.jsonData["cmc"] != cardInCollection.jsonData["cmc"]):
					return self.jsonData["cmc"] > cardInCollection.jsonData["cmc"]
			if (sort == 'price'):
				if (float(self.jsonData.get(CardInCollection.args.currency, "0.0")) != float(cardInCollection.jsonData.get(CardInCollection.args.currency, "0.0"))):
					return float(self.jsonData.get(CardInCollection.args.currency, "0.0")) > float(cardInCollection.jsonData.get(CardInCollection.args.currency, "0.0"))
			if (sort == 'count'):
				if (self.count != cardInCollection.count):
					return self.count > cardInCollection.count
			if (sort == 'name'):
				if (self.name != cardInCollection.name):
					return self.name > cardInCollection.name
			if (sort == 'color'):
				if (self.jsonData['color_identity'] != cardInCollection.jsonData['color_identity']):
					return mtgColors.compareColors(self.jsonData['color_identity'], cardInCollection.jsonData['color_identity'])
		#default
		return self.name > cardInCollection.name