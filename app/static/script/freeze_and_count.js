(function (global) {

async function fetchFreeze() {
    return fetch('/api_freeze_and_count/send_last_freeze/', { method: 'GET', headers: { 'Content-Type': 'application/json' }, credentials: 'same-origin' })
        .then(response => response.json())
}


function showButton(data) {

    if (data.message === "It's freeze time") {
        freezeTimeButton.removeClass('hide');
        freezeComingButton.addClass('hide');
        freezeParagraph.text(`Заморозка в туре ${data.tour} уже идет, время её начала: ${showDate(data)}. Чтобы её закончить прямо сейчас, нажмите на кнопку.`);
    } else if (data.message === 'Freeze time is coming soon') {
        freezeTimeButton.addClass('hide');
        freezeComingButton.removeClass('hide');
        freezeParagraph.text(`Время начала следующей заморозки перед ${data.tour} туром: ${showDate(data)}. Её можно начать прямо сейчас, нажав на кнопку.`);
    } else if (data.message === 'Danger!') {
        freezeTimeButton.addClass('hide');
        freezeComingButton.addClass('hide');
        freezeParagraph.text(`Срочно! Время следующего дедлайна не назначено! Скорее идите в админку и разберитесь с моделью Tour. Иначе PIZDETS!`);
        freezeParagraph.css('color', 'red');
    }
}


function showDate(data) {

    const options = {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: 'numeric',
    minute: 'numeric',
    };

    date = new Date(data.time).toLocaleString("ru", options);
    return date;
}

const freezeTimeButton = $('#freeze_time');
const freezeComingButton = $('#freeze_is_coming');
const freezeParagraph = $('#freeze_message');
const countButton = $('#count_button');
const addTransfers = $('#add_transfers');

fetchFreeze().then( data => showButton(data));

freezeTimeButton.click(() => {
//    let now = new Date();
    let message = 'Finish freeze time';
    let dataToSend = {'message': message};
    fetch('/api_freeze_and_count/receive_freeze_data/', { method: 'POST', headers: { 'Content-type': 'application/json' }, body: JSON.stringify(dataToSend), credentials: 'same-origin' })
    .then(fetchFreeze).then( data => showButton(data));
})

freezeComingButton.click(() => {
    freezeComingButton.attr('disabled', true);
//    let now = new Date();
    let message = 'Start freeze time';
    let dataToSend = {'message': message};
    fetch('/api_freeze_and_count/receive_freeze_data/', { method: 'POST', headers: { 'Content-type': 'application/json' }, body: JSON.stringify(dataToSend), credentials: 'same-origin' })
    .then(fetchFreeze).then( data => {
        freezeComingButton.removeAttr('disabled');
        showButton(data);
    })
})


countButton.click(() => {

    $('#not_number').addClass('hide');
    const tour = $('#tour_input').val();
    $('#tour_input').val(null);
    if (Number(tour)) {
        countButton.attr('disabled', true);
        let now = new Date();
        fetch('/api_freeze_and_count/count_and_save_points/', { method: 'POST', headers: {
            'Content-type': 'application/json' },
            body: JSON.stringify(Number(tour)),
            credentials: 'same-origin'
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);
            countButton.removeAttr('disabled');
        })
    } else {
        $('#not_number').removeClass('hide');
    }

//    console.log(tour);
})

addTransfers.click(() => {
    $('#not_number_transfers').addClass('hide');
    const transfers = $('#transfers_count').val();
    $('#transfers_count').val(null);
    if (Number(transfers)) {
        addTransfers.attr('disabled', true);
        fetch('/api_freeze_and_count/add_changes_to_all_profile/', { method: 'POST', headers: {
            'Content-type': 'application/json' },
            body: JSON.stringify(Number(transfers)),
            credentials: 'same-origin'
        })
        .then(data =>{
            addTransfers.removeAttr('disabled');
            console.log('yes');
        })
    } else {
        $('#not_number_transfers').removeClass('hide');
    }
//    console.log(tour);
})


})(window)

