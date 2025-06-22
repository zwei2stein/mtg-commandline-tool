prettyPrintGroups = ['shortType']
prettyPrintSort = ['shortType', 'name']


class Deck:

    def __init__(self, cards, file):
        self.cards = cards
        self.file = file
        self.deck_hash = None

    def getCommander(self):
        return {k: v for (k, v) in self.cards.items() if v.getProp('commander')}

    def getSideboard(self):
        return {k: v for (k, v) in self.cards.items() if (v.getProp('sideboard') and not v.getProp('commander'))}

    def getMainboard(self):
        return {k: v for (k, v) in self.cards.items() if (v.getProp('mainboard') and not v.getProp('commander'))}

    def getByShortType(self, shortType):
        return {k: v for (k, v) in self.cards.items() if
                (v.getProp('shortType') == shortType and v.getProp('mainboard') and not v.getProp('commander'))}

    def getShortTypes(self):
        shortTypes = set()

        for key, card in self.cards.items():
            shortTypes.add(card.getProp('shortType'))

        return shortTypes

    def simple_card_list(self):
        return self.cards.values()

    def getAverageEDHrecRank(self):
        count = 0
        rankSum = 0
        for deckCardName, deckCard in self.cards.items():
            if deckCard.jsonData.get("edhrec_rank", None):
                count = count + deckCard.count
                rankSum = rankSum + deckCard.jsonData["edhrec_rank"] * deckCard.count
        if count == 0:
            return 0
        else:
            return int(rankSum / count)
