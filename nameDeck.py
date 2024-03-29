import mtgColors
import deckFormat
import deckCreatureTypes
import deckStatistics
import deckPrice

from decimal import *

import random

colorPairingNames = {
 'W': ['White', 'Monowhite', 'Mono-white', 'W'],
 'U': ['Blue', 'Monoblue', 'Mono-blue', 'U'],
 'B': ['Black', 'Monoblack', 'Mono-black', 'B'],
 'R': ['Red', 'Monored', 'Mono-red', 'R'],
 'G': ['Green', 'Monogreen', 'Mono-green', 'G'],
 'WU': ['Azorius', 'White/Blue', 'White-Blue', 'WU'],
 'WB': ['Orzhov', 'White/Black', 'White-Black', 'WB'],
 'WR': ['Boros', 'White/Red', 'White-Red', 'WR'],
 'WG': ['Selesnya', 'White/Green', 'White-Green', 'WG'],
 'UB': ['Dimir', 'Blue/Black', 'Blue-Black', 'UB'],
 'UR': ['Izzet', 'Blue/Red', 'Blue-Red', 'UR'],
 'UG': ['Simic', 'Blue/Green', 'Blue-Green', "UG"],
 'BR': ['Rakdos', 'Black/Red', 'Black-Red', 'BR'],
 'BG': ['Golgari', 'Black/Green', 'Black-Green', 'BG'],
 'RG': ['Gruul', 'Red/Green', 'Red-Green', 'RG'],
 'WUB': ['Esper', 'WUB', 'Discipline'],
 'WUR': ['Jeskai', 'Raugrin', 'WUR', 'Raka'],
 'WUG': ['Bant', 'WUG', 'Flourishing'],
 'WBR': ['Mardu', 'Savai', 'WBR', 'Borzhov', 'Dega'],
 'WBG': ['Abzan', 'Indatha', 'WBG', 'Necra'],
 'WRG': ['Naya', 'WRG', 'Passion'],
 'UBR': ['Grixis', 'UBR', 'Insight'],
 'UBG': ['Sultai', 'Zagoth', 'UBG', 'Ana'],
 'URG': ['Temur', 'Ketria', 'URG', 'Grizzet', 'Ceta'],
 'BRG': ['Jund', 'BRG', 'Revival'],
 'WUBR': ['WUBR', 'Artifice'],
 'WUBG': ['WUBG', 'Growth'],
 'WURG': ['WURG', 'Altruism'],
 'WBRG': ['WBRG', 'Aggression'],
 'UBRG': ['UBRG', 'Chaos'],
 'WUBRG': ['Prismatic', '5-Color', 'Multicolor', 'Rainbow', 'Domain'],
 'C': ['Colorless', 'Monobrown', 'Diamond']}

keywordList = ["Abandon", "Absorb", "Actions", "Activate", "Adapt", "Addendum", "Affinity", "Afflict", "Afterlife", "Aftermath", "Amplify", "Annihilator", "Ascend", "Assist", "Attach", "Aura Swap", "Awaken", "Banding", "Battalion", "Battle Cry", "Bestow", "Bloodrush", "Bloodthirst", "Bolster", "Bushido", "Buyback", "Cascade", "Cast", "Champion", "Changeling", "Channel", "Chroma", "Cipher", "Clash", "Cohort", "Conspire", "Constellation", "Converge", "Convoke", "Council's Dilemma", "Counter", "Crew", "Cumulative Upkeep", "Cycling", "Dash", "Deathtouch", "Defender", "Delirium", "Delve", "Destroy", "Detain", "Dethrone", "Devoid", "Devour", "Discard", "Domain", "Double Agenda", "Double Strike", "Double", "Dredge", "Echo", "Embalm", "Emerge", "Eminence", "Enchant", "Enrage", "Entwine", "Epic", "Equip", "Escalate", "Eternalize", "Evergreen", "Evoke", "Evolve", "Exalted", "Exchange", "Exert", "Exile", "Exploit", "Explore", "Extort", "Fabricate", "Fading", "Fateful Hour", "Fateseal", "Fear", "Ferocious", "Fight", "First Strike", "Flanking", "Flash", "Flashback", "Flying", "Forecast", "Formidable", "Fortify", "Frenzy", "Fuse", "Goad", "Graft", "Grandeur", "Gravestorm", "Haste", "Haunt", "Hellbent", "Heroic", "Hexproof", "Hidden Agenda", "Hideaway", "Horsemanship", "Imprint", "Improvise", "Indestructible", "Infect", "Ingest", "Inspired", "Intimidate", "Investigate", "Join Forces", "Jump-Start", "Keyword", "Kicker", "Kinship", "Landfall", "Landwalk", "Level Up", "Lieutenant", "Lifelink", "Living Weapon", "Madness", "Manifest", "Mechanics", "Megamorph", "Meld", "Melee", "Menace", "Mentor", "Metalcraft", "Miracle", "Modular", "Monstrosity", "Morbid", "Morph", "Multikicker", "Myriad", "Ninjutsu", "Offering", "Outlast", "Overload", "Parley", "Partner with", "Partner", "Persist", "Phasing", "Planeswalk", "Play", "Poisonous", "Populate", "Proliferate", "Protection", "Provoke", "Prowess", "Prowl", "Radiance", "Raid", "Rally", "Rampage", "Reach", "Rebound", "Recover", "Regenerate", "Reinforce", "Renown", "Replicate", "Retrace", "Reveal", "Revolt", "Riot", "Ripple", "Scavenge", "Scry", "Set in Motion", "Shadow", "Shroud", "Shuffle", "Skulk", "Soulbond", "Soulshift", "Spectacle", "Spell Mastery", "Splice", "Split Second", "Storm", "Strive", "Sunburst", "Support", "Surge", "Surveil", "Suspend", "Sweep", "Tempting Offer", "Threshold", "Totem Armor", "Trample", "Transfigure", "Transform", "Transmute", "Tribute", "Typecycling", "Undaunted", "Undergrowth", "Undying", "Unearth", "Unleash", "Untap", "Vanishing", "Vigilance", "Vote", "Will of the Council", "Wither", "Words"]

def getKeywords(deck):

	keywords = {}

	for deckCardName in deck:
		deckCard = deck[deckCardName]

		oracleText = deckCard.getFullOracleText()

		for keyword in keywordList:
			if (keyword in oracleText):
				if (keyword in keywords):
					keywords[keyword] = keywords[keyword] + deckCard.count
				else:
					keywords[keyword] = deckCard.count

	keywords = {k: v for k, v in keywords.items() if v >= deckStatistics.getDeckCardCount(deck)["count"]/10}

	return sorted(keywords, key=lambda k: keywords[k], reverse=True)[:2]

def getTribalNames(deck):

	creatureTypes = deckCreatureTypes.getCreatureTypes(deck)

	creatureCount = deckCreatureTypes.getCreatureCount(deck)

	maxCount = 0
	commonTypes = []
	for creatureType in creatureTypes:
		if creatureTypes[creatureType] > maxCount and creatureTypes[creatureType] >= creatureCount / 3:
			maxCount = creatureTypes[creatureType]
			commonTypes = []
		if creatureTypes[creatureType] == maxCount:
			commonTypes.append(creatureType)

	return commonTypes

def prettierCardName(cardName):
	return cardName.replace('The ', '', 1)

def getSignificantCards(deck):

	maxPriceCardPrice = Decimal(0)
	maxPriceCard = None

	maxCmc = 0.0
	maxCmcCard = None

	commanderCard = None

	for deckCardName in deck:
		deckCard = deck[deckCardName]

		price = Decimal(deckCard.jsonData.get("usd", "0.0")) * Decimal(deckCard.count - deckCard.sideboard/3) 
		if (price > maxPriceCardPrice):
			maxPriceCard = prettierCardName(deckCardName)
			maxPriceCardPrice = price

		cmc = deckCard.jsonData.get("cmc", 0.0) * (deckCard.count - deckCard.sideboard/3)
		if (cmc > maxCmc):
			maxCmcCard = prettierCardName(deckCardName)
			maxCmc = cmc

		if (deckCard.commander):
			commanderCard = prettierCardName(deckCardName)

	order = {commanderCard: 1, maxPriceCard: 2, maxCmcCard: 3}

	return sorted(list(dict.fromkeys(filter(None,[commanderCard, maxPriceCard, maxCmcCard]))), key=lambda k: order[k])

def getDeckFormat(deck):

	deckFormats = deckFormat.getDeckFormat(deck)['formats']
	deckFormats = list(filter(lambda k: deckFormats[k] == True, deckFormats))

	if ('commander' in deckFormats):
		deckFormats.append('EDH')
	
	return sorted(deckFormats, key=lambda k: deckFormat.specificityOfFormat[k], reverse=True)[:1];

def getDeckBudget(deck):

	price = deckPrice.deckPrice(deck, 'usd')

	oneDeckFormat = getDeckFormat(deck)

	if (oneDeckFormat == []):
		return []

	if (Decimal(deckFormat.budgetPrice[oneDeckFormat[0]]) > price["totalPrice"]):
		return ['budget']
	else:
		return []

def appendNamed(list, names):
	if (len(names) > 0):
		random.shuffle(names)
		list.append(names[0])


def nameDeck(deck):

	names = []

	appendNamed(names, colorPairingNames[mtgColors.colorIdentity2String((mtgColors.getDeckColorIdentity(deck)))])
	appendNamed(names, getTribalNames(deck))
	appendNamed(names, getDeckFormat(deck))
	appendNamed(names, getKeywords(deck))
	appendNamed(names, getSignificantCards(deck))
	appendNamed(names, getDeckBudget(deck))

	random.shuffle(names)

	names = names[0:3]

	response = {}

	response['names'] = " ".join(names)

	return response


def printnDeckNameToConsole(response):

	print ('Deck names:')

	print ('\t"' + response['names'] + '"')