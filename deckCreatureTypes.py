
def getCreatureTypes(deck):

	creatureTypeCounts = {}


	for deckCardName in deck:
		deckCard = deck[deckCardName]

		faceTypes = deckCard.jsonData.get('type_line', '').split("//")

		for faceType in faceTypes:
			typesSplit = faceType.strip().split("\u2014")

			if (len(typesSplit) > 1):
				if ("Creature" in typesSplit[0]):
					creatureTypes = typesSplit[1].strip().split(" ")
					for creatureType in creatureTypes:
						creatureTypeCounts[creatureType]= deckCard.count + creatureTypeCounts.get(creatureType, 0)

	return creatureTypeCounts

def printnGetCreatureTypes(response):

	for x in sorted(response.items(), key=lambda x: str(100-x[1])+ " " + x[0]):
		print ('\t',x[1], x[0])