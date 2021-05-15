import hashlib
import io
import json
from datetime import datetime
from timeit import default_timer as timer
from types import SimpleNamespace

import humanize
from flask import Flask
from flask import abort
from flask import jsonify
from flask import request

import cardListFormater
import mtgCardInCollectionObject

import deckAge
import deckPrice
import mtgCardTextFileDao
import mtgColors
import priceSourceHandler
import deckComplexity
import listTokens
import verifyDeck
from mtgDeckObject import Deck

app = Flask(__name__, static_url_path='/')

salt = "$!K;g.}yDdeg\"Q5J".encode('utf-8')

deckHome = '../decklists/comanders_quaters'

configuration = {}
with open('./config.json') as json_data_file:
    configuration = json.load(json_data_file)

priceSourceHandler.initPriceSource('none', configuration["priceSources"])

def basicCardList(deckCards):
    res = []
    for deckCardName, deckCard in deckCards.items():
        manaCost = []
        imageUris = []
        if deckCard.jsonData.get('mana_cost', None) is not None:
            manaCost = deckCard.jsonData.get('mana_cost', "")[1:-1].replace(' // ', '{=}').split("}{")
            imageUris.append(deckCard.jsonData.get("image_uris", {"normal": None})["normal"])
        elif deckCard.jsonData.get('card_faces', None) is not None:
            for face in deckCard.jsonData.get('card_faces', []):
                if len(manaCost) > 0 and len(face.get('mana_cost', "")) > 0:
                    manaCost.extend('=')
                manaCost.extend(face.get('mana_cost', "")[1:-1].replace(' // ', '{=}').split("}{"))
                imageUris.append(face.get("image_uris", {"normal": None})["normal"])
        manaCost = [cost.replace('/', '') for cost in manaCost if cost != ""]
        res.append({'count': deckCard.count, 'name': deckCardName,
                    'colors': mtgColors.colorIdentity2String(deckCard.getProp('color')), 'manaCost': manaCost,
                    'imageUris': imageUris, "scryfallUri": deckCard.jsonData.get("scryfall_uri", None)})
    return  sorted(res, key=lambda item: item.get("name"))


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/<deck>/deckList.json', methods=['GET'])
def deckList(deck):
    print("deckList start", deck)
    start = timer()

    context = SimpleNamespace()

    decks = mtgCardTextFileDao.readDeckDirectory(deckHome, {}, configuration["filePattern"], context)

    jsonResponse = {}

    for file in decks:
        if deck == hashlib.sha256(file.encode() + salt).hexdigest():
            print ('Serving deck', file)
            deck = Deck(decks[file])
            jsonResponse["commanders"] = basicCardList(deck.getCommander())
            jsonResponse["companions"] = basicCardList(deck.getSideboard())
            jsonResponse['deckList'] = []
            for shortType in sorted(deck.getShortTypes(), key=lambda item: mtgCardInCollectionObject.getShortTypeOrder(item)):
                listOfType = basicCardList(deck.getByShortType(shortType))
                count = 0
                for item in listOfType:
                    count = count + item['count']
                jsonResponse['deckList'].append({'shortType': shortType.capitalize(), 'count': count, 'cards': listOfType})

            with open(file) as f:
                first_line = f.readline()
                if first_line.startswith("# source: "):
                    jsonResponse["url"] = first_line[len("# source: "):]
            break

    response = jsonify(jsonResponse)
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Cache-Control', 'public, max-age=43200')

    end = timer()
    print("deckPriceMethod end, elapsed time ", (end - start))

    return response


@app.route('/<deck>/tokens.json', methods=['GET'])
def tokens(deck):
    print("tokens start", deck)
    start = timer()

    context = SimpleNamespace()

    decks = mtgCardTextFileDao.readDeckDirectory(deckHome, {}, configuration["filePattern"], context)

    tokens = []
    counters = []
    others = []

    for file in decks:
        if deck == hashlib.sha256(file.encode() + salt).hexdigest():
            print ('Serving deck', file)
            response = listTokens.listTokens(decks[file])
            for token in sorted(response['tokens']):
                tokens.append({'token': token, 'cards': basicCardList(cardListFormater.cardObjectListToCardObjectMap(response['tokens'][token]))})
            for counter in sorted(response['counters']):
                counters.append({'counter': counter, 'cards': basicCardList(cardListFormater.cardObjectListToCardObjectMap(response['counters'][counter]))})
            for other in sorted(response['other']):
                others.append({'other': other, 'cards': basicCardList(cardListFormater.cardObjectListToCardObjectMap(response['other'][other]))})

    jsonResponse = {'tokens': tokens, 'counters': counters, 'other': others}

    response = jsonify(jsonResponse)
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Cache-Control', 'public, max-age=43200')

    end = timer()
    print("tokens end, elapsed time ", (end - start))

    return response


@app.route('/<currency>/possibleDecks.json', methods=['POST'])
def possibleDecks(currency):
    print("possibleDecks start")
    start = timer()

    context = SimpleNamespace()
    context.currency = currency
    context.sort = 'name'

    collection = request.form['collection']

    with io.StringIO(collection) as f:
        collection = mtgCardTextFileDao.readCardFile(f, 'web_request', {}, False, context)

    decks = mtgCardTextFileDao.readDeckDirectory(deckHome, {}, configuration["filePattern"], context)

    response = []

    for file in decks:
        deckList = decks[file]

        missingCards = verifyDeck.missingCards(deckList, collection, context.currency)

        deckInfo = {}

        deckInfo["deckFile"] = hashlib.sha256(file.encode() + salt).hexdigest()

        deck = Deck(deckList)

        deckInfo["commanders"] = basicCardList(deck.getCommander())
        deckInfo["companions"] = basicCardList(deck.getSideboard())

        deckInfo['percentage'] = 100 * (missingCards['totalDeckCards'] - missingCards['totalCount']) / missingCards['totalDeckCards']
        deckInfo['printPercentage'] = "{:3.2f}".format(deckInfo['percentage'] ) + "%"

        deckInfo['haveList'] = []

        haveList = Deck(cardListFormater.cardObjectCountMapToCardObjectMap(missingCards['haveList']))

        totalCount = 0

        for shortType in sorted(haveList.getShortTypes(), key=lambda item: mtgCardInCollectionObject.getShortTypeOrder(item)):
            listOfType = basicCardList(haveList.getByShortType(shortType))
            count = 0
            for item in listOfType:
                count = count + item['count']
            totalCount = totalCount + count
            deckInfo['haveList'].append({'shortType': shortType.capitalize(), 'count': count, 'cards': listOfType})

        deckInfo['haveListCount'] = totalCount

        deckInfo['shoppingList'] = []

        shoppingList = Deck(cardListFormater.cardObjectCountMapToCardObjectMap(missingCards['shoppingList']))

        totalCount = 0

        for shortType in sorted(shoppingList.getShortTypes(), key=lambda item: mtgCardInCollectionObject.getShortTypeOrder(item)):
            listOfType = basicCardList(shoppingList.getByShortType(shortType))
            count = 0
            for item in listOfType:
                count = count + item['count']
            totalCount = totalCount + count
            deckInfo['shoppingList'].append({'shortType': shortType.capitalize(), 'count': count, 'cards': listOfType})

        deckInfo['shoppingListCount'] = totalCount

        deckInfo['shoppingListPrice'] = int(missingCards['totalPrice'])

        response.append(deckInfo)

    jsonResponse = sorted(response, key=lambda i: i['percentage'], reverse=True)

    for line in jsonResponse:
        del line["percentage"]

    end = timer()
    print("possibleDecks end, elapsed time ", (end - start))

    return jsonify(jsonResponse)

@app.route('/<currency>/<sort>/deckPrice.json', methods=['GET'])
def deckPriceMethod(currency, sort):
    print("deckPriceMethod start", currency, sort)
    start = timer()

    if currency not in ['eur', 'usd', 'tix', 'czk']:
        abort(400, description="Currency invalid")
    if sort not in ['deckPriceTotal', 'date', 'rank', 'commanders_sort', 'complexity']:
        abort(400, description="Sort invalid")

    context = SimpleNamespace()
    context.currency = currency

    decks = mtgCardTextFileDao.readDeckDirectory(deckHome, {}, configuration["filePattern"], context)

    response = []

    for file in decks:
        deckList = decks[file]
        deckPrices = deckPrice.deckPrice(deckList, currency)
        deckAges = deckAge.deckAge(deckList)
        deck = Deck(deckList)

        deckInfo = {}

        deckInfo["deckPriceTotal"] = int(deckPrices["deckPrice"])
        deckInfo["commanders"] = basicCardList(deck.getCommander())
        deckInfo["commanders_sort"] = "_".join([item['name'] for item in deckInfo["commanders"]])
        deckInfo["companions"] = basicCardList(deck.getSideboard())
        deckInfo["date"] = datetime.now() - deckAges["deckDate"]
        deckInfo["age"] = humanize.naturaldelta(deckAges["deckDate"] - datetime.now(), months=True)
        deckInfo["rank"] = deck.getAverageEDHrecRank()
        deckInfo["complexity"] = deckComplexity.deckComplexity(deckList)["complexity"]
        deckInfo["deckFile"] = hashlib.sha256(file.encode() + salt).hexdigest()

        response.append(deckInfo)

    jsonResponse = sorted(response, key=lambda i: i[sort])

    for line in jsonResponse:
        del line["date"]
        del line["commanders_sort"]

    response = jsonify(jsonResponse)
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Cache-Control', 'public, max-age=43200')

    end = timer()
    print("deckPriceMethod end, elapsed time ", (end - start))

    return response
