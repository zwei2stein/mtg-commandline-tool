import datetime
import json
import os
import shutil
import sys
from json import JSONDecodeError

import requests

import console
import util

proxies = None
auth = None

clear_cache = 'none'
cacheTimeout = 365


class CardRetrievalError(Exception):
    def __init__(self, message, card_name, error_code):
        super(CardRetrievalError, self).__init__(message)
        self.cardName = card_name
        self.errorCode = error_code


def getCacheDir():
    base_dir = os.path.join(os.path.dirname(sys.argv[0]), ".scryfallCache")
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    return base_dir


def flushCache():
    try:
        shutil.rmtree(getCacheDir())
    except OSError as e:
        print("Error where clearing cache directory at " + getCacheDir() + ": %s - %s." % (e.filename, e.strerror))


def initCache(collection):
    last_length = 0
    count = 1

    for card in collection:

        status_line = 'Fetching card info (' + str(count) + '/' + str(len(collection)) + ', ...' + str(
            collection[card].sourceFile)[-50:-2] + '): ' + card + " ..."

        count += 1
        currentLength = len(status_line)
        if currentLength < last_length:
            status_line = status_line + (last_length - currentLength) * ' '
        # newline before doing "status"
        if last_length == 0:
            sys.stdout.write('\n')
        last_length = currentLength

        sys.stdout.write('\r' + status_line)
        sys.stdout.flush()
    doneMessage = ''
    sys.stdout.write('\r' + doneMessage + (last_length - len(doneMessage)) * " " + '\r')
    sys.stdout.flush()


def fetchCardJson(card, json_file, retry_times=3):
    response = requests.get("http://api.scryfall.com/cards/named", params={'exact': card.techName}, proxies=proxies,
                            auth=auth)
    fuzzy_result = False
    if response.status_code == 404:
        print()
        print(console.CRED + "Card '" + card.techName + "' (" + util.absolutePaths(
            card.sourceFile) + ") Was not found in scryfall using exact search." + console.CEND + " Trying fuzzy search.")
        response = requests.get("http://api.scryfall.com/cards/named", params={'fuzzy': card.techName}, proxies=proxies,
                                auth=auth)
        fuzzy_result = True
        if response.status_code < 400:
            print("\'" + card.techName + "\' found as \'" + response.json()[
                "name"] + "\'. " + console.CRED + "Fix files " + util.absolutePaths(card.sourceFile) + console.CEND)
    if (response.status_code == 503 or response.status_code == 504) and retry_times > 0:
        sys.stderr.write('Retrying ' + response.url)
        fetchCardJson(card, json_file, retry_times - 1)
    elif response.status_code >= 400 or retry_times == 0:
        raise CardRetrievalError(
            'Bad response ' + str(response.status_code) + ' for ' + card.techName + "' (" + util.absolutePaths(
                card.sourceFile) + ")",
            card.techName, response.status_code)
    if not fuzzy_result:
        with open(json_file, 'w') as f:
            json.dump(response.json(), f)
    return response.json()


def getCachedCardJson(card):
    jsonFile = os.path.join(getCacheDir(), util.cleanFilename(card) + ".json")
    if os.path.exists(jsonFile):
        fileAge = datetime.date.today() - datetime.date.fromtimestamp(os.path.getmtime(jsonFile))

        if (clear_cache == 'always' or (clear_cache == 'timeout' and fileAge.days > cacheTimeout) or (
                clear_cache == 'price' and fileAge.days > 1)):
            return fetchCardJson(card, jsonFile)
        else:
            # print("Loading cached " + jsonFile)
            with open(jsonFile, encoding='utf-8') as json_data:
                try:
                    return json.load(json_data)
                except JSONDecodeError:
                    print("Deleting and retrying invalid " + jsonFile)
                    json_data.close()
                    os.remove(jsonFile)
                    return fetchCardJson(card, jsonFile)
    else:
        # print("Loading online " + jsonFile)
        return fetchCardJson(card, jsonFile)


def searchByCard(card):
    url = card.jsonData['prints_search_uri']

    json_file = os.path.join(getCacheDir(), card.jsonData["oracle_id"] + ".prints.json")
    if os.path.exists(json_file):
        file_age = datetime.date.today() - datetime.date.fromtimestamp(os.path.getmtime(json_file))

        if (clear_cache == 'always' or (clear_cache == 'timeout' and file_age.days > cacheTimeout) or (
                clear_cache == 'price' and file_age.days > 1)):
            return fetchCardJson(card, json_file)
        else:
            # print("Loading cached " + jsonFile)
            with open(json_file, encoding='utf-8') as json_data:
                try:
                    return json.load(json_data)
                except JSONDecodeError:
                    print("Deleting and retrying invalid " + json_file)
                    json_data.close()
                    os.remove(json_file)
                    return searchByCard(card)

    response = requests.get(url, proxies=proxies, auth=auth)

    foundCardsJson = []

    while response is not None and response.status_code == 200:

        jsonResponse = response.json()

        for card in jsonResponse['data']:
            foundCardsJson.append(card)

        if jsonResponse['has_more']:
            response = requests.get(jsonResponse['next_page'], proxies=proxies, auth=auth)
        else:
            response = None

    with open(json_file, 'w') as f:
        json.dump(foundCardsJson, f)

    return foundCardsJson


def search(query):
    response = requests.get('https://api.scryfall.com/cards/search', params={'q': query}, proxies=proxies, auth=auth)

    foundCardNames = []

    while response is not None and response.status_code == 200:

        jsonResponse = response.json()

        for card in jsonResponse['data']:
            foundCardNames.append(card['name'])

        if jsonResponse['has_more']:
            response = requests.get(jsonResponse['next_page'], proxies=proxies, auth=auth)
        else:
            response = None

    return foundCardNames


def getTokenByUrl(url):
    response = requests.get(url, proxies=proxies, auth=auth)
    if response is not None and response.status_code == 200:
        return response.json()
    else:
        return None


def get_set_data(set_code):
    json_file = os.path.join(getCacheDir(), set_code + "_set.json")
    if os.path.exists(json_file):
        with open(json_file, encoding='utf-8') as json_data:
            try:
                return json.load(json_data)
            except JSONDecodeError:
                print("Deleting and retrying invalid " + json_file)
                json_data.close()
                os.remove(json_file)
                return get_set_data(set_code)
    else:
        response = requests.get('https://api.scryfall.com/sets/' + set_code, proxies=proxies, auth=auth)
        if response.status_code == 200:
            with open(json_file, 'w') as f:
                json.dump(response.json(), f)
            return response.json()
        else:
            return dict()
