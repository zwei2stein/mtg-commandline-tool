import re

import console

def appendListInMap(map, key, item):
	key = key.capitalize()
	if (key not in map):
		map[key] = set([])
	map[key].add(item)

def addCounter(counterType, keyWords, list, oracleText, deckCardName):
		for keyWord in keyWords:
			match = re.search('('+keyWord+')', oracleText)			
			if (match):
				appendListInMap(list, counterType, deckCardName)

def listTokens(deckCards):
	tokens = {}
	counters = {}
	misc = {}
	tokenCandidates = {}

	for deckCardName in deckCards:
		deckCard = deckCards[deckCardName]
		oracleText = deckCard.jsonData.get('oracle_text', '')
		typeLine = deckCard.jsonData.get('type_line','')

		for face in deckCard.jsonData.get('card_faces', []):
			oracleText = oracleText + '\n' + face.get('oracle_text', '')
			typeLine = typeLine + '\n' + face.get('type_line', '')

		oracleTextWithoutCardName = oracleText.replace(deckCardName, 'CARD_NAME')

		foundToken = False

		match = re.search("(Fabricate [0-9]+)", oracleText)
		if (match):
			appendListInMap(tokens,  "1/1 colorless Servo artifact creature token", deckCardName)
			appendListInMap(counters,  "+1/+1 counter", deckCardName)
			foundToken = True

		match = re.search("(Afterlife [0-9]+)", oracleText)
		if (match):
			appendListInMap(tokens,  "1/1 white and black Spirit creature token with flying", deckCardName)
			foundToken = True

		match = re.search("(Embalm)", oracleText)
		if (match):
			subtype = typeLine.split("\u2014", 1)[1].strip()
			appendListInMap(tokens, deckCard.jsonData.get('power','?') + '/' + deckCard.jsonData.get('toughness','?')  + " white "+ deckCardName + " " + subtype + " Zombie token", deckCardName)
			appendListInMap(misc, "Embalm marker", deckCardName)
			foundToken = True

		match = re.search('(Eternalize)', oracleText)
		if (match):
			appendListInMap(tokens, "4/4 black "+ deckCardName +" Zombie token", deckCardName)
			appendListInMap(misc, "Eternalize marker", deckCardName)
			foundToken = True

		match = re.search('([Mm]orph)', oracleText)
		if (match):
			appendListInMap(tokens, "2/2 colorless creature", deckCardName)

		match = re.search('([Mm]anifest)', oracleText)
		if (match):
			appendListInMap(tokens, "2/2 colorless creature", deckCardName)

		match = re.search("([iI]nvestigate)", oracleText)
		if (match):
			appendListInMap(tokens, "colorless Clue artifact token with \"{2}, Sacrifice this artifact: Draw a card.\"", deckCardName)
			foundToken = True

		for match in re.finditer('[Cc]reate(s)? ([a-zX ]+) (([0-9X]+)/([0-9X]+) ([a-z ]+) ([A-Za-z ]+) ([a-z ]+) token(s)?( with [A-Za-z ]+)?)', oracleText):
			tokenString = match.string[match.start(3):match.end(3)]
			tokenString = re.sub("tokens", "token", tokenString, 1)
			appendListInMap(tokens, tokenString, deckCardName)
			foundToken = True

		match = re.search('[Cc]reate(s)? [a-zX]+ colorless Treasure artifact token(s)?', oracleText)
		if (match):
			appendListInMap(tokens, "colorless Treasure artifact token with \"{T}, Sacrifice this artifact: Add one mana of any color to your mana pool.\"", deckCardName)
			foundToken = True

		match = re.search('[Cc]reate(s)? [a-zX]+ colorless artifact token(s)? named Gold', oracleText)
		if (match):
			appendListInMap(tokens, "colorless Gold artifact token with \"Sacrifice this artifact: Add one mana of any color to your mana pool.\"", deckCardName)
			foundToken = True

		match = re.search('[Cc]reate a token that\'s a copy of', oracleText)
		if (match):
			appendListInMap(tokens, "Copy token", deckCardName)
			foundToken = True

#non tokens and counters

		match = re.search('([sS]oulbond)', oracleText)
		if (match):
			appendListInMap(misc, "Soulbond marker", deckCardName)

		match = re.search('([Pp]rowess)', oracleText)
		if (match):
			appendListInMap(misc, "Prowess marker", deckCardName)

		match = re.search('([aA]scend)', oracleText)
		if (match):
			appendListInMap(misc, "City's Blessing marker", deckCardName)

		match = re.search('({E})', oracleText)
		if (match):
			appendListInMap(counters, "Energy counter", deckCardName)

		match = re.search('(Exert)', oracleText)
		if (match):
			appendListInMap(misc, "Exert marker", deckCardName)

		match = re.search('(Embalm)', oracleText)
		if (match):
			appendListInMap(misc, "Embalm marker", deckCardName)

		plusCounterKeywords = {'Riot', 'Adapt', 'Mentor', 'Explore', 'Monstrosity', 'Support', 'Awaken', 'Amplify', 'Bloodthirst', 'Dethrone', 'Modular', 'Devour', 'Renown', 'Scavenge', 'Sunburst', 'Undying', 'Unleash', 'Outlast', 'Reinforce'}
		addCounter("+1/+1 counter", plusCounterKeywords, counters, oracleText, deckCardName)

		match = re.search('(Cumulative upkeep)', oracleText)
		if (match):
			appendListInMap(tokens, "Age counter", deckCardName)

		addCounter("Time counter", {'Vanishing', 'Suspend'}, counters, oracleText, deckCardName)

		addCounter("Poison counter", {'Poisonous', 'Infect'}, counters, oracleText, deckCardName)

		minusCounterKeywords = { 'Infect', 'Wither', 'Persist'}
		addCounter("-1/-1 counter", minusCounterKeywords, counters, oracleText, deckCardName)

		match = re.search('(Living weapon)', oracleText)
		if (match):
			appendListInMap(tokens, "0/0 black Germ creature token", deckCardName)

		match = re.search('(Storm)', oracleTextWithoutCardName)
		if (match):
			appendListInMap(counters, "Storm counter", deckCardName)

		for match in re.finditer('([\+\-]1/[\+\-]1 [Cc]ounter)', oracleText):
			appendListInMap(counters, match.string[match.start(1):match.end(1)], deckCardName)

		badMatches = {'and counter', 'another counter', 'be counter', 'get counter', 'have counter', 'is counter', 'more counter', 'no counter', 'of counter', 'the counter', 'those counter', 'with counter'}
		for match in re.finditer('([A-Za-z][a-z]+ [Cc]ounter)', oracleText):
			counter = match.string[match.start(1):match.end(1)]
			if (counter.lower() not in badMatches):
				appendListInMap(counters, counter, deckCardName)

		match = re.search('(Legendary Planeswalker)', typeLine)
		if (match):
			appendListInMap(counters, "Loyalty counter", deckCardName)

		for match in re.finditer('(You get an emblem with .+)', oracleText):
			appendListInMap(misc, match.string[match.start(1):match.end(1)], deckCardName)

		if (not foundToken):
			match = re.search("(token)", oracleText)
			if (match):
				tokenCandidates[deckCardName] = oracleText

	response = {}

	response['tokens'] = tokens
	response['counters'] = counters
	response['misc'] = misc
	response['tokenCandidates'] = tokenCandidates

	return response


def printTokensToConsole(response):

	if (len(response['tokens']) > 0):
		print (console.CGREEN + "Tokens:" + console.CEND)
		for token in sorted(response['tokens']):
			print(token)
			for card in sorted(response['tokens'][token]):
				print('\t', card) 

	if (len(response['counters']) > 0):
		print (console.CGREEN + "Counters:" + console.CEND)
		for token in sorted(response['counters']):
			print(token)
			for card in sorted(response['counters'][token]):
				print('\t', card) 

	if (len(response['misc']) > 0):
		print (console.CGREEN + "Other:" + console.CEND)
		for token in sorted(response['misc']):
			print(token)
			for card in sorted(response['misc'][token]):
				print('\t', card) 

	if (len(response['tokenCandidates']) > 0):
		print (console.CGREEN + "Missed token cards:" + console.CEND)
		for candidate in sorted(response['tokenCandidates']):
			print(console.CRED + candidate + console.CEND)
			print('\tOracle text:', response['tokenCandidates'][candidate])