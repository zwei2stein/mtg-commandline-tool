
MTG Commandline tool
====================

This is tool for handling decklists and card collection.

## Key uses:
------------

 * Maintain refence of available cards, aid for physical storage.
 * Help to build decks from available cards.
 * Querry about additional infomation about decks and cards you own to create detailed reports.

## Examples:
------------

### List tokens and counters that given deck interacts with:

`$ python ./tool/mtg.py -lt -d ./decklists/PauperElves.lst`

### Create shopping list with prices for deck you want to build:

`$ python ./tool/mtg.py -mc -d ./decklists/PauperElves.lst -pp`

### Reformat deck file to be pretty (group by card types) and include card prices in tix

`$ python ./tool/mtg.py -cd ./decklists/PauperElves.lst -sl console -s name -g type -pp -c tix`

### Draw sample hand from deck

`$ python ./tool/mtg.py -d ./decklists/PauperElves.lst -draw 7`

### Show Differences between two decks (- is from first deck, + is from seccond deck)

`$ python ./tool/mtg.py -d ./decklists/PauperMonoWhiteHeroic_Instant.txt -diff ./decklists/PauperMonoWhiteHeroic_Aura.txt`

### Print price of each deck in speificed directory

`$ python ./tool/mtg.py -d ./decklists/comanders_quaters/ -dp --currency eur`

## Setup:
---------

First, you need plain text files with your cards and decks.

You can get that done in several ways:

 * If you have precons and your own decks, you can find decklists for them
 * You can scan your collection with app like http://app.tcgplayer.com/. This app allows you to share list of scanned cards with another app. Share it with email client and you can mail it to yourself. Share it with dropbox and it will create file.

 * You can also just add cards manually. And yes, it is going to take some time. It sucks if you want to use this tool. Sorry.

 * Tip: you can put deck list with minus values to indicate that cards were removed from collection to build that deck.

## File format:
---------------

This tools is able to read most plain text files with deck/card lists.

Most commonly, you want you files to follow this pattern:

X Card Name
X Another Card Name # Comment for this card.

Where "X" is how many cards there are and "Card Name" is name of card - this name should match scryfall name, be capitalized properly and should be its english name. 

Line starting with "Sideboard" denotes sideboard separator and every card following that line will be considered part of sideboard.

Lines starting with # are comments.

Other formats (x after card count), (Collectro number) after card name and [set] after card name are loosely supported.

### Example of card file:

```
4 Timberwatch Elf
4 Lys Alana Huntmaster
4 Priest of Titania # replace, too weak
3 Nettle Sentinel
```

### Another example:

```
4x Birchlore Rangers
4x Quirion Ranger
4x Wellwisher
2x Essence Warden (106) [CMA]
4 Lead the Stampede
13 Forest

Sideboard:

2 Electrickery
2 Scattershot Archer
```

## TODO:

 * sort by set (by set)

 * normalize deck file.

 * reformat verifyDeck code

 * fix print price for deck

 * smart set choice for group by / order

 * Refactor console output

 * missing cards - better handle minus counts for cards.

 * commander marker support

 ---

3) Most expensive 4x card - $.

4) Most expensive 4x card - mana.

5) Most common keyword

6) Most common edition

7) Total deck price (penny, budget)

8) Card complexity (% keywords / abilities on cards), (beginner, simple)