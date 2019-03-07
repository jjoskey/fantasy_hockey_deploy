(function (global) {


const players = [];

var myPlayers = new Object;
var fieldDisable, dataGlobal;

async function fetchAllPlayers() { // достает всех игроков из базы данных
    return fetch('/api_players/send_players_list/', {method: 'GET', headers: { 'Content-type': 'application/json' }, credentials: 'same-origin'})
        .then(response => response.json())
        .then(data => {
            dataGlobal = data;
            console.log(dataGlobal);
            return dataGlobal;
        })
}


function disablation(disable, message, tr) {
    if (disable) {
        let finalMessage = '';
        for (let i = 0; i < message.length; i++) {
            finalMessage += message[i];
            if (i !== message.length - 1) {
                finalMessage += ' ';
            }
        }
        tr.attr('title', finalMessage);
        tr.addClass('players-tr-disabled');
    } else {
        tr.removeClass('players-tr-disabled');
        tr.attr('title', '');
    }
}


function renderAllPlayers(data) {

    const tableBody = $('.tbody-all-players');

        if (!tableBody.children().length) {
            data.all_players.forEach(function(element) {
                const tr = $(`<tr class="player_row"><td>${element.fields.surname} ${element.fields.name}</td><td class="cell_centerize">${element.fields.position}</td><td class="cell_centerize">${element.fields.price}</td><td>${element.fields.club}</td></tr>`);
                tr.attr('data-player-id', element.id);
                disablation(element.disable, element.message, tr);
                tableBody.append(tr);
                players.push({domElement: tr, player: element});
            })
        } else {
            data.all_players.forEach(function (element) {
                const playerItem = players.find(item => item.player.id === element.id);
                if (playerItem) {
                    disablation(element.disable, element.message, playerItem.domElement);
                }
            })
        }

        $('.player_row').on('click', e => {
//            console.log('yes');
//            console.log(event.target.parentElement)
            if (!e.target.parentElement.classList.contains('players-tr-disabled')) {
                e.target.parentElement.classList.add('players-tr-disabled');
                const playerId = event.target.parentElement.getAttribute('data-player-id');
                console.log(playerId);
                fetch('/api_players/receive_player_id_to_add/', { method: 'POST', headers: { 'Content-type': 'application/json' }, body: JSON.stringify(playerId), credentials: 'same-origin' })
               .then(fetchAllPlayers)
               .then(data => {
                   useRecievedData(data);
               })
            }
        })
}


function showTourData(data) {
//    if (data.tour_info.deadline) console.log('yes!');

    const tour = $('#tour');
    const tourName = $('#tour_name');
    const deadline = $('#deadline');
    const deadlineEnd = $('#deadline_end');
    if (data.tour_info.tour_name) {
        tourName.text(`Текущий тур: ${data.tour_info.tour_name}`);
        tourName.parent().removeClass('hide');
    } else if (data.tour_info.tour) {
        tour.text(`Текущий тур: ${data.tour_info.tour}`);
        tour.parent().removeClass('hide');
    }



    if (data.tour_info.deadline) {
        let date = new Date(data.tour_info.deadline);
//        console.log(date);
        deadline.text(`Начало следующего дедлайна: ${date.toLocaleString('ru')}`);
        deadline.parent().removeClass('hide');
    }

    if (data.tour_info.deadline_end) {
        let date = new Date(data.tour_info.deadline_end);
        deadlineEnd.text(`Примерное время окончания дедлайна: ${date.toLocaleString('ru')}`);
        deadlineEnd.parent().removeClass('hide');
    }

}


function chooseCaptain(data) {
    const tableBody = $('.tbody-users-players');
            tableBody.empty();
            data.users_players.forEach(function(element) {
                let captain;
                if (element.id === data.captain) {
                    captain = '<i class="captain-icon fas fa-copyright" style="line-height: 0.4;"></i>';
                } else {
                    captain = '';
                }
                const tr = $(`<tr class="users_player_row"><td>${element.fields.surname} ${element.fields.name}</td><td class="cell_centerize">${element.fields.position}</td><td>${element.fields.club}</td><td class="cell_centerize">${captain}</td></tr>`);
                tr.attr('data-player-id', element.id);
                tableBody.append(tr);

            })

            $('.users_player_row').on('click', e => {
//            console.log('yes');
//            console.log(event.target.parentElement)

                const playerId = event.target.parentElement.getAttribute('data-player-id');
                console.log(playerId);
                fetch('/api_players/receive_captains_id/', { method: 'POST', headers: { 'Content-type': 'application/json' }, body: JSON.stringify(playerId), credentials: 'same-origin' })
               .then(fetchAllPlayers)
               .then(data => {
                   useRecievedData(data);
               })

        })
}

//$('.players-list').click( e => {
//   const playerId = playersListTarget(e);
//   if (!playerId) { return; }
//
//   fetch('/api_players/receive_player_id_to_add/', { method: 'POST', headers: { 'Content-type': 'application/json' }, body: JSON.stringify(playerId) })
//   .then(fetchAllPlayers)
//   .then(data => {
//       useRecievedData(data);
//   })
//});
//console.log($('tr'));



//    console.log(data);
//    const playersList = $('.players-list');
//
//    if (!playersList.children().length) {
//        data.all_players.forEach(function (element) {
//            const li = $('<li></li>');
//            li.addClass('players-list-li');
//            li.attr('data-player-id', element.id);
//            disablation(element.disable, element.message, li);
//            li.append(`${element.fields.surname} ${element.fields.name} ${element.fields.price} ${element.fields.position} ${element.fields.club}`);
//            playersList.append(li);
//            players.push({domElement: li, player: element});
//        })
//    } else {
//        data.all_players.forEach(player => {
//            const playerItem = players.find(item => item.player.id === player.id);
//            if (playerItem) {
//                disablation(player.disable, player.message, playerItem.domElement);
////
//            }
//        })
//    }


function renderBudget(data) {
    const myBudget = $('#budget');
    myBudget.html('Бюджет: ' + data.budget);
}


function renderChanges(data) {
    $('#changes').html('Количество трансферов: ' + data.changes);
}


function renderMyPlayers(data) {

//    const myPlayersList = $('.my-players');
//    myPlayersList.empty();
//    data.users_players.forEach( element => {
//        const li = $('<li></li>');
//        li.addClass('players-list-li');
//        li.attr('data-player-id', element.id);
//        disablation(element.disable, element.message, li);
//        li.append(`${element.fields.surname} ${element.fields.name} ${element.fields.price} ${element.fields.position} ${element.fields.club}`);
//
//        myPlayersList.append(li);
//    })

    const goalkeeperDiv = $('.goalkeeper');
    const defenderDiv = $('.defender');
    const midfielderDiv = $('.midfielder');
    const forwardDiv = $('.forward');

    goalkeeperDiv.empty();
    defenderDiv.empty();
    midfielderDiv.empty();
    forwardDiv.empty();

    data.users_players.forEach( element => {
        fieldDisable = element.disable;
        myPlayers[element.id] = element.fields.surname;
        const playerDiv = $('<div class="player"></div>');

        let tShirt = chooseShirt(element.fields.club);
        playerDiv.append(`<img class="player_image" src=${tShirt} alt="player" data-player-id=${element.id}>`);
        if (element.id === data.captain) {
            playerDiv.append(`<img class="player_image" src="/static/images/play/bandage_test.png" alt="player" data-player-id=${element.id}>`)
        }
        playerDiv.append(`<p class="font-weight-light player_sign" data-player-id=${element.id}><i class="fas fa-times" data-player-id=${element.id}></i>${element.fields.surname}</p>`);

        playerDiv.on('click', (e) => {
            if (!playerDiv.hasClass('disabled')) {
//                console.log(element.id);


                if (e.target.tagName === 'IMG' || e.target.tagName === 'P' || e.target.tagName === 'I') {
//                    console.log('YES!')
                    fetch('/api_players/receive_player_id_to_unactivate/', { method: 'POST', headers: { 'Content-type': 'application/json' }, body: JSON.stringify(element.id), credentials: 'same-origin' })
                    .then(fetchAllPlayers)
                    .then( data => {
                        useRecievedData(data);
                    })
                }
            }
        });

        if (element.disable) {
            playerDiv.addClass('disabled');
        }

        if (element.fields.position === 'GK') {
            goalkeeperDiv.append(playerDiv);
        } else if (element.fields.position === 'DE') {
            defenderDiv.append(playerDiv);
        } else if (element.fields.position === 'MF') {
            midfielderDiv.append(playerDiv);
        } else if (element.fields.position === 'FW') {
            forwardDiv.append(playerDiv);
        }


    })
    resizePlayerSign()
}

function chooseShirt(club) {

    let tShirt;

    if (club === 'Динамо-Строитель') {
        tShirt = '/static/images/play/1_shirt_DS.png';
    } else if (club === 'Динамо-Электросталь') {
        tShirt = '/static/images/play/2_shirt_DE.png';
    } else if (club === 'Динамо-Казань') {
        tShirt = '/static/images/play/3_shirt_DK.png';
    } else if (club === 'Динамо-ЦОП') {
        tShirt = '/static/images/play/4_shirt_DCOP.png';
    } else if (club === 'Тана') {
        tShirt = '/static/images/play/6_shirt_TANA.png'
    } else if (club === 'СПБ УОР2') {
        tShirt = '/static/images/play/5_shirt_SPB.png'
    } else if (club === 'Волна') {
        tShirt = '/static/images/play/7_shirt_VOLNA.png'
    }

    return tShirt;
}


//function playersListTarget(e) { // достает таргет при клике на элемент
//
//    if (e.target.tagName === 'LI' && !e.target.classList.contains('players-list-li-disabled'))
//        return +e.target.getAttribute('data-player-id');
//}


function saveButtonDisabled(data) {
    if (data.save === 'enable') {
        $('#save_team').attr("disabled", false);
    } else {
        $('#save_team').attr("disabled", true)
    }
}


function cancelButtonHide(data) {
    if (data.cancel === 'enable') {
        $('#cancel_transfers').removeClass('hide');
    } else {
        $('#cancel_transfers').addClass('hide');
    }
}


function hidingElementsForCaptainChoosing(data) {

    inputGroup = $('.input-group-div');
    tableAllPlayers = $('.table_players_all');
    tableMyPlayers = $('.users-players-div');
    buttonCaptain = $('.button-captain-div');
    buttonToPlayers = $('.button-to-players-div');

//        if freeze_and_count.is_first_time(user):
//            return 'wait_for_team'
//        else:
//            if is_captain:
//                return 'can_choose_another'
//            else:
//                return 'choose_captain'
    if (data.captain_stage === 'wait_for_team') {
        inputGroup.removeClass('hide');
        tableAllPlayers.removeClass('hide');
        tableMyPlayers.addClass('hide');
        buttonCaptain.addClass('hide');
        buttonToPlayers.addClass('hide');
    } else if (data.captain_stage === 'can_choose_another') {
        inputGroup.removeClass('hide');
        tableAllPlayers.removeClass('hide');
        tableMyPlayers.addClass('hide');
        buttonCaptain.removeClass('hide');
        buttonToPlayers.addClass('hide');
    } else if (data.captain_stage === 'choose_captain') {
        inputGroup.addClass('hide');
        tableAllPlayers.addClass('hide');
        tableMyPlayers.removeClass('hide');
        buttonCaptain.addClass('hide');
        buttonToPlayers.addClass('hide');
    } else if (data.captain_stage === 'freeze') {
        inputGroup.removeClass('hide');
        tableAllPlayers.removeClass('hide');
        tableMyPlayers.addClass('hide');
        buttonCaptain.addClass('hide');
        buttonToPlayers.addClass('hide');
    }
}






//$('.players-list').click( e => {
//   const playerId = playersListTarget(e);
//   if (!playerId) { return; }
//
//   fetch('/api_players/receive_player_id_to_add/', { method: 'POST', headers: { 'Content-type': 'application/json' }, body: JSON.stringify(playerId) })
//   .then(fetchAllPlayers)
//   .then(data => {
//       useRecievedData(data);
//   })
//});
//
//
//
//
//
//
//
//
//$('.my-players').click( e => {
//    const playerId = playersListTarget(e);
//    if (!playerId) return;
//
//    fetch('/api_players/receive_player_id_to_unactivate/', { method: 'POST', headers: { 'Content-type': 'application/json' }, body: JSON.stringify(playerId) })
//    .then(fetchAllPlayers)
//    .then( data => {
//        useRecievedData(data);
//    })
//})


$('#save_team').click( () => {
    $('#save_team').attr('disabled', true)
    fetch('/api_players/save_team/', { method: 'POST', credentials: 'same-origin' })
    .then(fetchAllPlayers)
    .then( data => {
        useRecievedData(data);
    })
})


$('#cancel_transfers').click( () => {
    $(this).attr('disabled', true);
    fetch('/api_players/cancel_transfers/', { method: 'POST' , credentials: 'same-origin'})
    .then(fetchAllPlayers)
    .then( data => {
        useRecievedData(data);
    })
    $(this).removeAttr('disabled');
})


$('#button-captain').click( () => {
    $('.button-captain-div').addClass('hide');
    $('.button-to-players-div').removeClass('hide');
    $('.input-group-div').addClass('hide');
    $('.table_players_all').addClass('hide');
    $('.users-players-div').removeClass('hide');


})


$('#button-to-players').click( () => {
    $('.button-captain-div').removeClass('hide');
    $('.button-to-players-div').addClass('hide');
    $('.input-group-div').removeClass('hide');
    $('.table_players_all').removeClass('hide');
    $('.users-players-div').addClass('hide');
})


fetchAllPlayers()
.then(data => {
    useRecievedData(data);
    filterTable($('#selectClub').find(':selected').text(), $('#selectPosition').find(':selected').val());
})

//$(document).ready( function () {
//    $('.table_all_players').DataTable();
//} );

$('.players-tr-disabled').tooltip();

function useRecievedData(data) {
    renderAllPlayers(data);
    renderMyPlayers(data);
    renderBudget(data);
    saveButtonDisabled(data);
    cancelButtonHide(data);
    renderChanges(data);
    chooseCaptain(data);
    hidingElementsForCaptainChoosing(data);
    showTourData(data);
}

window.onresize = resizePlayerSign


function resizePlayerSign() {


    let fieldHeight = parseFloat($('.field_div').css( 'height' ));

    let size, topSign, buttonFontSize, buttonBottom;
    if (fieldHeight >= 450) {
        size = 16 * fieldHeight / 690;
        topSign = 75;
        buttonBottom = 2.5;
        buttonFontSize = 0.875;
    } else if (fieldHeight >= 350 && fieldHeight < 450) {
        size = 9;
        topSign = 69;
        buttonBottom = 2.5;
        buttonFontSize = 0.75;
    } else {
        size = 8.5;
        topSign = 67;
//        buttonHeight = 0.85;
        buttonFontSize = 0.55;
        buttonBottom = 1.5;
    }

    $('.player_sign').css({fontSize: size, top: topSign + '%'})
    $('#save_team').css({fontSize: buttonFontSize + 'rem'});
    $('#cancel_transfers').css({fontSize: buttonFontSize + 'rem'});
    $('.buttons').css({bottom: buttonBottom + '%'});
    addDotsToSignes(fieldHeight);
}


function addDotsToSignes(fieldHeight) {

    let maxSignes, currentSurname;
    if (fieldDisable) {
         if (fieldHeight < 320) {
            maxSignes = 10;
        } else if (fieldHeight >= 320 && fieldHeight < 400) {
            maxSignes = 12;
        } else if (fieldHeight >= 400 && fieldHeight < 450) {
            maxSignes = 14;
        } else {
            maxSignes = 15;
        }

    } else {


        if (fieldHeight < 320) {
            maxSignes = 8;
        } else if (fieldHeight >= 320 && fieldHeight < 400) {
            maxSignes = 10;
        } else if (fieldHeight >= 400 && fieldHeight < 450) {
            maxSignes = 13;
        } else {
            maxSignes = 14;
        }
    }
    $('.player_sign').each(function(index) {
    let id = $(this).attr("data-player-id");
    currentSurname = myPlayers[$(this).attr("data-player-id")];
    if (currentSurname.length <= maxSignes) {
        $(this).text(currentSurname);
        $(this).prepend(`<i class="fas fa-times" data-player-id=${id}></i>`)
    }
    else {
        $(this).text(currentSurname.slice(0, maxSignes-1) + '..');
        $(this).prepend(`<i class="fas fa-times" data-player-id=${id}></i>`)
    }

    });
}


//console.log(dataGlobal);
function filterTable(valClub, valPosition) {
    let table, tr, td;
    table = $('.table_players_all');
    tr = $('.player_row');
//    console.log(tr);

    tr.each(function(index) {


        td = $(this).find('td');
//        let text = td[3].text();
        if (valPosition === 'Все позиции') {
            if (td[3].innerText === valClub) {
                $(this).attr("style", "display: '';");
            } else {
                $(this).attr("style", "display: none;");
            }
        } else {
        if (td[3].innerText === valClub && td[1].innerText === valPosition) {
                $(this).attr("style", "display: '';");
            } else {
                $(this).attr("style", "display: none;");
            }
        }
//        console.log(td);

    })

//    console.log(dataGlobal);

}

//$('#selectClub').find(':selected').text()
//$('#selectPosition').find(':selected').val()

$('#selectClub').change( function() {
//  console.log(this.value)
    filterTable(this.value, $('#selectPosition').find(':selected').val())
//  filterTable(val);
});

$('#selectPosition').change( function() {
//  console.log(this.value)
    filterTable($('#selectClub').find(':selected').text(), this.value);
//  filterTable(val);
});

 })(window)

