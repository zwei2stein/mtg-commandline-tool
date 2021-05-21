
var apiHost = "./";

function inProgress() {
    $('#deckTableTech').show();
    $('#loading').show();
    $('#error').hide();
    $('#deckTable').hide();
    $('#deckTable>tbody').empty();
    $('#possibleDecksTable').hide();
    $('#possibleDecksTable>tbody').empty();

    $('#refresh').prop('disabled', true);
    $('#currency').prop('disabled', true);
    $('#order').prop('disabled', true);
    $('#collection').prop('disabled', true);
    $('#possibleDecks').prop('disabled', true);
}

function cleanUp() {
    $('#loading').hide();

    $('#refresh').prop('disabled', false);
    $('#currency').prop('disabled', false);
    $('#order').prop('disabled', false);
    $('#collection').prop('disabled', false);
    $('#possibleDecks').prop('disabled', false);
}

function reload() {
    inProgress();
    $.ajax({
        url: apiHost + $('#currency').val() + "/" + $('#order').val()  + "/deckPrice.json"
    }).done(function(data) {
        data.forEach(function(item, index) {
            var commanders = '';
            item.commanders.forEach(function (item, index) {
                commanders = commanders + commanderCardLine(item, '');
            });
            item.companions.forEach(function (item, index) {
                commanders = commanders + commanderCardLine(item, 'companion');
            });
            var row = ''
            row = row + '<td class="rank">' + ( index + 1 ) + '</td>';
            row = row + '<td><a onClick="showDeck(\'' + item.deckFile + '\', ' + ( index + 1 ) + ');" title="Decklist">&#128220;</a></td>';
            row = row + '<td><a onClick="showTokens(\'' + item.deckFile + '\', ' + ( index + 1 ) + ');" title="Tokens and counters">&#127922;</a></td>';
            row = row + '<td><a href="/' + item.deckFile + '/deckList.txt" title="Download decklist" target="_blank">&#128190;</a></td>';
            $('#deckTable>tbody').append('<tr>' + row + '<td>'+ commanders +'</td><td>' + item.age + '</td><td>' + item.rank + '</td><td>' + item.complexity + '</td><td class="deckPrice">'+ item.deckPriceTotal +"</td><td>" + $('#currency').val() + "</td></tr>");
            $('#deckTable>tbody').append('<tr id="deckLine' + ( index + 1 ) + '"><td colspan="4"></td><td colspan="3" class="deck">Loading...</td><td colspan="3"></td></tr>');
            $('#deckTable>tbody').append('<tr id="tokenLine' + ( index + 1 ) + '"><td colspan="4"></td><td colspan="3" class="deck">Loading...</td><td colspan="3"></td></tr>');
            $('#deckLine'+ ( index + 1 )).hide();
            $('#tokenLine'+ ( index + 1 )).hide();
        });
        $('#deckTable').show();
    }).fail(function() {
        $('#error').show();
    }).always(function() {
        cleanUp();
    });
}

function possibleDecks() {
    inProgress();
    $.ajax({
        method: "POST",
        url: apiHost + $('#currency').val() + "/possibleDecks.json",
        data: { collection: $('#collection').val() }
    }).done(function(data) {
        data.forEach(function(item, index) {
            var row = '<tr>';

            row = row + '<td class="rank">' + ( index + 1 ) + '</td>';
            row = row + '<td><a onClick="showDeck(\'' + item.deckFile + '\', ' + ( index + 1 ) + ');" title="Decklist">&#128220;</a></td>';
            row = row + '<td><a onClick="showTokens(\'' + item.deckFile + '\', ' + ( index + 1 ) + ');" title="Tokens and counters">&#127922;</a></td>';
            row = row + '<td><a href="/' + item.deckFile + '/deckList.txt" title="Download decklist" target="_blank">&#128190;</a></td>';
            row = row + '<td>';
            item.commanders.forEach(function (item, index) {
                row = row + commanderCardLine(item, '');
            });
            item.companions.forEach(function (item, index) {
                row = row + commanderCardLine(item, 'companion');
            });
            row = row + '</td>';
            row = row + '<td>' + item.printPercentage + '</td>';
            row = row + '<td class="deckPrice">' + item.shoppingListPrice + '</td>';
            row = row + '<td>' + $('#currency').val() + '</td>'

            row = row + '</tr>';

            var deckList = '<h3 id="haveList' + ( index + 1 ) + '" class="folded">Have (' + item.haveListCount + '):</h3><div id="haveListContainer' + ( index + 1 ) + '">';

            item.haveList.forEach(function (item, index) {
                deckList = deckList + '<h3>' + item.shortType + ' (' + item.count + ')</h3><div class="deckCardList">';
                item.cards.forEach(function (item, index) {
                    deckList = deckList + cardLine(item);
                });
                deckList = deckList + '</div>';
            });
            deckList = deckList + '</div>';

            deckList = deckList + '<h3 id="needList' + ( index + 1 ) + '" class="folded">Need (' + item.shoppingListCount + '):</h3><div id="needListContainer' + ( index + 1 ) + '">';

            item.shoppingList.forEach(function (item, index) {
                deckList = deckList + '<h3>' + item.shortType + ' (' + item.count + ')</h3><div class="deckCardList">';
                item.cards.forEach(function (item, index) {
                    deckList = deckList + cardLine(item);
                });
                deckList = deckList + '</div>';
            });
            deckList = deckList + '</div>';

            $('#possibleDecksTable>tbody').append(row);
            $('#possibleDecksTable>tbody').append('<tr id="shoppingListLine' + ( index + 1 ) + '"><td colspan="4"></td><td colspan="3" class="deck">' + deckList + '</td><td colspan="2"></td></tr>');
            $('#possibleDecksTable>tbody').append('<tr id="deckLine' + ( index + 1 ) + '"><td colspan="4"></td><td colspan="3" class="deck">Loading...</td><td colspan="2"></td></tr>');
            $('#possibleDecksTable>tbody').append('<tr id="tokenLine' + ( index + 1 ) + '"><td colspan="4"></td><td colspan="3" class="deck">Loading...</td><td colspan="2"></td></tr>');
            $('#deckLine'+ ( index + 1 )).hide();
            $('#tokenLine'+ ( index + 1 )).hide();

            $('#haveList' + ( index + 1 )).click(function() {
                $('#haveListContainer' + ( index + 1 )).toggle();
                if ($('#haveListContainer' + ( index + 1 )).is(':visible')) {
                    $('#haveList' + ( index + 1 )).addClass('unfolded');
                    $('#haveList' + ( index + 1 )).removeClass('folded');
                } else {
                    $('#haveList' + ( index + 1 )).addClass('folded');
                    $('#haveList' + ( index + 1 )).removeClass('unfolded');
                }
            });
            $('#haveListContainer' + ( index + 1 )).hide();

            $('#needList' + ( index + 1 )).click(function() {
                $('#needListContainer' + ( index + 1 )).toggle();
                if ($('#needListContainer' + ( index + 1 )).is(':visible')) {
                    $('#needList' + ( index + 1 )).addClass('unfolded');
                    $('#needList' + ( index + 1 )).removeClass('folded');
                } else {
                    $('#needList' + ( index + 1 )).addClass('folded');
                    $('#needList' + ( index + 1 )).removeClass('unfolded');
                }
            });
            $('#needListContainer' + ( index + 1 )).hide();

        });
        $('#possibleDecksTable').show();
    }).fail(function() {
        $('#error').show();
    }).always(function() {
        cleanUp();
    });
}

function cardImageRollover(imageUris) {
    if (imageUris) {
        return ' onmouseover="showCardImage([\'' + imageUris.join("','") + '\']);" onmouseout="fadeCardImage();"';
    } else {
        return '';
    }
}

function cardLink(scryfallUri) {
    if (scryfallUri) {
        return ' onclick="window.open(\'' + scryfallUri + '\', \'_blank\')"';
    } else {
        return '';
    }
}

function commanderCardLine(item, aditionalCss) {
    return '<span class="card commander ' + aditionalCss + ' color' + item.colors + '"' + cardLink(item.scryfallUri) + cardImageRollover(item.imageUris) + '>' + item.name + " " +  manaCostHtml(item.manaCost) + "</span>";
}

function cardLine(item) {
    return '<div class="card color' + item.colors + '"' + cardLink(item.scryfallUri) + cardImageRollover(item.imageUris) + '><div class="manaCost">' + manaCostHtml(item.manaCost) + "</div><span>" + item.count + ' ' + item.name + "</span></div>";
}

function cardInline(item) {
    return '<span class="card color' + item.colors + '"' + cardLink(item.scryfallUri) + cardImageRollover(item.imageUris) + '>' + item.name + ' ' + manaCostHtml(item.manaCost) + "</span>";
}

function showTokens(deckFile, index) {
    var isVisible = $('#tokenLine'+index).is(':visible');
    $('#deckLine'+index).hide();

    if (isVisible) {
        $('#tokenLine'+index).hide();
    } else {
        $('#tokenLine'+index).show();
        $.ajax({
            url: apiHost + deckFile + "/tokens.json"
        }).done(function(data) {

            var deckList = '';

            if (data.tokens.length > 0) {
                deckList = deckList + '<h3>Token(s):</h3>';
                data.tokens.forEach(function (item, index) {
                    deckList = deckList + '<div class="token">' + item.token + '</div>';
                    deckList = deckList + '<div class="simpleCardList">';
                    item.cards.forEach(function (item, index) {
                        deckList = deckList + cardInline(item);
                    });
                    deckList = deckList + '</div>';
                });
            }

            if (data.counters.length > 0) {
                deckList = deckList + '<h3>Counter(s):</h3>';
                data.counters.forEach(function (item, index) {
                    deckList = deckList + '<div class="token">' + item.counter + '</div>';
                    deckList = deckList + '<div class="simpleCardList">';
                    item.cards.forEach(function (item, index) {
                        deckList = deckList + cardInline(item);
                    });
                    deckList = deckList + '</div>';
                });
            }

            if (data.other.length > 0) {
                deckList = deckList + '<h3>Other stuff:</h3>';
                data.other.forEach(function (item, index) {
                    deckList = deckList + '<div class="token">' + item.other + '</div>';
                    deckList = deckList + '<div class="simpleCardList">';
                    item.cards.forEach(function (item, index) {
                        deckList = deckList + cardInline(item);
                    });
                    deckList = deckList + '</div>';
                });
            }

            $('#tokenLine'+index+" .deck").html(deckList);
        }).fail(function() {
            $('#tokenLine'+index).hide();
        }).always(function() {
        });
    }
}

function showDeck(deckFile, index) {
    var isVisible = $('#deckLine'+index).is(':visible');
    $('#tokenLine'+index).hide();

    if (isVisible) {
        $('#deckLine'+index).hide();
    } else {
        $('#deckLine'+index).show();
        $.ajax({
            url: apiHost + deckFile + "/deckList.json"
        }).done(function(data) {

              var deckList = '';

              data.deckList.forEach(function (item, index) {
                    deckList = deckList + '<h3>' + item.shortType + ' (' + item.count + ')</h3><div class="deckCardList">';
                    item.cards.forEach(function (item, index) {
                        deckList = deckList + cardLine(item)
                    });
                    deckList = deckList + '</div>';
              });

             $('#deckLine'+index+" .deck").html(deckList);
        }).fail(function() {
            $('#deckLine'+index).hide();
        }).always(function() {
        });
    }
}

function showCardImage(imageUris) {
    var previews = ''
    imageUris.forEach(function (item, index) {
        previews = previews + '<div class="cardPreview" style="background-image:url('+item+')"></div>';
    });
    $("#cardPreviewBox").html(previews);
    $("#cardPreviewBox").css('opacity', '1');
}

function fadeCardImage() {
    $("#cardPreviewBox").css('opacity', '0.1');
}

function manaCostHtml(manaCostJson) {
    var manaCost = '';

    if (manaCostJson) {
        manaCostJson.forEach(function (cost, index) {
            if (cost == '=') {
                manaCost = manaCost + " //";
            } else {
                manaCost = manaCost + " <i class='ms ms-cost ms-" + cost.toLowerCase() + "'></i>";
            }
        });
    }

    return manaCost;
}

$(document).ready(function() {
    reload();

    $('#refresh').click(function() {
        reload();
    });

    $('#possibleDecks').click(function() {
        possibleDecks();
    });

});
