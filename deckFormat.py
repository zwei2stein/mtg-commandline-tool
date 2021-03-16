import console
import deckStatistics

formatList = ["commander", "duel", "future", "legacy", "modern", "pauper", "penny", "standard", "vintage", "oldschool",
              "pioneer"]

singletonFormats = {
    "commander": True,
    "duel": True,
    "future": False,
    "legacy": False,
    "modern": False,
    "pauper": False,
    "penny": False,
    "standard": False,
    "vintage": False,
    "oldschool": False,
    "pioneer": False
}

requiresCommander = {
    "commander": True,
    "duel": True,
    "future": False,
    "legacy": False,
    "modern": False,
    "pauper": False,
    "penny": False,
    "standard": False,
    "vintage": False,
    "oldschool": False,
    "pioneer": False
}

minCardCount = {
    "commander": 100,
    "duel": 100,
    "future": 60,
    "legacy": 60,
    "modern": 60,
    "pauper": 60,
    "penny": 60,
    "standard": 60,
    "vintage": 60,
    "oldschool": 40,
    "pioneer": 60
}

maxSideboardSize = {
    "commander": 0,
    "duel": 0,
    "future": 15,
    "legacy": 15,
    "modern": 15,
    "pauper": 15,
    "penny": 15,
    "standard": 15,
    "vintage": 15,
    "oldschool": 15,
    "pioneer": 15
}

specificityOfFormat = {
    "standard": 10,
    "modern": 9,
    "pioneer": 8,
    "pauper": 7,
    "penny": 6,
    "commander": 5,
    "EDH": 5,
    "duel": 4,
    "vintage": 2,
    "legacy": 1,
    "oldschool": 0,
    "future": -1
}

budgetPrice = {
    "standard": 50,
    "modern": 100,
    "pauper": 20,
    "penny": 5,
    "commander": 50,
    "duel": 100,
    "vintage": 500,
    "legacy": 500,
    "oldschool": 500,
    "future": -1,
    "pioneer": 75
}


def canBeCommander(card):
    commander_legality = card.jsonData.get('legalities', {}).get("commander", "not_legal")
    if commander_legality in ['not_legal', 'banned']:
        return False

    face_types = card.jsonData.get('type_line', '').split("//")
    face_type = face_types[0]
    types_split = face_type.strip().split("\u2014")
    if len(types_split) > 1:
        if "Creature" not in types_split[0] or "Legendary" not in types_split[0]:
            return False

    return True


def getDeckFormat(deck, watch_format=None):
    invalid_watch_cards = {}
    invalid_watch_deck = []

    formats = {
        "commander": True,
        "duel": True,
        "future": True,
        "legacy": True,
        "modern": True,
        "pauper": True,
        "penny": True,
        "standard": True,
        "vintage": True,
        "oldschool": True,
        "pioneer": True
    }

    for deckCardName in deck:
        deck_card = deck[deckCardName]
        legalities = deck_card.jsonData.get('legalities', {})
        for deck_format in formats:
            # We assume that if legality information is not available, then it is not legal
            legality = legalities.get(deck_format, "not_legal")
            if legality in ['not_legal', 'banned']:
                if deck_format == watch_format:
                    invalid_watch_cards[deckCardName] = legality
                formats[deck_format] = False

    isDeckSingleton = deckStatistics.getIsDeckSingleton(deck)['isDeckSingleton']
    deckCardCount = deckStatistics.getDeckCardCount(deck)

    for deck_format in formats:
        if not isDeckSingleton and singletonFormats[deck_format] is True:
            if deck_format == watch_format:
                invalid_watch_deck.append("not singleton")
            formats[deck_format] = False
        if deckCardCount["count"] + deckCardCount["commander"] < minCardCount[deck_format]:
            if deck_format == watch_format:
                invalid_watch_deck.append("too few main deck cards")
            formats[deck_format] = False
        if requiresCommander[deck_format] and deckCardCount["commander"] < 1:
            if deck_format == watch_format:
                invalid_watch_deck.append("missing commander")
            formats[deck_format] = False
        if maxSideboardSize[deck_format] < deckCardCount["sideboardCount"]:
            if deck_format == watch_format:
                invalid_watch_deck.append("too many sideboard cards")
            formats[deck_format] = False

    return {'formats': formats, 'invalidWatchCards': invalid_watch_cards, 'invalidWatchDeck': invalid_watch_deck,
            'watchFormat': watch_format}


def printDetDeckFormatToConsole(response, only_inspect=False):
    formats = response['formats']

    if not only_inspect:

        print("Deck valid for format:")
        for deck_format in sorted(formats, key=lambda k: specificityOfFormat[k], reverse=True):
            if formats[deck_format]:
                print("\t* ", console.CGREEN + deck_format + console.CEND)

        print("Deck " + console.CRED + "not" + console.CEND + " valid for format:")
        for deck_format in sorted(formats, key=lambda k: specificityOfFormat[k], reverse=True):
            if not formats[deck_format]:
                print("\t* ", console.CRED + deck_format + console.CEND)

    watchFormat = response['watchFormat']

    if watchFormat is not None and formats[watchFormat] is False:
        print('Deck is not valid in ' + watchFormat + ' format because:')
        for reason in response['invalidWatchDeck']:
            print('\t* ' + console.CRED + reason + console.CEND)
        for card in response['invalidWatchCards']:
            print('\t* ' + card + ' is ' + console.CRED + response['invalidWatchCards'][card] + console.CEND)
    elif watchFormat is not None and formats[watchFormat] is True:
        print('Deck is valid in ' + watchFormat + ' format without issues.')
