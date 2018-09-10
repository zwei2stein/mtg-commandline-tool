import requests
import json
import string
import unicodedata
import os

import console

proxies = None
auth = None

valid_filename_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)

def cleanFilename(filename, whitelist=valid_filename_chars, replace=' '):
	# replace spaces
	for r in replace:
		filename = filename.replace(r, '_')
	
	# keep only valid ascii chars
	cleaned_filename = unicodedata.normalize('NFKD', filename).encode('ASCII', 'ignore').decode()
	
	# keep only whitelisted chars
	return ''.join(c for c in cleaned_filename if c in whitelist)

def getCachedCardJson(card):
	baseDir = ".scryfall"
	jsonFile = baseDir + "/" + cleanFilename(card.name) + ".json"
	if (not os.path.exists(baseDir)):
		os.makedirs(baseDir)
	if (os.path.exists(jsonFile)):
#		print("Loading cached " + jsonFile)
		with open(jsonFile, encoding='utf-8') as json_data:
			return json.load(json_data)
	else:
#		print("Loading online " + jsonFile)
		response = requests.get("http://api.scryfall.com/cards/named",  params={'exact': card.name}, proxies=proxies, auth=auth)
		if (response.status_code == 404):
			print ()
			print ( console.CRED + "Card '" +card.name + "'' Was not found in scryfall using exact search." + console.CEND + " Trying fuzzy search.")
			response = requests.get("http://api.scryfall.com/cards/named",  params={'fuzzy': card.name}, proxies=proxies, auth=auth)
			if (response.status_code < 400):
				print ("Found as " + response.json()["name"])
		
		if (response.status_code >= 400):
			raise Exception('Bad response ' + str(response.status_code) + ' for ' + card.name) 
		with open(jsonFile, 'w') as f:
			json.dump(response.json(), f)
		return response.json()

#
