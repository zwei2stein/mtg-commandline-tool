
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

`$ python ./tool/mtg.py -mc -d ./decklists/PauperElves.lst -p price`

### Reformat deck file to be pretty (group by card types) and include card prices in tix

`$ python ./tool/mtg.py -cd ./decklists/PauperElves.lst -sl console -s name -g type -p price -c tix`

### Draw sample hand from deck

`$ python ./tool/mtg.py -d ./decklists/PauperElves.lst -draw 7`

### Show Differences between two decks (- is from first deck, + is from seccond deck)

`$ python ./tool/mtg.py -d ./decklists/PauperMonoWhiteHeroic_Instant.txt -diff ./decklists/PauperMonoWhiteHeroic_Aura.txt`

### Print price of each deck in speificed directory

`$ python ./tool/mtg.py -d ./decklists/comanders_quaters/ -dp --currency eur`

## Setup:
---------

First, you need plain text files with your collection and decks.

You can get that done in several ways:

 * If you have precons you can find decklists for them.

 * You might have decklists for your own decks already
 
 * You can scan your collection with app like http://app.tcgplayer.com/. This app allows you to share list of scanned cards with another app. Share it with email client and you can mail it to yourself. Share it with dropbox and it will create file.

 * You can also just add cards manually. And yes, it is going to take some time. It sucks if you want to use this tool. Sorry.

 * Tip: you can put deck list with minus values to indicate that cards were removed from collection to build a deck or traded away.

## File format:
---------------

This tools is able to read most plain text files with deck/card lists.

Most commonly, you want you files to follow this pattern:

X Card Name
X Another Card Name # Comment for this card.

Where "X" is how many cards there are and "Card Name" is name of card - this name must match scryfall name, should be capitalized properly and should be its english name. 

Line starting with "Sideboard" denotes sideboard separator and every card following that line will be considered part of sideboard.

Lines starting with # are comments.

Other formats (x after card count), (Collector number) after card name and [set] after card name are loosely supported (=ignored).

### Example of card file:

```
4 Timberwatch Elf
4 Lys Alana Huntmaster
4 Priest of Titania # replace, too weak
3 Nettle Sentinel
```

### Example with sideboard:

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

### Example with commander:

```
Commander:

1 Arcades, the Strategist

1 Angelic Wall
1 Arcades Sabboth
1 Assault Formation
1 Axebane Guardian
```

## Commandline help

```
usage: mtg.py [-h] [-cd COLLECTIONDIRECTORY] [-id] [-fp FILEPATTERN]
              [-c {eur,usd,tix}] [-cache {init,flush}]
              [-clearCache {awlays,4price,timeout,none}]
              (-sl SAVELIST | -d DECK) [-pp] [-pc]
              [-s [{price,cmc,name,count,color,set,type,shortType,rarity} [{price,cmc,name,count,color,set,type,shortType,rarity} ...]]]
              [-g [{price,cmc,name,count,color,set,type,shortType,rarity} [{price,cmc,name,count,color,set,type,shortType,rarity} ...]]]
              [-fl {standard,future,frontier,modern,legacy,pauper,vintage,penny,commander,1v1,duel,brawl}]
              [-ft FILTERTYPE] [-mc] [-lt] [-dp] [-mcu] [-ms] [-lm] [-cc]
              [-is] [-df] [-ct] [-draw DRAWCARDS] [-nd] [-diff DIFF]

Process MTG card plain text lists (decks and collection)

optional arguments:
  -h, --help            show this help message and exit
  -cd COLLECTIONDIRECTORY, --collectionDirectory COLLECTIONDIRECTORY
                        Sets root directory to scan for card collection.
                        Default is './library' directory. Single file
                        representing collection can be specified instead of
                        directory.
  -id, --ignoreDecks    Ignore files with 'deck' in path. Usefull when you
                        store decks along with your collection.
  -fp FILEPATTERN, --filePattern FILEPATTERN
                        Regular expression pattern for files that are
                        considered part of collection. Default is '.*\.txt'
  -c {eur,usd,tix}, --currency {eur,usd,tix}
                        Currency used for sorting by price and for output of
                        price. Default 'eur'
  -cache {init,flush}, --cache {init,flush}
                        Manual cache control: 'init' fetches all cards from
                        collectin from scryfall to cache, 'flush' clears cache
                        directory.
  -clearCache {awlays,4price,timeout,none}, --clearCache {awlays,4price,timeout,none}
                        Determines how is caching from scrycall handled.
                        'always' - always fetch fresh data. 'price' - fetch
                        data if price changes. 'timeout' - fetch data if 365
                        days have passed. 'none' - always use cached version.
                        Default 'none'
  -sl SAVELIST, --saveList SAVELIST
                        Save consolidated list or print it to 'console'
  -d DECK, --deck DECK  Chooses deck file to work on, required for deck tools.
                        If directory is specified, tool will work on each deck
                        file found in directory
  -pp, --printPrice     Add price to output
  -pc, --printColor     Add color identity to output
  -s [{price,cmc,name,count,color,set,type,shortType,rarity} [{price,cmc,name,count,color,set,type,shortType,rarity} ...]], --sort [{price,cmc,name,count,color,set,type,shortType,rarity} [{price,cmc,name,count,color,set,type,shortType,rarity} ...]]
                        Sort list order by. Default 'name'.
  -g [{price,cmc,name,count,color,set,type,shortType,rarity} [{price,cmc,name,count,color,set,type,shortType,rarity} ...]], --group [{price,cmc,name,count,color,set,type,shortType,rarity} [{price,cmc,name,count,color,set,type,shortType,rarity} ...]]
                        Group saved list by given parameter. Always groups
                        sideboards together.
  -fl {standard,future,frontier,modern,legacy,pauper,vintage,penny,commander,1v1,duel,brawl}, --filterLegality {standard,future,frontier,modern,legacy,pauper,vintage,penny,commander,1v1,duel,brawl}
                        Filter result list by format legality. Default is no
                        filter.
  -ft FILTERTYPE, --filterType FILTERTYPE
                        Filter results by type line of card
  -mc, --missingCards   Prints cards missing from given deck file
  -lt, --listTokens     Prints tokens and counters for given deck file
  -dp, --deckPrice      Prints price of given deck file
  -mcu, --manaCurve     Prints mana curve of given deck file
  -ms, --manaSymbols    Prints mana symbols count in casting costs of given
                        deck file
  -lm, --landMana       Prints mana source count of given deck file
  -cc, --cardCount      Gives total count of cards for deck
  -is, --isSingleton    Checks deck if it is singeton
  -df, --deckFormat     Prints formats in which is deck legal
  -ct, --deckCreatureTypes
                        Prints list of creature types in deck with their
                        counts (not including possible tokens)
  -draw DRAWCARDS, --drawCards DRAWCARDS
                        Draw N cards from deck.
  -nd, --nameDeck       Attempts to generate name for given deck
  -diff DIFF, --diff DIFF
                        Diffe deck with another deck.
```

## TODO:

 * sort by set (by set) - better order.

 * set from file

 * normalize deck file.

 * smart set choice for group by / order

 * Refactor console output

 * commander marker support

 ---

3) Most expensive 4x card - $.

4) Most expensive 4x card - mana.

5) Most common keyword

6) Most common edition

7) Total deck price (penny, budget)

8) Card complexity (% keywords / abilities on cards), (beginner, simple)