import re

import console
import mtgCardInCollectionObject
from mtgColors import colorIdentity2NiceString
from mtgDeckObject import Deck
from scryfall import getTokenByUrl


def appendListInMap(map_with_lists, key, item):
    #key = key.capitalize()
    if key not in map_with_lists:
        map_with_lists[key] = set([])
    map_with_lists[key].add(item)


def addCounter(counterType, keyWords, map_with_lists, oracleText, deckCard):
    for keyWord in keyWords:
        match = re.search('(' + keyWord + ')', oracleText)
        if match:
            appendListInMap(map_with_lists, counterType, deckCard)


pseudo_card_cache = {}


def pseudo_card(card_name, template):
    if card_name not in pseudo_card_cache:
        pseudo_card_cache[card_name] = mtgCardInCollectionObject.CardInCollection(card_name, 1, None,
                                                                                  context=template.context)
    return pseudo_card_cache[card_name]


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

        found_token = False

        if deckCard.getJsonName() not in nonTokenCards:

            match = re.search("(Fabricate [0-9]+)", oracleText)
            if match:
                appendListInMap(tokens, "1/1 colorless Servo artifact creature token", deckCard)
                appendListInMap(counters, "+1/+1 counter", deckCard)
                found_token = True

            match = re.search("(Afterlife [0-9]+)", oracleText)
            if match:
                appendListInMap(tokens, "1/1 white and black Spirit creature token with flying", deckCard)
                found_token = True

            match = re.search("([Aa]mass [0-9]+)", oracleText)
            if match:
                appendListInMap(tokens, "0/0 black Zombie Army creature token", deckCard)
                appendListInMap(counters, "+1/+1 counter", deckCard)
                found_token = True

            match = re.search("[Aa]mass ([A-Z][a-z]+) [0-9]+", oracleText)
            if match:
                type = match.string[match.start(1):match.end(1)-1]
                appendListInMap(tokens, f"0/0 black {type} Army creature token", deckCard)
                appendListInMap(counters, "+1/+1 counter", deckCard)
                found_token = True

            match = re.search("(Embalm)", oracleText)
            if match:
                subtype = typeLine.split("\u2014", 1)[1].strip()
                appendListInMap(tokens, deckCard.jsonData.get('power', '?') + '/' + deckCard.jsonData.get('toughness',
                                                                                                          '?') + " white " + deckCard.getJsonName() + " " + subtype + " Zombie token",
                                deckCard)
                appendListInMap(other, "Embalm marker", deckCard)
                found_token = True

            match = re.search('(Eternalize)', oracleText)
            if match:
                appendListInMap(tokens, "4/4 black " + deckCard.getJsonName() + " Zombie token", deckCard)
                appendListInMap(other, "Eternalize marker", deckCard)
                found_token = True

            match = re.search("(Encore)", oracleText)
            if match:
                subtype = typeLine.split("\u2014", 1)[1].strip()
                appendListInMap(tokens, deckCard.jsonData.get('power', '?') + '/' + deckCard.jsonData.get('toughness',
                                                                                                          '?') + " " + deckCard.getJsonName() + " " + subtype + " token",
                                deckCard)
                found_token = True

            match = re.search('([Mm]orph)', oracleTextWithoutCardName)
            if match:
                appendListInMap(tokens, "2/2 colorless creature (morph)", deckCard)

            match = re.search('([Mm]anifest)', oracleText)
            if match:
                appendListInMap(tokens, "2/2 colorless creature (manifest)", deckCard)

            match = re.search('([Dd]isguise)|([Cc]loak)', oracleTextWithoutCardName)
            if match:
                appendListInMap(tokens, "2/2 creature with ward {2} (disguise)", deckCard)


            match = re.search("([iI]nvestigate)", oracleText)
            if match:
                appendListInMap(tokens,
                                "colorless Clue artifact token with \"{2}, Sacrifice this artifact: Draw a card.\"",
                                deckCard)
                found_token = True

            # 1, define list of regexes that return tokens

            # Create a 2/2 white Astartes Warrior creature token with vigilance
            freeform_token_regex = {
                '[Cc]reate(s)? ([a-zX ]+) (([0-9X]+)/([0-9X]+) ([a-z ]+) ([A-Za-z ]+) ([a-z ]+) token(s)?( named [A-Za-z ]+ with ["{},:A-Za-z0-9 .]+)?( with ["{},:A-Za-z0-9 .]+ named [A-Za-z ]+)?)',
                '[Cc]reate(s)? ([a-zX ]+) (([0-9X]+)/([0-9X]+) ([a-z ]+) ([A-Za-z ]+) ([a-z ]+) token(s)?( named [A-Za-z ]+)?)',
                '[Cc]reate(s)? ([a-zX ]+) (([0-9X]+)/([0-9X]+) ([a-z ]+) ([A-Za-z ]+) ([a-z ]+) token(s)?( with ["{},:A-Za-z0-9 .]+)?)',
                '[Cc]reate(s)? ([a-zX ]+) (([a-z ]+) ([A-Za-z ]+) ([a-z ]+) token(s)?( named [A-Za-z ]+ with ["{},:A-Za-z .]+)?(\\. It has \"[,A-Za-z\\\'\\. ]+\")?)',
                '[Cc]reate(s)? ([a-zX ]+) (([A-Za-z ]+) ([a-z ]+) token(s)?( named [A-Za-z ]+ with ["{}:,A-Za-z0-9 .]+)?)',
                '[Cc]reate(s)? ([a-zX ]+) (([A-Za-z ]+) ([a-z ]+) token(s)?( named [A-Za-z ]+)?)'
            }

            # 2, find for each in oracle text

            freeform_token_candidates = []

            for regex in freeform_token_regex:
                for match in re.finditer(regex, oracleText):
                    token_string = match.string[match.start(3):match.end(3)]
                    token_string = re.sub("tokens", "token", token_string, 1)
                    freeform_token_candidates.append(token_string)
                    found_token = True

            # 3, if one of candidates is substring of another, ignore it.
            #    correct result will only have one substring - itself.

            for candidate in freeform_token_candidates:
                if len(list(filter(lambda x: candidate in x, freeform_token_candidates))) == 1:
                    appendListInMap(tokens, candidate, deckCard)

            match = re.search('[Cc]reate(s)? [a-zX ]+ Food token(s)?', oracleText)
            if match:
                appendListInMap(tokens, "Food token", deckCard)
                found_token = True

            match = re.search('[Cc]reate(s)? [a-zX]+( colorless)? Treasure( artifact)? token(s)?', oracleText)
            if match:
                appendListInMap(tokens,
                                "colorless Treasure artifact token with \"{T}, Sacrifice this artifact: Add one mana of any color to your mana pool.\"",
                                deckCard)
                found_token = True

            match = re.search('[Cc]reate(s)? [a-zX]+ colorless artifact token(s)? named Gold', oracleText)
            if match:
                appendListInMap(tokens,
                                "colorless Gold artifact token with \"Sacrifice this artifact: Add one mana of any color to your mana pool.\"",
                                deckCard)
                found_token = True

            match = re.search('[Cc]reate a token that\'s a copy of', oracleText)
            if match:
                appendListInMap(tokens, "Copy token", deckCard)
                found_token = True

            match = re.search('Mobilize \\d+', oracleText)
            if match:
                appendListInMap(tokens, "1/1 red Warrior creature token", deckCard)
                found_token = True

            match = re.search('[Ee]ndures ([X0-9]+)', oracleText)
            if match:
                pt = match.string[match.start(1):match.end(1)]
                appendListInMap(tokens, f"{pt}/{pt} white Spirit creature token", deckCard)
                found_token = True

            match = re.search('Job select', oracleText)
            if match:
                appendListInMap(tokens, "1/1 colorless Hero creature token", deckCard)
                found_token = True

            match = re.search('Gift a Food', oracleText)
            if match:
                appendListInMap(tokens, "Food token", deckCard)
                found_token = True

            match = re.search('Gift a tapped Fish', oracleText)
            if match:
                appendListInMap(tokens, "1/1 blue Fish creature token", deckCard)
                found_token = True

            match = re.search('Gift a tapped Fish', oracleText)
            if match:
                appendListInMap(tokens, "1/1 blue Fish creature token", deckCard)
                found_token = True

            match = re.search('Gift a Octopus', oracleText)
            if match:
                appendListInMap(tokens, "8/8 blue Octopus creature token", deckCard)
                found_token = True

            match = re.search('Gift a Treasure', oracleText)
            if match:
                appendListInMap(tokens,
                                "colorless Treasure artifact token with \"{T}, Sacrifice this artifact: Add one mana of any color to your mana pool.\"",
                                deckCard)
                found_token = True

            # non tokens and counters

            match = re.search('([sS]oulbond)', oracleText)
            if match:
                appendListInMap(other, "Soulbond marker", deckCard)

            match = re.search('([Pp]rowess)', oracleText)
            if match:
                appendListInMap(other, "Prowess marker", deckCard)

            match = re.search('(Adventure)', typeLine)
            if match:
                appendListInMap(other, "On an Adventure marker", deckCard)

            match = re.search('(Room)', typeLine)
            if match:
                appendListInMap(other, "Locked door marker", deckCard)

            match = re.search('[Rr]ing tempts you', oracleText)
            if match:
                appendListInMap(other, "The Ring marker", deckCard)

            match = re.search('([aA]scend )', oracleText)
            if match:
                appendListInMap(other, "City's Blessing marker", deckCard)

            match = re.search('({E})', oracleText)
            if match:
                appendListInMap(counters, "Energy counter", deckCard)

            match = re.search('(devotion to ([a-z]+( and [a-z]+)?))', oracleText)
            if match:
                appendListInMap(other, "Devotion marker for " + match.string[match.start(2):match.end(2)], deckCard)

            match = re.search('(Exert)', oracleText)
            if match:
                appendListInMap(other, "Exert marker", deckCard)

            match = re.search('([Ss]uspect )', oracleText)
            if match:
                appendListInMap(other, "Suspect marker", deckCard)

            match = re.search('(Embalm)', oracleText)
            if match:
                appendListInMap(other, "Embalm marker", deckCard)

            plusCounterKeywords = {'Endures', 'Riot', 'Adapt', 'Mentor', 'Explore', 'Monstrosity', 'Support', 'Awaken', 'Amplify',
                                   'Bloodthirst', 'Dethrone', 'Modular', 'Devour', 'Renown', 'Scavenge', 'Sunburst',
                                   'Undying', 'Unleash', 'Outlast', 'Reinforce'}
            addCounter("+1/+1 counter", plusCounterKeywords, counters, oracleText, deckCard)

            match = re.search('(Cumulative upkeep)', oracleText)
            if match:
                appendListInMap(counters, "Age counter", deckCard)

            match = re.search('Battle', typeLine)
            if match:
                appendListInMap(counters, "Defense counter", deckCard)

            addCounter("Time counter", {'Vanishing', 'Suspend'}, counters, oracleText, deckCard)

            addCounter("Poison counter", {'Poisonous', 'Infect'}, counters, oracleText, deckCard)

            minusCounterKeywords = {'Infect', 'Wither', 'Persist'}
            addCounter("-1/-1 counter", minusCounterKeywords, counters, oracleText, deckCard)

            match = re.search('(Living weapon)', oracleText)
            if match:
                appendListInMap(tokens, "0/0 black Germ creature token", deckCard)

            match = re.search('(Storm)', oracleTextWithoutCardName)
            if match and deckCard.getJsonName() not in ["Attempted Murder"]:
                appendListInMap(other, "Storm count marker", deckCard)

            match = re.search('(Flurry)', oracleTextWithoutCardName)
            if match:
                appendListInMap(other, "Storm count marker", deckCard)

            for match in re.finditer('([+\\-]\\d/[+\\-]\\d [Cc]ounter)', oracleText):
                appendListInMap(counters, match.string[match.start(1):match.end(1)], deckCard)

            badMatches = {'control counter', 'may counter', 'and counter', 'another counter', 'be counter',
                          'get counter', 'have counter', 'is counter', 'more counter', 'no counter', 'of counter',
                          'the counter', 'those counter', 'with counter', 'all counter'}
            for match in re.finditer('([A-Za-z][a-z]+ [Cc]ounter)', oracleText):
                counter = match.string[match.start(1):match.end(1)]
                if (counter.lower() not in badMatches):
                    appendListInMap(counters, counter, deckCard)

            match = re.search('(Legendary Planeswalker)', typeLine)
            if match:
                appendListInMap(counters, "Loyalty counter", deckCard)

            for match in re.finditer('(You get an emblem with .+)', oracleText):
                appendListInMap(other, match.string[match.start(1):match.end(1)], deckCard)

            for match in re.finditer('([Rr]oll ([a-zX ]+) (d[0-9]+))', oracleText):
                appendListInMap(other, "Dice: " + match.string[match.start(3):match.end(3)], deckCard)

            for match in re.finditer('(Roll a six-sided die)', oracleText):
                appendListInMap(other, "Dice: d6", deckCard)


            for match in re.finditer('([Vv]enture into the dungeon)', oracleText):
                appendListInMap(other, "Dungeon of the Mad Mage,", deckCard)
                appendListInMap(other, "Lost Mine of Phandelver", deckCard)
                appendListInMap(other, "Tomb of Annihilation", deckCard)
                # implied by the dungeons:
                appendListInMap(tokens,
                                "colorless Treasure artifact token with \"{T}, Sacrifice this artifact: Add one mana of any color to your mana pool.\"",
                                pseudo_card("Dungeon of the Mad Mage", deckCard))
                appendListInMap(tokens,
                                "1/1 black Skeleton creature token",
                                pseudo_card("Dungeon of the Mad Mage", deckCard))
                appendListInMap(tokens,
                                "1/1 red Goblin creature token",
                                pseudo_card("Lost Mine of Phandelver", deckCard))
                appendListInMap(tokens,
                                "colorless Treasure artifact token with \"{T}, Sacrifice this artifact: Add one mana of any color to your mana pool.\"",
                                pseudo_card("Lost Mine of Phandelver", deckCard))
                appendListInMap(counters, "+1/+1 counter",
                                pseudo_card("Lost Mine of Phandelver", deckCard))
                appendListInMap(tokens,
                                "The Atropal, a legendary 4/4 black God Horror creature token with deathtouch",
                                pseudo_card("Tomb of Annihilation", deckCard))

            for match in re.finditer('([Yy]ou take the initiative)', oracleText):
                appendListInMap(other, "The Initiative marker ", deckCard)
                appendListInMap(other, "Undercity", deckCard)
                # implied by the dungeon:
                appendListInMap(counters, "+1/+1 counter", pseudo_card("Undercity", deckCard))
                appendListInMap(tokens,
                                "colorless Treasure artifact token with \"{T}, Sacrifice this artifact: Add one mana of any color to your mana pool.\"",
                                pseudo_card("Undercity", deckCard))
                appendListInMap(tokens, "4/1 black Skeleton creature token with menace",
                                pseudo_card("Undercity", deckCard))

            for match in re.finditer('(completed a dungeon)', oracleText):
                appendListInMap(other, "Dungeon completed marker", deckCard)

            match = re.search('(Enchantment \u2014 Class)', typeLine)
            if match:
                appendListInMap(other, "Class level marker", deckCard)

            match = re.search('((becomes day)|(Daybound))', oracleText)
            if match:
                appendListInMap(other, "Day/Night marker", deckCard)

            match = re.search('{TK}', oracleText)
            if match:
                appendListInMap(other, "Ticket Bucket-Bot", deckCard)

            match = re.search('(may put ([a-z ]+)?( (ability)|(name)|(art))? sticker(s)? on)', oracleText)
            if match:
                appendListInMap(other, "Sticker sheet side deck", deckCard)

            match = re.search('[Oo]pen [a-z]+ Attraction(s)?', oracleText)
            if match:
                appendListInMap(other, "Attraction side deck", deckCard)
                appendListInMap(other, "Dice: d6", deckCard)

            match = re.search('(it becomes plotted)|(has plot)|(Plot )', oracleText)
            if match:
                appendListInMap(other, "Ploted marker", deckCard)

            match = re.search('Start your engines!', oracleText)
            if match:
                appendListInMap(other, "Start Your Engines! marker", deckCard)

            match = re.search('(Exhaust)', oracleText)
            if match:
                appendListInMap(other, "Exhaust marker", deckCard)

            match = re.search('(Prototype )', oracleText)
            if match:
                appendListInMap(other, "Prototype marker", deckCard)

        if not found_token:
            match = re.search("(token)", oracleText)
            if match:
                all_parts = deckCard.jsonData.get('all_parts', [])
                if len(all_parts) == 0:
                    match = re.search("(copy)", oracleText)
                    if match:
                        appendListInMap(tokens, "Copy token", deckCard)
                else:
                    for part in all_parts:
                        if part['component'] == 'token':
                            token_json = getTokenByUrl(part['uri'])
                            if token_json is not None:
                                # 1/1 colorless Servo artifact creature token
                                token_string = ''
                                if token_json.get('power', None) or token_json.get('toughness', None):
                                    token_string = token_json.get('power', '?') + '/' + token_json.get('toughness', '?') + ' '

                                token_string = (token_string + colorIdentity2NiceString(
                                    token_json['color_identity']) + ' ' + \
                                              token_json['name'] + ' ' + re.sub(" \u2014 .+", '',
                                                                         token_json['type_line'].replace('Token ',
                                                                                                        '')) + ' token')
                                if token_json.get('oracle_text', None):
                                    token_string = token_string + ' with \'' + token_json['oracle_text'].replace('\n',
                                                                                                              ' ') + '\''
                                appendListInMap(tokens, token_string, deckCard)

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
