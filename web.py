import io
import json
from datetime import datetime
from timeit import default_timer as timer
from types import SimpleNamespace

import humanize
from flask import Flask, make_response
from flask import abort
from flask import jsonify
from flask import request

import cardListFormater
import deckAge
import deckComplexity
import deckPrice
import listTokens
import mtgCardInCollectionObject
import mtgCardTextFileDao
import mtgColors
import verifyDeck
from mtgDeckObject import Deck
from price_source import priceSourceHandler
from web_infra.database import DeckDao
from web_infra.deck_manager import DeckManager

app = Flask(__name__, static_url_path='/')

with open('./config.json') as json_data_file:
    configuration = json.load(json_data_file)

deck_manager = DeckManager(DeckDao(), '../decklists/comanders_quaters', configuration)

priceSourceHandler.initPriceSource('none', configuration["cacheRootDirectory"], configuration["priceSources"])

deck_manager.init_decks(SimpleNamespace())


def basicCardList(deck_cards):
    res = []
    for deckCardName, deckCard in deck_cards.items():
        mana_cost = []
        image_uris = []
        if deckCard.jsonData.get('mana_cost', None) is not None:
            mana_cost = deckCard.jsonData.get('mana_cost', "")[1:-1].replace(' // ', '{=}').split("}{")
            image_uris.append(deckCard.jsonData.get("image_uris", {"normal": None})["normal"])
        elif deckCard.jsonData.get('card_faces', None) is not None:
            for face in deckCard.jsonData.get('card_faces', []):
                if len(mana_cost) > 0 and len(face.get('mana_cost', "")) > 0:
                    mana_cost.extend('=')
                mana_cost.extend(face.get('mana_cost', "")[1:-1].replace(' // ', '{=}').split("}{"))
                image_uris.append(face.get("image_uris", {"normal": None})["normal"])
        mana_cost = [cost.replace('/', '') for cost in mana_cost if cost != ""]
        res.append({'count': deckCard.count, 'name': deckCardName,
                    'colors': mtgColors.colorIdentity2String(deckCard.getProp('color')), 'manaCost': mana_cost,
                    'imageUris': image_uris, "scryfallUri": deckCard.jsonData.get("scryfall_uri", None)})
    return sorted(res, key=lambda item: item.get("name"))


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/<count>/staples.json', methods=['GET'])
def staples(count):
    print("staples start", count)
    start = timer()

    context = SimpleNamespace()

    card_collection = sorted(basicCardList(deck_manager.get_all_cards(context)), key=lambda item: item.get("count"),
                             reverse=True)

    json_response = {"cards": card_collection[:int(count)]}

    response = jsonify(json_response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Cache-Control', 'public, max-age=43200')

    end = timer()
    print("deckListDownload end, elapsed time ", (end - start))

    return response


@app.route('/<deck_hash>/deckList.txt', methods=['GET'])
def deckListDownload(deck_hash):
    print("deckListDownload start", deck_hash)
    start = timer()

    context = SimpleNamespace()
    context.filterLegality = None
    context.filterType = None
    context.print = None
    context.sort = ['shortType', 'name']

    deck = deck_manager.get_deck(deck_hash, context)

    if deck is None:
        abort(404, 'deck not found')
    else:

        print('Serving deck', deck.file)

        formated_file = io.StringIO()
        mtgCardTextFileDao.saveCardFile(formated_file, deck.cards, ['shortType'], context)
        formated_file.seek(0)

        file_name = ''
        first = True
        for deckCardName, deckCard in deck.getCommander().items():
            file_name = file_name + deckCardName
            if not first:
                file_name = file_name + '+'
            else:
                first = False

        file_name = file_name + "_" + deck_hash[-5:] + '.txt'

        file_response = formated_file.getvalue()
        formated_file.close()

        response = make_response(file_response, 200)

        response.headers.add('Content-Type', 'text/plain; charset=utf-8')
        response.headers.add('Content-Disposition', 'attachment;filename="' + file_name + '"')

        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Cache-Control', 'public, max-age=43200')

        end = timer()
        print("deckListDownload end, elapsed time ", (end - start))

        return response


@app.route('/<deck_hash>/deckList.json', methods=['GET'])
def deckList(deck_hash):
    print("deckList start", deck_hash)
    start = timer()

    context = SimpleNamespace()

    deck = deck_manager.get_deck(deck_hash, context)

    if deck is None:
        abort(404, 'deck not found')
    else:

        json_response = {}

        print('Serving deck', deck.file)
        json_response["commanders"] = basicCardList(deck.getCommander())
        json_response["companions"] = basicCardList(deck.getSideboard())
        json_response['deckList'] = []
        for shortType in sorted(deck.getShortTypes(),
                                key=lambda type_item: mtgCardInCollectionObject.getShortTypeOrder(type_item)):
            list_of_type = basicCardList(deck.getByShortType(shortType))
            count = 0
            for item in list_of_type:
                count = count + item['count']
            json_response['deckList'].append(
                {'shortType': shortType.capitalize(), 'count': count, 'cards': list_of_type})

        with open(deck.file) as f:
            first_line = f.readline()
            if first_line.startswith("# source: "):
                json_response["url"] = first_line[len("# source: "):]

        response = jsonify(json_response)
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Cache-Control', 'public, max-age=43200')

        end = timer()
        print("deckList end, elapsed time ", (end - start))

        return response


@app.route('/<deck_hash>/tokens.json', methods=['GET'])
def list_tokens(deck_hash):
    print("tokens start", deck_hash)
    start = timer()

    context = SimpleNamespace()

    deck = deck_manager.get_deck(deck_hash, context)

    if deck is None:
        abort(404, 'deck not found')
    else:

        tokens = []
        counters = []
        others = []

        print('Serving deck', deck.file)
        response = listTokens.listTokens(deck)
        for token in sorted(response['tokens']):
            tokens.append({'token': token, 'cards': basicCardList(
                cardListFormater.cardObjectListToCardObjectMap(response['tokens'][token]))})
        for counter in sorted(response['counters']):
            counters.append({'counter': counter, 'cards': basicCardList(
                cardListFormater.cardObjectListToCardObjectMap(response['counters'][counter]))})
        for other in sorted(response['other']):
            others.append({'other': other, 'cards': basicCardList(
                cardListFormater.cardObjectListToCardObjectMap(response['other'][other]))})

        json_response = {'tokens': tokens, 'counters': counters, 'other': others}

        response = jsonify(json_response)
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

    decks = deck_manager.get_decks(context)

    response = []

    for deck in decks:

        missing_cards = verifyDeck.missingCards(deck.cards, collection, context.currency)

        deck_info = dict()

        deck_info["deckFile"] = deck_manager.hash_deck(deck)

        deck_info["commanders"] = basicCardList(deck.getCommander())
        deck_info["companions"] = basicCardList(deck.getSideboard())

        deck_info['percentage'] = 100 * (missing_cards['totalDeckCards'] - missing_cards['totalCount']) / missing_cards[
            'totalDeckCards']
        deck_info['printPercentage'] = "{:3.2f}".format(deck_info['percentage']) + "%"

        deck_info['haveList'] = []

        have_list = Deck(cardListFormater.cardObjectCountMapToCardObjectMap(missing_cards['haveList']), deck.file)

        total_count = 0

        for shortType in sorted(have_list.getShortTypes(),
                                key=lambda type_item: mtgCardInCollectionObject.getShortTypeOrder(type_item)):
            list_of_type = basicCardList(have_list.getByShortType(shortType))
            count = 0
            for item in list_of_type:
                count = count + item['count']
            total_count = total_count + count
            deck_info['haveList'].append({'shortType': shortType.capitalize(), 'count': count, 'cards': list_of_type})

        deck_info['haveListCount'] = total_count

        deck_info['shoppingList'] = []

        shopping_list = Deck(cardListFormater.cardObjectCountMapToCardObjectMap(missing_cards['shoppingList']),
                             deck.file)

        total_count = 0

        for shortType in sorted(shopping_list.getShortTypes(),
                                key=lambda type_item: mtgCardInCollectionObject.getShortTypeOrder(type_item)):
            list_of_type = basicCardList(shopping_list.getByShortType(shortType))
            count = 0
            for item in list_of_type:
                count = count + item['count']
            total_count = total_count + count
            deck_info['shoppingList'].append(
                {'shortType': shortType.capitalize(), 'count': count, 'cards': list_of_type})

        deck_info['shoppingListCount'] = total_count

        deck_info['shoppingListPrice'] = int(missing_cards['totalPrice'])

        response.append(deck_info)

    json_response = sorted(response, key=lambda i: i['percentage'], reverse=True)

    for line in json_response:
        del line["percentage"]

    end = timer()
    print("possibleDecks end, elapsed time ", (end - start))

    return jsonify(json_response)


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

    decks = deck_manager.get_decks(context)
    response = []

    for deck in decks:
        deck_prices = deckPrice.deckPrice(deck.cards, currency)
        deck_ages = deckAge.deckAge(deck.cards)

        deck_info = dict()

        deck_info["deckPriceTotal"] = int(deck_prices["deckPrice"])
        deck_info["commanders"] = basicCardList(deck.getCommander())
        deck_info["commanders_sort"] = "_".join([item['name'] for item in deck_info["commanders"]])
        deck_info["companions"] = basicCardList(deck.getSideboard())
        deck_info["date"] = datetime.now() - deck_ages["deckDate"]
        deck_info["age"] = humanize.naturaldelta(deck_ages["deckDate"] - datetime.now(), months=True)
        deck_info["rank"] = deck.getAverageEDHrecRank()
        deck_info["complexity"] = deckComplexity.deckComplexity(deck.cards)["complexity"]
        deck_info["deckFile"] = deck_manager.hash_deck(deck)

        response.append(deck_info)

    json_response = sorted(response, key=lambda i: i[sort])

    for line in json_response:
        del line["date"]
        del line["commanders_sort"]

    response = jsonify(json_response)
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Cache-Control', 'public, max-age=43200')

    end = timer()
    print("deckPriceMethod end, elapsed time ", (end - start))

    return response
