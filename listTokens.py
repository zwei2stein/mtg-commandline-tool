import re

import console
from mtgColors import colorIdentity2NiceString
from mtgDeckObject import Deck
from scryfall import getTokenByUrl


def appendListInMap(map_with_lists, key, item):
    key = key.capitalize()
    if key not in map_with_lists:
        map_with_lists[key] = set([])
    map_with_lists[key].add(item)


def addCounter(counterType, keyWords, map_with_lists, oracleText, deckCard):
    for keyWord in keyWords:
        match = re.search('(' + keyWord + ')', oracleText)
        if match:
            appendListInMap(map_with_lists, counterType, deckCard)


def listTokens(deck: Deck):
    tokens = {}
    counters = {}
    other = {}
    tokenCandidates = {}

    for deckCard in deck.simple_card_list():
        oracleText = deckCard.getFullOracleText()
        typeLine = deckCard.getFullTypeLine()

        oracleText = oracleText.replace('nontoken', '~')
        oracleTextWithoutCardName = oracleText.replace(deckCard.getJsonName(), 'CARD_NAME')

        nonTokenCards = {'Intangible Virtue', 'Anointed Procession', 'Outlaws\' Merriment', 'Mascot Exhibition'}

        foundToken = False

        if deckCard.getJsonName() not in nonTokenCards:

            match = re.search("(Fabricate [0-9]+)", oracleText)
            if (match):
                appendListInMap(tokens, "1/1 colorless Servo artifact creature token", deckCard)
                appendListInMap(counters, "+1/+1 counter", deckCard)
                foundToken = True

            match = re.search("(Afterlife [0-9]+)", oracleText)
            if (match):
                appendListInMap(tokens, "1/1 white and black Spirit creature token with flying", deckCard)
                foundToken = True

            match = re.search("([Aa]mass [0-9]+)", oracleText)
            if (match):
                appendListInMap(tokens, "0/0 black Zombie Army creature token", deckCard)
                appendListInMap(counters, "+1/+1 counter", deckCard)
                foundToken = True

            match = re.search("(Embalm)", oracleText)
            if (match):
                subtype = typeLine.split("\u2014", 1)[1].strip()
                appendListInMap(tokens, deckCard.jsonData.get('power', '?') + '/' + deckCard.jsonData.get('toughness',
                                                                                                          '?') + " white " + deckCard.getJsonName() + " " + subtype + " Zombie token",
                                deckCard)
                appendListInMap(other, "Embalm marker", deckCard)
                foundToken = True

            match = re.search('(Eternalize)', oracleText)
            if (match):
                appendListInMap(tokens, "4/4 black " + deckCard.getJsonName() + " Zombie token", deckCard)
                appendListInMap(other, "Eternalize marker", deckCard)
                foundToken = True

            match = re.search("(Encore)", oracleText)
            if (match):
                subtype = typeLine.split("\u2014", 1)[1].strip()
                appendListInMap(tokens, deckCard.jsonData.get('power', '?') + '/' + deckCard.jsonData.get('toughness',
                                                                                                          '?') + " " + deckCard.getJsonName() + " " + subtype + " token",
                                deckCard)
                foundToken = True

            match = re.search('([Mm]orph)', oracleTextWithoutCardName)
            if (match):
                appendListInMap(tokens, "2/2 colorless creature (morph)", deckCard)

            match = re.search('([Mm]anifest)', oracleText)
            if (match):
                appendListInMap(tokens, "2/2 colorless creature (manifest)", deckCard)

            match = re.search("([iI]nvestigate)", oracleText)
            if (match):
                appendListInMap(tokens,
                                "colorless Clue artifact token with \"{2}, Sacrifice this artifact: Draw a card.\"",
                                deckCard)
                foundToken = True

            for match in re.finditer(
                    '[Cc]reate(s)? ([a-zX ]+) (([0-9X]+)/([0-9X]+) ([a-z ]+) ([A-Za-z ]+) ([a-z ]+) token(s)?( with [A-Za-z ]+)?)',
                    oracleText):
                tokenString = match.string[match.start(3):match.end(3)]
                tokenString = re.sub("tokens", "token", tokenString, 1)
                appendListInMap(tokens, tokenString, deckCard)
                foundToken = True

            for match in re.finditer(
                    '[Cc]reate(s)? ([a-zX ]+) (([a-z ]+) ([A-Za-z ]+) ([a-z ]+) token(s)?(\\. It has \"[A-Za-z\\\'\\. ]+\")?)',
                    oracleText):
                tokenString = match.string[match.start(3):match.end(3)]
                tokenString = re.sub("tokens", "token", tokenString, 1)
                appendListInMap(tokens, tokenString, deckCard)
                foundToken = True

            match = re.search('[Cc]reate(s)? [a-zX ]+ Food token(s)?', oracleText)
            if (match):
                appendListInMap(tokens, "Food token", deckCard)
                foundToken = True

            match = re.search('[Cc]reate(s)? [a-zX]+( colorless)? Treasure( artifact)? token(s)?', oracleText)
            if (match):
                appendListInMap(tokens,
                                "colorless Treasure artifact token with \"{T}, Sacrifice this artifact: Add one mana of any color to your mana pool.\"",
                                deckCard)
                foundToken = True

            match = re.search('[Cc]reate(s)? [a-zX]+ colorless artifact token(s)? named Gold', oracleText)
            if (match):
                appendListInMap(tokens,
                                "colorless Gold artifact token with \"Sacrifice this artifact: Add one mana of any color to your mana pool.\"",
                                deckCard)
                foundToken = True

            match = re.search('[Cc]reate a token that\'s a copy of', oracleText)
            if (match):
                appendListInMap(tokens, "Copy token", deckCard)
                foundToken = True

            # non tokens and counters

            match = re.search('([sS]oulbond)', oracleText)
            if (match):
                appendListInMap(other, "Soulbond marker", deckCard)

            match = re.search('([Pp]rowess)', oracleText)
            if (match):
                appendListInMap(other, "Prowess marker", deckCard)

            match = re.search('(Adventure)', typeLine)
            if (match):
                appendListInMap(other, "On an Adventure marker", deckCard)

            match = re.search('([aA]scend )', oracleText)
            if (match):
                appendListInMap(other, "City's Blessing marker", deckCard)

            match = re.search('({E})', oracleText)
            if (match):
                appendListInMap(counters, "Energy counter", deckCard)

            match = re.search('(devotion to ([a-z]+( and [a-z]+)?))', oracleText)
            if (match):
                appendListInMap(other, "Devotion marker for " + match.string[match.start(2):match.end(2)], deckCard)

            match = re.search('(Exert)', oracleText)
            if (match):
                appendListInMap(other, "Exert marker", deckCard)

            match = re.search('(Embalm)', oracleText)
            if (match):
                appendListInMap(other, "Embalm marker", deckCard)

            plusCounterKeywords = {'Riot', 'Adapt', 'Mentor', 'Explore', 'Monstrosity', 'Support', 'Awaken', 'Amplify',
                                   'Bloodthirst', 'Dethrone', 'Modular', 'Devour', 'Renown', 'Scavenge', 'Sunburst',
                                   'Undying', 'Unleash', 'Outlast', 'Reinforce'}
            addCounter("+1/+1 counter", plusCounterKeywords, counters, oracleText, deckCard)

            match = re.search('(Cumulative upkeep)', oracleText)
            if (match):
                appendListInMap(counters, "Age counter", deckCard)

            addCounter("Time counter", {'Vanishing', 'Suspend'}, counters, oracleText, deckCard)

            addCounter("Poison counter", {'Poisonous', 'Infect'}, counters, oracleText, deckCard)

            minusCounterKeywords = {'Infect', 'Wither', 'Persist'}
            addCounter("-1/-1 counter", minusCounterKeywords, counters, oracleText, deckCard)

            match = re.search('(Living weapon)', oracleText)
            if (match):
                appendListInMap(tokens, "0/0 black Germ creature token", deckCard)

            match = re.search('(Storm)', oracleTextWithoutCardName)
            if (match):
                appendListInMap(other, "Storm count marker", deckCard)

            for match in re.finditer('([\+\-]\d/[\+\-]\d [Cc]ounter)', oracleText):
                appendListInMap(counters, match.string[match.start(1):match.end(1)], deckCard)

            badMatches = {'control counter', 'may counter', 'and counter', 'another counter', 'be counter',
                          'get counter', 'have counter', 'is counter', 'more counter', 'no counter', 'of counter',
                          'the counter', 'those counter', 'with counter'}
            for match in re.finditer('([A-Za-z][a-z]+ [Cc]ounter)', oracleText):
                counter = match.string[match.start(1):match.end(1)]
                if (counter.lower() not in badMatches):
                    appendListInMap(counters, counter, deckCard)

            match = re.search('(Legendary Planeswalker)', typeLine)
            if (match):
                appendListInMap(counters, "Loyalty counter", deckCard)

            for match in re.finditer('(You get an emblem with .+)', oracleText):
                appendListInMap(other, match.string[match.start(1):match.end(1)], deckCard)

            for match in re.finditer('([Rr]oll ([a-zX ]+) (d[0-9]+))', oracleText):
                appendListInMap(other, "Dice: " + match.string[match.start(3):match.end(3)], deckCard)

            for match in re.finditer('([Vv]enture into the dungeon)', oracleText):
                appendListInMap(other, "Dungeon maps", deckCard)

            for match in re.finditer('([Vv]enture into the dungeon)', oracleText):
                appendListInMap(other, "Dungeon maps", deckCard)

            for match in re.finditer('(completed a dungeon)', oracleText):
                appendListInMap(other, "Dungeon completed marker", deckCard)

            match = re.search('(Enchantment \u2014 Class)', typeLine)
            if match:
                appendListInMap(other, "Class level marker", deckCard)

            match = re.search('((becomes day)|(Daybound))', oracleText)
            if match:
                appendListInMap(other, "Day/Night marker", deckCard)

        if (not foundToken):
            match = re.search("(token)", oracleText)
            if (match):
                all_parts = deckCard.jsonData.get('all_parts', [])
                if len(all_parts) == 0:
                    match = re.search("(copy)", oracleText)
                    if (match):
                        appendListInMap(tokens, "Copy token", deckCard)
                else:
                    for part in all_parts:
                        if part['component'] == 'token':
                            tokenJson = getTokenByUrl(part['uri'])
                            if tokenJson is not None:
                                # 1/1 colorless Servo artifact creature token
                                tokenString = tokenJson.get('power', '?') + '/' + tokenJson.get(
                                    'toughness', '?') + ' ' + colorIdentity2NiceString(
                                    tokenJson['color_identity']) + ' ' + \
                                              tokenJson[
                                                  'name'] + ' ' + re.sub(" \u2014 .+", '',
                                                                         tokenJson['type_line'].replace('Token ',
                                                                                                        '')) + ' token'
                                if tokenJson['oracle_text']:
                                    tokenString = tokenString + ' with \'' + tokenJson['oracle_text'].replace('\n',
                                                                                                              ' ') + '\''
                                appendListInMap(tokens, tokenString, deckCard)

    response = dict()

    response['tokens'] = tokens
    response['counters'] = counters
    response['other'] = other
    response['tokenCandidates'] = tokenCandidates

    return response


def printTokensToConsole(response):
    if len(response['tokens']) > 0:
        print(console.CGREEN + "Tokens:" + console.CEND)
        for token in sorted(response['tokens']):
            print(token)
            for card in sorted(response['tokens'][token]):
                print('\t', card)

    if len(response['counters']) > 0:
        print(console.CGREEN + "Counters:" + console.CEND)
        for token in sorted(response['counters']):
            print(token)
            for card in sorted(response['counters'][token]):
                print('\t', card)

    if len(response['other']) > 0:
        print(console.CGREEN + "Other:" + console.CEND)
        for token in sorted(response['other']):
            print(token)
            for card in sorted(response['other'][token]):
                print('\t', card)

    if len(response['tokenCandidates']) > 0:
        print(console.CGREEN + "Missed token cards:" + console.CEND)
        for candidate in sorted(response['tokenCandidates']):
            print(console.CRED + candidate + console.CEND)
            print('\tOracle text:', response['tokenCandidates'][candidate])
