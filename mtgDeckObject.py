
prettyPrintGroups = ['shortType']
prettyPrintSort = ['shortType', 'name']

class Deck:

	def __init__(self, cards):
		self.cards = cards

	def getCommander(self):
		return {k:v for (k,v) in self.cards.items() if v.getProp('commander')}

	def getSideboard(self):
		return {k:v for (k,v) in self.cards.items() if (v.getProp('sideboard') and not v.getProp('commander'))}

	def getMainboard(self):
		return {k:v for (k,v) in self.cards.items() if (v.getProp('mainboard') and not v.getProp('commander'))}
