import hashlib
import json
from datetime import datetime
from types import SimpleNamespace

import humanize
from flask import Flask
from flask import abort
from flask import jsonify

import deckAge
import deckPrice
import mtgCardTextFileDao
import priceSourceHandler
import mtgColors
from mtgDeckObject import Deck

app = Flask(__name__)

configuration = {}
with open('./config.json') as json_data_file:
    configuration = json.load(json_data_file)

priceSourceHandler.initPriceSource('none', configuration["priceSources"])


def basicCardList(deckCards):
    res = []
    for deckCardName, deckCard in deckCards.items():
        res.append({'name': deckCardName, 'colors': mtgColors.colorIdentity2String(deckCard.getProp('color'))})
    return res


@app.route('/')
def index():
    abort(403)


@app.route('/<currency>/<sort>/deckPrice.json', methods=['GET'])
def deckPriceMethod(currency, sort):

    if currency not in ['eur', 'usd', 'tix', 'czk']:
        abort(400, description="Currency invalid")
    if sort not in ['deckPriceTotal', 'date', 'rank', 'commanders']:
        abort(400, description="Sort invalid")

    context = SimpleNamespace()
    context.currency = currency

    decks = mtgCardTextFileDao.readDeckDirectory('../decklists/comanders_quaters', {}, configuration["filePattern"],
                                                 context)

    response = []

    for file in decks:
        deckList = decks[file]
        deckPrices = deckPrice.deckPrice(deckList, currency)
        deckAges = deckAge.deckAge(deckList)
        deck = Deck(deckList)

        deckPrices["deckPriceTotal"] = int(deckPrices["deckPrice"])
        deckPrices["commanders"] = sorted(basicCardList(deck.getCommander()), key=lambda item: item.get("name"))
        deckPrices["companions"] = sorted(basicCardList(deck.getSideboard()), key=lambda item: item.get("name"))
        deckPrices["date"] = deckAges["deckDate"]
        deckPrices["age"] = humanize.naturaldelta(deckAges["deckDate"] - datetime.now(), months=True)
        deckPrices["rank"] = deck.getAverageEDHrecRank()
        deckPrices["deckFile"] = hashlib.sha256(file.encode()).hexdigest()

        response.append(deckPrices)

    jsonResponse = sorted(response, key=lambda i: i[sort])

    response = jsonify(jsonResponse)
    response.headers.add('Access-Control-Allow-Origin', '*')

    return response
