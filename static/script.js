
var apiHost = "./";

function reload() {
    $('#loading').show();
    $('#header').hide();
    $('#error').hide();
    $('#deckTable>tbody').empty();
    $('#refresh').prop('disabled', true);
    $('#currency').prop('disabled', true);
    $('#order').prop('disabled', true);
    $('#collection').prop('disabled', true);
    $('#possibleDecks').prop('disabled', true);
    $.ajax({
        url: apiHost + $('#currency').val() + "/" + $('#order').val()  + "/deckPrice.json"
    }).done(function(data) {
        data.forEach(function(item, index) {
            var commanders = '';
            item.commanders.forEach(function (item, index) {
                commanders = commanders + '<span class="commander color' + item.colors + '"' + cardImageRollover(item.imageUri) + '>' + item.name + " " +  manaCostHtml(item.manaCost) + "</span>";
            });
            item.companions.forEach(function (item, index) {
                commanders = commanders + '<span class="commander companion color' + item.colors + '"' + cardImageRollover(item.imageUri) + '>' + item.name + " " +  manaCostHtml(item.manaCost) + "</span>";
            });
            var indexTag = '<td class="rank">' + ( index + 1 ) + '</td>';
            var deckListTag = '<td><a onClick="showDeck(\'' + item.deckFile + '\', ' + ( index + 1 ) + ');" title="Decklist">&#128220;</a></td>';
            var tokensTag = '<td><a onClick="showTokens(\'' + item.deckFile + '\', ' + ( index + 1 ) + ');" title="Tokens and counters">&#127922;</a></td>';
            $('#deckTable>tbody').append('<tr>' + indexTag + deckListTag + tokensTag + '<td>'+ commanders +'</td><td>' + item.age + '</td><td>' + item.rank + '</td><td>' + item.complexity + '</td><td class="deckPrice">'+ item.deckPriceTotal +"</td><td>" + $('#currency').val() + "</td></tr>");
            $('#deckTable>tbody').append('<tr id="deckLine' + ( index + 1 ) + '"><td colspan="3"></td><td colspan="3" class="deck">Loading...</td><td colspan="3"></td></tr>');
            $('#deckTable>tbody').append('<tr id="tokenLine' + ( index + 1 ) + '"><td colspan="3"></td><td colspan="3" class="deck">Loading...</td><td colspan="3"></td></tr>');
            $('#deckLine'+ ( index + 1 )).hide();
            $('#tokenLine'+ ( index + 1 )).hide();
        });
        $('#header').show();
    }).fail(function() {
        $('#error').show();
    }).always(function() {
        $('#loading').hide();
        $('#refresh').prop('disabled', false);
        $('#currency').prop('disabled', false);
        $('#order').prop('disabled', false);
        $('#collection').prop('disabled', false);
        $('#possibleDecks').prop('disabled', false);
    });
}

function possibleDecks() {
    $('#loading').show();
    $('#header').hide();
    $('#error').hide();
    $('#deckTable>tbody').empty();
    $('#refresh').prop('disabled', true);
    $('#currency').prop('disabled', true);
    $('#order').prop('disabled', true);
    $('#collection').prop('disabled', true);
    $('#possibleDecks').prop('disabled', true);
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
            row = row + '<td>';
            item.commanders.forEach(function (item, index) {
                row = row + '<span class="commander color' + item.colors + '"' + cardImageRollover(item.imageUri) + '>' + item.name + " " +  manaCostHtml(item.manaCost) + "</span>";
            });
            item.companions.forEach(function (item, index) {
                row = row + '<span class="commander companion color' + item.colors + '"' + cardImageRollover(item.imageUri) + '>' + item.name + " " +  manaCostHtml(item.manaCost) + "</span>";
            });
            row = row + '</td>';
            row = row + '<td colspan="3">' + item.printPercentage + '</td>';
            row = row + '<td class="deckPrice">' + item.shoppingListPrice + '</td>';
            row = row + '<td>' + $('#currency').val() + '</td>'

            row = row + '</tr>';

            var deckList = '<h3 id="haveList' + ( index + 1 ) + '" class="folded">Have (' + item.haveListCount + '):</h3><div id="haveListContainer' + ( index + 1 ) + '">';

            item.haveList.forEach(function (item, index) {
                deckList = deckList + '<h3>' + item.shortType + ' (' + item.count + ')</h3><div class="deckCardList">';
                item.cards.forEach(function (item, index) {
                    deckList = deckList + '<div class="card color' + item.colors + '"' + cardImageRollover(item.imageUri) + '><div class="manaCost">' + manaCostHtml(item.manaCost) + "</div><div>" + item.count + ' ' + item.name + "</div></div>"
                });
                deckList = deckList + '</div>';
            });
            deckList = deckList + '</div>';

            deckList = deckList + '<h3 id="needList' + ( index + 1 ) + '" class="folded">Need (' + item.shoppingListCount + '):</h3><div id="needListContainer' + ( index + 1 ) + '">';

            item.shoppingList.forEach(function (item, index) {
                deckList = deckList + '<h3>' + item.shortType + ' (' + item.count + ')</h3><div class="deckCardList">';
                item.cards.forEach(function (item, index) {
                    deckList = deckList + '<div class="card color' + item.colors + '"' + cardImageRollover(item.imageUri) + '><div class="manaCost">' + manaCostHtml(item.manaCost) + "</div><div>" + item.count + ' ' + item.name + "</div></div>"
                });
                deckList = deckList + '</div>';
            });
            deckList = deckList + '</div>';

            $('#deckTable>tbody').append(row);
            $('#deckTable>tbody').append('<tr id="shoppingListLine' + ( index + 1 ) + '"><td colspan="3"></td><td colspan="3" class="deck">' + deckList + '</td><td colspan="3"></td></tr>');
            $('#deckTable>tbody').append('<tr id="deckLine' + ( index + 1 ) + '"><td colspan="3"></td><td colspan="3" class="deck">Loading...</td><td colspan="3"></td></tr>');
            $('#deckTable>tbody').append('<tr id="tokenLine' + ( index + 1 ) + '"><td colspan="3"></td><td colspan="3" class="deck">Loading...</td><td colspan="3"></td></tr>');
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
        $('#header').show();
    }).fail(function() {
        $('#error').show();
    }).always(function() {
        $('#loading').hide();
        $('#refresh').prop('disabled', false);
        $('#currency').prop('disabled', false);
        $('#order').prop('disabled', false);
        $('#collection').prop('disabled', false);
        $('#possibleDecks').prop('disabled', false);
    });
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
                        deckList = deckList + '<span class="card color' + item.colors + '"' + cardImageRollover(item.imageUri) + '>' + item.name + ' ' + manaCostHtml(item.manaCost) + "</span>"
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
                        deckList = deckList + '<span class="card color' + item.colors + '"' + cardImageRollover(item.imageUri) + '>' + item.name + ' ' + manaCostHtml(item.manaCost) + "</span>"
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
                        deckList = deckList + '<span class="card color' + item.colors + '"' + cardImageRollover(item.imageUri) + '>' + item.name + ' ' + manaCostHtml(item.manaCost) + "</span>"
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
                        deckList = deckList + '<div class="card color' + item.colors + '"' + cardImageRollover(item.imageUri) + '><div class="manaCost">' + manaCostHtml(item.manaCost) + "</div><div>" + item.count + ' ' + item.name + "</div></div>"
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

function showCardImage(imageUri) {
    $("#cardPreview").css('opacity', '1');
    $("#cardPreview").css('background-image', 'url(' + imageUri + ')');
}

function fadeCardImage() {
    $("#cardPreview").css('opacity', '0.1');
}

function cardImageRollover(imageUri) {
    if (imageUri) {
        return ' onmouseover="showCardImage(\'' + imageUri + '\');" onmouseout="fadeCardImage();"';
    } else {
        return '';
    }
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
