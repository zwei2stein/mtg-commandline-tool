def deckComplexity(deckCards):
    totalWordCount = 0
    cardCount = 0

    for deckCardName, deckCard in deckCards.items():
        oracleText = deckCard.getFullOracleText()
        oracleText.replace(deckCardName, 'CARD_NAME')
        cardCount = cardCount + deckCard.count
        totalWordCount = totalWordCount + len(oracleText.split()) * deckCard.count

    response = {"complexity": int(totalWordCount / cardCount)}

    return response


def printDeckComplexityConsole(response):
    print('Deck complexity index:', response["complexity"])
