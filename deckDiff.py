import difflib
import io

import console
import mtgCardTextFileDao
import mtgDeckObject


def diff(deck1, deck2, context):
    original_sort = context.sort

    context.sort = mtgDeckObject.prettyPrintSort

    deck1_pretty = io.StringIO()
    mtgCardTextFileDao.saveCardFile(deck1_pretty, deck1, mtgDeckObject.prettyPrintGroups, context, diffFormat=True)

    deck2_pretty = io.StringIO()
    mtgCardTextFileDao.saveCardFile(deck2_pretty, deck2, mtgDeckObject.prettyPrintGroups, context, diffFormat=True)

    previous_line = None
    same_count = 1
    result = []
    for line in difflib.unified_diff(deck1_pretty.getvalue().split('\n'), deck2_pretty.getvalue().split('\n'), n=1000):

        if line.startswith('+++') or line.startswith('---') or line.startswith('@@'):
            continue
        if len(line.strip()) == 0:
            result.append('')
        elif previous_line != line:
            result.append(line)
            same_count = 1
            previous_line = line
        else:
            same_count += 1
            marker = line[0]
            result[-1] = marker + str(same_count) + " " + line[2:].split(" ", 1)[1]

    for line in result:
        if line.startswith('+'):
            print(console.CGREEN + line + console.CEND)
        elif line.startswith('-'):
            print(console.CRED + line + console.CEND)
        else:
            print(line)

    if len(result) == 0:
        print(console.CGREEN + "Decks are identical" + console.CEND)

    deck1_pretty.close()
    deck2_pretty.close()

    context.sort = original_sort
