(function (global) {


    console.log('yo');
    $('.user_row').on('click', e => {
        const userId = e.target.parentElement.getAttribute('data-user-id');
        const link = window.location.origin + '/users/' + userId;
        console.log(link)
    })

})(window)
