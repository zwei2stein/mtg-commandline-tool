import hashlib

from mtgCardTextFileDao import readDeckDirectory
from mtgDeckObject import Deck
from web_infra.database import DeckDao


class DeckManager:

    def __init__(self, deck_dao: DeckDao, deck_home, configuration):
        self.deck_dao = deck_dao
        self.deckHome = deck_home
        self.configuration = configuration

    @staticmethod
    def hash_deck(deck: Deck):
        salt = "$!K;g.}yDdeg\"Q5J".encode('utf-8')
        return hashlib.sha256(deck.file.encode() + salt).hexdigest()

    def init_decks(self, context):
        print('Inititializing deck database')
        decks = readDeckDirectory(self.deckHome, dict(), self.configuration["filePattern"], context)
        for file in decks:
            deck = Deck(decks[file], file)
            deck.deck_hash = self.hash_deck(deck)
            self.deck_dao.add_deck(deck)
        print('Done init, have', self.deck_dao.deck_count(), 'decks')

    def get_deck(self, deck_hash, context):
        deck = self.deck_dao.get_deck(deck_hash, context)
        if deck is None:
            self.init_decks(context)
            deck = self.deck_dao.get_deck(deck_hash, context)
        return deck

    def get_decks(self, context):
        if self.deck_dao.deck_count() == 0:
            self.init_decks(context)
        return self.deck_dao.get_deck_list(context)

    def get_all_cards(self, context):
        if self.deck_dao.card_count() == 0:
            self.init_decks(context)
        return self.deck_dao.get_all_cards(context)
