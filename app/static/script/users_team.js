(function (global) {

function addDotsToSignes(fieldHeight) {

    let maxSignes, currentSurname;

    if (fieldHeight < 320) {
        maxSignes = 10;
    } else if (fieldHeight >= 320 && fieldHeight < 400) {
        maxSignes = 12;
    } else if (fieldHeight >= 400 && fieldHeight < 450) {
        maxSignes = 14;
    } else {
        maxSignes = 15;
    }


    $('.player_sign').each(function(index) {
//    let id = $(this).attr("data-player-id");
    currentSurname = $(this).text();
    if (currentSurname.length > maxSignes) {
        $(this).text(currentSurname.slice(0, maxSignes-1) + '..');

    }

    });
}

resizePlayerSign();
window.onresize = resizePlayerSign;


function resizePlayerSign() {


    let fieldHeight = parseFloat($('.field_div').css( 'height' ));

    let size, topSign;
    if (fieldHeight >= 450) {
        size = 16 * fieldHeight / 690;
        topSign = 75;

    } else if (fieldHeight >= 350 && fieldHeight < 450) {
        size = 9;
        topSign = 69;

    } else {
        size = 8.5;
        topSign = 67;
//        buttonHeight = 0.85;

    }

    $('.player_sign').css({fontSize: size, top: topSign + '%'})

    addDotsToSignes(fieldHeight);
}

})(window)