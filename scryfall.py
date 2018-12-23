import requests
import json
import string
import unicodedata
import os
import sys
import datetime
import shutil

import console

proxies = None
auth = None

valid_filename_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)

clearCache = 'none'
cacheTimeout = 365

def getChacgeDir():
	return os.path.join(os.path.dirname(sys.argv[0]), ".scryfallCache")

def flushCache():
	try:
		shutil.rmtree(getChacgeDir())
	except OSError as e:
		print ("Error: %s - %s." % (e.filename, e.strerror))

def initCache(collection):
	print()

	lastLength = 0

	count = 1;

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
	sys.stdout.write('\n' + 'Done. ' + '\n')
	sys.stdout.flush()
		
def cleanFilename(filename, whitelist=valid_filename_chars, replace=' '):
	# replace spaces
	for r in replace:
		filename = filename.replace(r, '_')
	
	# keep only valid ascii chars
	cleaned_filename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore').decode()
	
	# keep only whitelisted chars
	return ''.join(c for c in cleaned_filename if c in whitelist)

def fetchCardJson(card, jsonFile):
	response = requests.get("http://api.scryfall.com/cards/named",  params={'exact': card.name}, proxies=proxies, auth=auth)
	if (response.status_code == 404):
		print ()
		print (console.CRED + "Card '" + card.name + "' (" + str(card.sourceFile) + ") Was not found in scryfall using exact search." + console.CEND + " Trying fuzzy search.")
		response = requests.get("http://api.scryfall.com/cards/named",  params={'fuzzy': card.name}, proxies=proxies, auth=auth)
		if (response.status_code < 400):
			print ("\'" + card.name + "\' found as \'" + response.json()["name"] + "\'.")
	if (response.status_code >= 400):
		raise Exception('Bad response ' + str(response.status_code) + ' for ' + card.name) 
	with open(jsonFile, 'w') as f:
		json.dump(response.json(), f)
	return response.json()

def getCachedCardJson(card):
	baseDir = getChacgeDir()
	jsonFile = os.path.join(baseDir, cleanFilename(card.name) + ".json")
	if (not os.path.exists(baseDir)):
		os.makedirs(baseDir)
	if (os.path.exists(jsonFile)):
		fileAge = datetime.date.today() - datetime.date.fromtimestamp(os.path.getmtime(jsonFile))

		if (clearCache == 'always' or (clearCache == 'timeout' and fileAge > cacheTimeout) or (clearCache == 'price' and fileAge > 1)):
			return fetchCardJson(card, jsonFile)
		else:
#		print("Loading cached " + jsonFile)
			with open(jsonFile, encoding='utf-8') as json_data:
				return json.load(json_data)
	else:
#		print("Loading online " + jsonFile)
		return fetchCardJson(card, jsonFile)
#
