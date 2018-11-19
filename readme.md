
MTG Commandline tool
====================

This is tool for handling decklists and card collection.

Key uses:
---------

 * Maintain refence of available cards, aid for physical storage.
 * Help to build decks from available cards.
 * Querry about additional infomation about decks to create detailed reports.

Example:
--------

### List tokens and counters that given deck interacts with:

$ python ./tool/mtg.py -lt -d decklists/Pauper\ Elves.lst
Sideboard found
Listing tokens for deck:
Tokens:
1/1 green elf warrior creature token
         Lys Alana Huntmaster
2/2 colorless creature
         Birchlore Rangers
Counters:
+1/+1 counter
         Elvish Vanguard






TODO:

 * sort by set (by set)

 * normalize deck file.

 * Diff decks

 * reforma verifyDeck