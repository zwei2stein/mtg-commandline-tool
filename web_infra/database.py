import sqlite3
import threading

from mtgCardInCollectionObject import CardInCollection
from mtgDeckObject import Deck


class DeckDao:

    def __init__(self):
        self.con = sqlite3.connect(":memory:", check_same_thread=False)
        self.con.row_factory = sqlite3.Row
        self.cur = self.con.cursor()
        self.make_schema()

        self.lock = threading.Lock()

    def make_schema(self):
        self.cur.execute("create table deck (id INTEGER PRIMARY KEY, file VARCHAR, hash VARCHAR)")
        self.cur.execute(
            "create table card (id INTEGER PRIMARY KEY, deck_id INTEGER, name VARCHAR, count INTEGER, sideboard_count INTEGER, is_commander INTEGER)")
        self.con.commit()

    def add_deck(self, deck: Deck):
        with self.lock:
            self.cur.execute('insert into deck (file, hash) values (?, ?)', [deck.file, deck.deck_hash])
            deck_id = self.cur.lastrowid
            for card in deck.simple_card_list():
                self.cur.execute(
                    'insert into card (deck_id, name, count, sideboard_count, is_commander) values (?, ?, ?, ?, ?)',
                    [deck_id, card.getJsonName(), card.count, card.sideboard, card.commander if 1 else 0])
            self.con.commit()

    def get_deck(self, deck_hash, context):
        with self.lock:
            deck = self.cur.execute('select id, file, hash from deck where hash=?', [deck_hash]).fetchone()
            if deck is not None:
                return Deck(self.get_deck_cards(deck['id'], context), deck['file'])
            else:
                return None

    def get_deck_list(self, context):
        decks = []
        with self.lock:
            for deck in self.cur.execute('select id, file, hash from deck').fetchall():
                decks.append(Deck(self.get_deck_cards(deck['id'], context), deck['file']))
        return decks

    def get_deck_cards(self, deck_id, context):
        cards = dict()
        for card in self.cur.execute(
                'select count, name, sideboard_count, is_commander from card where deck_id=?', [deck_id]).fetchall():
            cards[card['name']] = CardInCollection(card['name'], card['count'], None,
                                                   sideboard=card['sideboard_count'],
                                                   commander=card['is_commander'] == 1, context=context)
        return cards

    def deck_count(self):
        with self.lock:
            data = self.cur.execute('select count(*) as count from deck').fetchone()
            if data is not None:
                return int(data['count'])
            else:
                return 0

    def card_count(self):
        with self.lock:
            data = self.cur.execute('select count(*) as count from card').fetchone()
            if data is not None:
                return int(data['count'])
            else:
                return 0

    def get_all_cards(self, context):
        all_cards = []
        with self.lock:
            for card in self.cur.execute('select sum(count) as count, name as name from card group by name').fetchall():
                all_cards.append(CardInCollection(card['name'], card['count'], None, context=context))
