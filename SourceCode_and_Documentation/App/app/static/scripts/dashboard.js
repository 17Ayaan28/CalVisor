// Dashboard button events

// Add  Event Button
var new_event_button = document.getElementsByClassName('add_event_button')[0]

new_event_button.addEventListener('click', function () {
    location.href=Flask.url_for('main.new_event')
});

// Clear all button
var clear_all_button = document.getElementsByClassName('clear_all_button')[0];
clear_all_button.addEventListener('click', function () {
    location.href=Flask.url_for('main.clear_all');
})

// Recommendation Button
var rec_button = document.getElementsByClassName('get_recommendations_button')[0];
rec_button.addEventListener('click', function () {
    location.href=Flask.url_for('main.recommendations');
})

var submit_invite = document.getElementsByClassName('search-invitee_button')[0]; //Invitation System
submit_invite.addEventListener('click', async function () {
    let event_id = document.getElementById('event_id').value

    let username = document.getElementById('invitee_search_username').value;
    const data = { username, event_id }
    const response = await makeRequest(data, "/invite", 'POST')
    if (response.message !== " ") {
        document.getElementById('invite_error').innerText = response.message
    }
    else {

        document.getElementById('invite_error').innerText = "Your invite request has been sent!"
    }
    // location.href=Flask.url_for('main.invite');
})

var incoming_invites = document.getElementsByClassName('incoming_invites_button')[0]; //Invitation System
incoming_invites.addEventListener('click', async function () {
    const data = { }
    const response = await makeRequest(data, "/incoming_invites", 'GET')

    const incoming_invites_body = document.getElementById('incoming_invites_body');
    // incoming_invites_body.innerText = "";
    if (response.content){
        for (let index = 0; index < response.content.length; index++) {
            const content = response.content[index]
            incoming_invites_body.appendChild(makeInvite(content))
            if (index !== response.content.length - 1)
                incoming_invites_body.appendChild(document.createElement('br'))
        }
    } else {
        incoming_invites_body.appendChild(makeElement('','no_received_invite', response.message))
    }

})

var scheduling_event_button = document.getElementsByClassName('scheduling_invite_button')[0]; //Invitation System
scheduling_event_button.addEventListener('click', async function () {

    location.href=Flask.url_for('main.scheduling_invites')
})


function acceptInvite (invite_id) { //Invitation System

    const data = { invite_id}
    const response = makeRequest(data, '/accept_invite', 'POST')

    const accepted_invite = document.getElementById(`incoming_invite_${invite_id}`)
    document.getElementById('incoming_invites_body').removeChild(accepted_invite)

}

function declineInvite (invite_id) { //Invitation System
    const data = { invite_id }
    const response = makeRequest(data, '/decline_invite', 'POST')
    // do stuff
    const deleted_invite = document.getElementById(`incoming_invite_${invite_id}`)
    document.getElementById('incoming_invites_body').removeChild(deleted_invite)

}

makeInvite = (content) => { //Invitation System
    const div = document.createElement('div')
    const p = document.createElement('p');
    const accept = document.createElement('button');
    const decline = document.createElement('button');

    p.innerText = content.message

    accept.innerText = 'Accept'
    accept.setAttribute('type', 'button')
    accept.setAttribute('value', content.invite_id)
    accept.setAttribute('onClick', 'acceptInvite(value)')

    decline.innerText = 'Decline'
    decline.setAttribute('type', 'button')
    decline.setAttribute('value', content.invite_id)
    decline.setAttribute('onClick', 'declineInvite(value)')


    div.setAttribute('id', `incoming_invite_${content.invite_id}`)
    p.setAttribute('class', 'individual_invite')
    p.appendChild(document.createElement('br'))
    p.appendChild(accept)
    p.appendChild(decline)
    div.appendChild(p)

    return div
};

buildTimePicker = () => {
    let option;
    const hours = document.getElementById('hour');
    for (let h = 0; h <= 23; h++) {
        option = document.createElement('option');
        option.setAttribute('value', h);
        option.appendChild(document.createTextNode(h + 'h'));
        hours.appendChild(option);
    }
    const minutes = document.getElementById('minute');
    minutes.setAttribute('id', 'minute');
    for (let m = 0; m <= 59; m += 5) {
        option = document.createElement('option');
        option.setAttribute('value', m);
        option.appendChild(document.createTextNode(m + 'm'));
        minutes.appendChild(option);
    }
};
// When the user clicks on div, open the popup
function showModal(id) {
    const popup = document.getElementById(`popup-${id}`);
    // popup.classList.toggle('show');
    // Delay so it fires after window.onclick
    setTimeout(() => { popup.classList.toggle('show') }, 5);
}

function modalNavigate(url) {
    location.href = url;
}

window.onclick = () => {
    const popups = document.getElementsByClassName('popuptext');
    for(let i = 0; i < popups.length; ++i)
        if (popups[i].classList.contains('show'))
            popups[i].classList.remove('show');
};
