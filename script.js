function reload() {
    $('#loading').show();
    $('#header').hide();
    $('#error').hide();
    $('#deckTable>tbody').empty();
    $('#refresh').prop('disabled', true);
    $('#currency').prop('disabled', true);
    $('#order').prop('disabled', true);
    $.ajax({
        url: "http://127.0.0.1:5000/" + $('#currency').val() + "/" + $('#order').val()  + "/deckPrice.json"
    }).done(function(data) {
        data.forEach(function (item, index) {
            var commanders = ''
            item.commanders.forEach(function (item, index) {
                commanders = commanders + '<span class="commander color' + item.colors + '">' + item.name + "</span>"
            });
            item.companions.forEach(function (item, index) {
                commanders = commanders + '<span class="commander companion color' + item.colors + '">' + item.name + "</span>"
            });
            $('#deckTable>tbody').append("<tr><td>"+(index+1)+"</td><td>"+ commanders +'</td><td>'+ item.age +'</td><td>'+ item.rank +'</td><td class="deckPrice">'+ item.deckPriceTotal +"</td><td>" + $('#currency').val() + "</td></tr>");
        });
        $('#header').show();
    }).fail(function() {
        $('#error').show();
    }).always(function() {
        $('#loading').hide();
        $('#refresh').prop('disabled', false);
        $('#currency').prop('disabled', false);
        $('#order').prop('disabled', false);
    });
}

$(document).ready(function() {
    reload();

    $('#refresh').click(function() {
        reload();
    });
});
