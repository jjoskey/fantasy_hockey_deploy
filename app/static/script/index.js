(function (global) {

const timeElements = $('.time');
//console.log(timeElements);
timeElements.each(function() {
    console.log($(this).attr('data-time'));
    const date = new Date($(this).attr('data-time'));
    console.log(date);

//    console.log(date)
    $(this).text(date.toLocaleString('ru', {day: '2-digit', month: '2-digit' ,hour: '2-digit', minute:'2-digit'}));
//    console.log($(this).attr('data-time'));
})


if ( $('.previous_tour').children().length === 0 ) {
    $('.previous_tour').addClass('hide');
    $('.games-row').addClass('justify-content-center');
}

if ( $('.current_tour').children().length === 0 ) {
    $('.current_tour').addClass('hide');
    $('.games-row').addClass('justify-content-center');
}

//let date = new Date(data.tour_info.deadline)
})(window)