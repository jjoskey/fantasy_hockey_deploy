(function (global) {

    $('.user_row').on('click', e => {
        const userId = e.target.parentElement.getAttribute('data-user-id');
        const link = window.location.origin + '/users_team/' + userId;
        window.location.href = link;
    })

    $('.user_row').each( function(index, element) {
        console.log(element, index)
        if (index === 0) {
            $(element).css('background-color', 'gold')
        } else if (index === 1) {
            $(element).css('background-color', 'silver')
        } else if (index === 2) {
            $(element).css('background-color', '#cd7f32')
        }
    })

})(window)
