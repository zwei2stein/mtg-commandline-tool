import difflib
import io
import mtgCardTextFileDao
import mtgCardInCollectionObject
import console

def diff (deck1, deck2):

	originalSort = mtgCardInCollectionObject.CardInCollection.args.sort

	groups = ['shortType']

	sort = ['shortType', 'name']

	mtgCardInCollectionObject.CardInCollection.args.sort = sort

	deck1Pretty = io.StringIO()
	mtgCardTextFileDao.saveCardFile(deck1Pretty, deck1, groups, diffFormat=True)

	deck2Pretty = io.StringIO()
	mtgCardTextFileDao.saveCardFile(deck2Pretty, deck2, groups, diffFormat=True)

	previousLine = None
	sameCount = 1
	result = []
	for line in difflib.unified_diff(deck1Pretty.getvalue().split('\n'), deck2Pretty.getvalue().split('\n'), n=1000):

		if (line.startswith('+++') or line.startswith('---') or line.startswith('@@')):
			continue
		if (len(line.strip()) == 0):
			result.append('')
		elif (previousLine != line):
			result.append(line)
			sameCount = 1
			previousLine = line
		else:
			sameCount += 1
			marker = line[0]
			result[-1] = marker + str(sameCount) + " " + line[2:].split(" ", 1)[1]

	for line in result:
		if (line.startswith('+')):
			print (console.CGREEN + line + console.CEND)
		elif (line.startswith('-')):	
			print (console.CRED + line + console.CEND)
		else:
			print (line)

	if (len(result) == 0):
		print (console.CGREEN + "Decks are identical" + console.CEND)
		
	deck1Pretty.close()
	deck2Pretty.close()

	mtgCardInCollectionObject.CardInCollection.args.sort = originalSort