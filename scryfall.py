import datetime
import json
import os
from json import JSONDecodeError

import requests
import shutil
import sys

import console
import util

proxies = None
auth = None

clearCache = 'none'
cacheTimeout = 365

class CardRetrievalError(Exception):
    def __init__(self, message, cardName, errorCode):
        super(CardRetrievalError, self).__init__(message)
        self.cardName = cardName
        self.errorCode = errorCode

def getCacheDir():
	baseDir = os.path.join(os.path.dirname(sys.argv[0]), ".scryfallCache")
	if (not os.path.exists(baseDir)):
		os.makedirs(baseDir)
	return baseDir

def flushCache():
	try:
		shutil.rmtree(getCacheDir())
	except OSError as e:
		print ("Error where clearing cache directory at " + getCacheDir() + ": %s - %s." % (e.filename, e.strerror))

def initCache(collection):
	lastLength = 0
	count = 1

	for card in collection:

		statusLine = 'Fetching card info (' + str(count) + '/' + str(len(collection)) + ', ...' + str(collection[card].sourceFile)[-50:-2]  + '): ' + card + " ..."

		count += 1
		currentLength = len(statusLine)
		if (currentLength < lastLength):
			statusLine = statusLine + (lastLength - currentLength) * ' '
		# newline before doing "status"
		if (lastLength == 0):
			sys.stdout.write('\n')
		lastLength = currentLength

		sys.stdout.write('\r' + statusLine)
		sys.stdout.flush()
		collection[card].jsonData['name']
	doneMessage = ''
	sys.stdout.write('\r' + doneMessage + (lastLength - len(doneMessage)) * " " + '\r')
	sys.stdout.flush()

def fetchCardJson(card, jsonFile, retryTimes = 3):
	response = requests.get("http://api.scryfall.com/cards/named",  params={'exact': card.name}, proxies=proxies, auth=auth)
	fuzzyResult = False
	if (response.status_code == 404):
		print ()
		print (console.CRED + "Card '" + card.name + "' (" + str(card.sourceFile) + ") Was not found in scryfall using exact search." + console.CEND + " Trying fuzzy search.")
		response = requests.get("http://api.scryfall.com/cards/named",  params={'fuzzy': card.name}, proxies=proxies, auth=auth)
		fuzzyResult = True
		if (response.status_code < 400):
			print ("\'" + card.name + "\' found as \'" + response.json()["name"] + "\'. " + console.CRED + "Fix files " + str(card.sourceFile) + console.CEND)
	if ((response.status_code == 503 or response.status_code == 504) and retryTimes > 0):
		sys.stderr.write('Retrying ' + response.url)
		fetchCardJson(card, jsonFile, retryTimes - 1)
	elif (response.status_code >= 400 or retryTimes == 0):	
		raise CardRetrievalError('Bad response ' + str(response.status_code) + ' for ' + card.name, card.name, response.status_code) 
	if (not fuzzyResult):
		with open(jsonFile, 'w') as f:
			json.dump(response.json(), f)
	return response.json()

def getCachedCardJson(card):
	jsonFile = os.path.join(getCacheDir(), util.cleanFilename(card) + ".json")
	if (os.path.exists(jsonFile)):
		fileAge = datetime.date.today() - datetime.date.fromtimestamp(os.path.getmtime(jsonFile))

		if (clearCache == 'always' or (clearCache == 'timeout' and fileAge.days > cacheTimeout) or (clearCache == 'price' and fileAge.days > 1)):
			return fetchCardJson(card, jsonFile)
		else:
			print("Loading cached " + jsonFile)
			with open(jsonFile, encoding='utf-8') as json_data:
				try:
					return json.load(json_data)
				except JSONDecodeError:
					print("Deleting and retrying invalid " + jsonFile)
					json_data.close()
					os.remove(jsonFile)
					return fetchCardJson(card, jsonFile)
	else:
#		print("Loading online " + jsonFile)
		return fetchCardJson(card, jsonFile)
#

def search(query):

	foundCardNames = []

	response = requests.get('https://api.scryfall.com/cards/search',  params={'q': query}, proxies=proxies, auth=auth)

	while(response is not None and response.status_code == 200):

		json = response.json()

		for card in json['data']:
			foundCardNames.append(card['name'])

		if (json['has_more'] == True):
			response = requests.get(json['next_page'], proxies=proxies, auth=auth)
		else:
			response = None

	return foundCardNames