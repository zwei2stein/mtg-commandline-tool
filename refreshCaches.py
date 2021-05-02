from types import SimpleNamespace

import deckPrice
import mtgCardTextFileDao
import json
import sys
from timeit import default_timer as timer
import humanize

import priceSourceHandler

deckHome = './decklists/comanders_quaters'

def main():
    start = timer()

    with open(sys.path[0] + '/config.json') as json_data_file:
        configuration = json.load(json_data_file)

    configuration["scryfall"]["cacheTimeout"] = 1

    priceSourceHandler.initPriceSource('none', configuration["priceSources"])

    context = SimpleNamespace()
    decks = mtgCardTextFileDao.readDeckDirectory(deckHome, {}, configuration["filePattern"], context)

    currencies = ['usd','eur','tix']

    i = 1

    for file in decks:
        print("{:.0%}".format(i/len(decks)) + ' ' + humanize.naturaldelta(timer() - start) + ', Processing: ' + file)
        deckList = decks[file]
        for currency in currencies:
            context.currency = currency
            deckPrice.deckPrice(deckList, currency)
        i = i + 1

main()