def deckComplexity(deckCards):
    totalWordCount = 0
    cardCount = 0

    for deckCardName, deckCard in deckCards.items():
        oracleText = deckCard.getFullOracleText()
        cardCount = cardCount + deckCard.count
        print(oracleText.split())
        totalWordCount = totalWordCount + len(oracleText.split()) * deckCard.count

    response = {"complexity": totalWordCount / cardCount}

    return response


def printDeckComplexityConsole(response):
    print('Deck complexity index:', response["complexity"])
