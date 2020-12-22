var new_event_button = document.getElementsByClassName('change_password_button')[0]
new_event_button.addEventListener('click', function () {
    location.href=Flask.url_for('auth.changePassword')
});
