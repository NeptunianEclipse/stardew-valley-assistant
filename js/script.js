let villagers = villager_data.villagers;
let villagerCells = {};

function init() {
    let giftsTable = $('#gifts-table');

    for(let villager of villagers) {
        let imageCell = $('<div class="cell villager-img-cell"><img class="villager-img" src="' + villager.image + '"></div>');
        let nameCell = $('<div class="cell villager-name-cell">' + villager.name + '</div>');

        villagerCells[villager.name] = [];

        giftsTable.append(imageCell);
        villagerCells[villager.name].push(imageCell);

        giftsTable.append(nameCell);
        villagerCells[villager.name].push(nameCell);

        ['love', 'like'].forEach((category) => appendGiftInfo(giftsTable, villager.gifts[category], villager.name));

    }

    let tooltip = $('<span class="tooltip"></span>');

    $('.fancy-tooltip').mouseenter(function(event) {
        tooltip.text($(this).attr('title'));
        $(this).append(tooltip);
    });

    $('.fancy-tooltip').mouseleave(function(event) {
        tooltip.detach();
    });

    $(".nav-tab").click(function(event) {
        $('.tab-area').hide();
        $('.tab-area.' + $(this).attr('data-tab')).show();

        $('.nav-tab').removeClass('selected');
        $(this).addClass('selected');
    });

    $(".universal-toggle").click(function(event) {
        $("#universal-panel").toggle();
    });

    $(".search-bar").on('input', function(event) {
        filterShownVillagers($(this).val());
    });

    $(".search-bar").focus();
}

function appendGiftInfo(parent, gifts, villagerName) {
    let broadCell = $('<div class="cell"></div>');
    for(let gift of gifts.broad) {
        broadCell.append('<div class="broad-gift">' + gift + '</div>');
    }
    parent.append(broadCell);
    villagerCells[villagerName].push(broadCell);

    let cell = $('<div class="cell"></div>');
    for(let gift of gifts.specific) {
        cell.append('<a class="gift-img fancy-tooltip" href="' + gift.url + '" title="' + gift.name + '"><img src="' + gift.image + '"></a>');
    }
    parent.append(cell);
    villagerCells[villagerName].push(cell);
}

function filterShownVillagers(query) {
    let anyShown = false;

    for(villager of villagers) {
        if(villager.name.toLowerCase().includes(query.toLowerCase())) {
            for(cell of villagerCells[villager.name]) {
                cell.show();
            }
            anyShown = true;
        } else {
            for(cell of villagerCells[villager.name]) {
                cell.hide();
            }
        }
    }

    if(anyShown == false) {
        $('.no-results').show();
    } else {
        $('.no-results').hide();
    }
}



$(document).ready(init);