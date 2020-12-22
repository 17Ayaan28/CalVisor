cancel_buttons = document.getElementsByClassName('cancel');
for(var i = 0; i < cancel_buttons.length; ++i){
    cancel_buttons[i].addEventListener('click', function () {
        location.href=Flask.url_for('main.dashboard');
    })
}
