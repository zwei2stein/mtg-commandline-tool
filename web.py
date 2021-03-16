import json
from types import SimpleNamespace

import hashlib

from flask import Flask
from flask import abort
from flask import jsonify

import deckPrice
import mtgCardTextFileDao
import priceSourceHandler
from mtgDeckObject import Deck

app = Flask(__name__)

configuration = {}
with open('./config.json') as json_data_file:
	configuration = json.load(json_data_file)

priceSourceHandler.initPriceSource('none', configuration["priceSources"])

def basicCardList(deckCards):
	res = []
	for deckCardName in deckCards:
		res.append(deckCardName)
	return res

@app.route('/')
def index():
    abort(403)

@app.route('/<currency>/deckPrice.json', methods=['GET'])
def deckPriceMethod(currency):

	context = SimpleNamespace()
	context.currency = currency

	decks = mtgCardTextFileDao.readDeckDirectory('../decklists/comanders_quaters', {}, configuration["filePattern"], context)

	response = []

	for file in decks:
		print(file + ":")
		deckList = decks[file]
		deckPrices = deckPrice.deckPrice(deckList, currency)
		deck = Deck(deckList)

		deckPrices["deckPriceTotal"] = str(deckPrices["deckPrice"])
		deckPrices["commanders"] = basicCardList(deck.getCommander())
		deckPrices["companions"] = basicCardList(deck.getSideboard())
		deckPrices["deckFile"] = hashlib.sha256(file.encode()).hexdigest()

		response.append(deckPrices)

	jsonResponse = sorted(response, key = lambda i: i['deckPrice'])

	response = jsonify(jsonResponse)
	response.headers.add('Access-Control-Allow-Origin', '*')

	return response


