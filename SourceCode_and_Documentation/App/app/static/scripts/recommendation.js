// Select Buttons
var select_buttons = document.getElementsByClassName('select-rec');
for(var i = 0; i < select_buttons.length; ++i) {
    var select_btn = select_buttons[i];
    select_btn.addEventListener('click', function () {
        var parent = select_btn.parentNode;
        var rec_name = parent.getElementsByClassName('rec-name')[0].textContent;
        var rec_addr = parent.getElementsByClassName('rec-addr')[0].textContent;
        var rec_start = parent.getElementsByClassName('rec-start')[0].textContent;
        var rec_end = parent.getElementsByClassName('rec-end')[0].textContent;
        var rec_day_str = parent.getElementsByClassName('rec-day-str')[0].textContent;
        params = {'rec_name' : rec_name,
                  'rec_addr' : rec_addr,
                  'rec_day_str' : rec_day_str,
                  'rec_start': rec_start,
                  'rec_end'  : rec_end }
        location.href=Flask.url_for('main.add_rec', params);
    })
}


let fetch_body_json = {
    'have_place':  "",
    'destination': "",
    'category': "",
    "hrs": "",
    "mins": "",
    "curr_loc": ""
}


// Question 1
$('.question-1-input-button').hover(function(e) {
    var button_val = e.target.textContent
    $('.question-1-input-text').val(button_val)
}).click(function(e) {
    // Grab Input Text
    fetch_body_json['have_place'] = $('.question-1-input-text').val().trim()
    // Hide Buttons
    $('.question-1-buttons').slideUp(200, function(){
        if(fetch_body_json['have_place'] == 'Yes'){
            $('.question-5').slideDown(200)
        } else {
            $('.question-2').slideDown(200)
        }
    })
})
// Question 2
$('.question-2-input-button').hover(function(e) {
    var button_val = e.target.textContent
    $('.question-2-input-text').val(button_val)
}).click(function(e) {
    fetch_body_json['category'] = $('.question-2-input-text').val().trim()
    $('.question-2-buttons').slideUp(200, function() {
        $('.question-3').slideDown(200)
    })
})
// Question 3
$('.question-3-input-button.continue').click(function(e){
    fetch_body_json['hrs'] = $('.question-3-input-text.hours').val().trim()
    fetch_body_json['mins'] = $('.question-3-input-text.mins').val().trim()
    $('.question-3-buttons').slideUp(200, function() {
        if(! has_events_before){
            
            $('.question-4').slideDown(200)
        }

        $('.submit').slideDown(200)
    })
})
// Question 4
$('.submit-button.go').click(function(e) {
    fetch_body_json['curr_loc'] = $('.question-4-input-text.current-location').val().trim()


    $('.rec-items').slideUp(300, function(){
        $('.rec-list.header.found').slideUp(300, function(){
            $(".rec-list.header.searching").slideDown(300, function(){
                remove_recs()
                if(fetch_body_json['have_place'] == 'Yes'){
                    
                    res = schedulePlace(fetch_body_json).then(function(response){
                        return response.json();
                    }).then(function(parsedJSON){
                        $('.rec-list.header.searching').slideUp(300, function(){
                            $('.rec-list.header.found').slideDown(300)
                            $('.rec-items').slideDown(300, function(){
                                showRec(parsedJSON);
                                $('.add-rec').click(function(e){
                                    addRec(e.target.parentNode);
                                })
                            })
                        })
                    })
                } else {

                    res = getRecommendations(fetch_body_json).then(function(response){
                        return response.json();
                    }).then(function(parsedJSON){
                        
                        $('.rec-list.header.searching').slideUp(300, function(){
                            $('.rec-list.header.found').slideDown(300)
                            $('.rec-items').slideDown(300, function() {
                                showRec(parsedJSON);
                                $('.add-rec').click(function(e){
                                    addRec(e.target.parentNode);
                                })
                            })
                        })
                    })
                }
            })
        })
    })
})
// Question 5
$('.question-5-input-button.continue').click(function(e) {
    fetch_body_json['destination'] = $('.question-5-input-text.destination').val().trim()
    $('.question-5-buttons').slideUp(200, function(){
        $('.question-3').slideDown(200)
    })
})

async function getRecommendations(req_body){
    
    var url = location.origin.concat("/get_recommendations")
    let response = await fetch(url, {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify(req_body)
    })

    
    return response;
}

async function schedulePlace(req_body){
    
    var url = location.origin.concat("/schedule_place")
    let response = await fetch(url, {
        method: 'POST',
        headers: {'Content-Type':'application/json'},
        body: JSON.stringify(req_body)
    })
    
    return response;
}

function showRec(recs){
    let num_recs = recs['recs'].length;
    var rec_items = document.getElementsByClassName('rec-items')[0];
    for(let index=0; index < num_recs; ++index){
        // Create Elements for Rec Items
        var rec_item = document.createElement("div")
        rec_item.className='recommendation-item'
        // Set Clashing msg if event will clash
        if(recs['recs'][index]['clashing']){
            var clashing_msg = document.createElement('p')
            clashing_msg.className = 'recommendation-status clashing'
            clashing_msg.innerHTML = "Clashing"
            rec_item.appendChild(clashing_msg);
        }
        // Set Item Name
        var item_name = document.createElement('h3')
        item_name.className='item-name';
        item_name.innerHTML=recs['recs'][index]['place']['name']
        // Set Item Address
        var item_addr = document.createElement('p')
        item_addr.className='item-addr';
        item_addr.innerHTML= "Address: " + recs['recs'][index]['place']['addr']
        // Set Item Date
        var item_date = document.createElement('p')
        item_date.className ='item-date';
        item_date.innerHTML= "Date: ";
        var item_date_span = document.createElement('span')
        item_date_span.className = 'item-date-date'
        item_date_span.innerHTML = recs['recs'][index]['date']
        item_date.appendChild(item_date_span);
        // Set Item Start
        var item_start = document.createElement('p')
        item_start.className = 'item-start'
        item_start.innerHTML= "Start time: "
        var item_start_span = document.createElement('span')
        item_start_span.className = 'item-start-time'
        item_start_span.innerHTML = recs['recs'][index]['start']
        item_start.appendChild(item_start_span);
        // Set Item End
        var item_end = document.createElement('p')
        item_end.className = 'item-end';
        item_end.innerHTML= "End time: "
        var item_end_span = document.createElement('span')
        item_end_span.className = 'item-end-time'
        item_end_span.innerHTML = recs['recs'][index]['end']
        item_end.appendChild(item_end_span);
        // Set Travel Time to Destination
        var item_travel = document.createElement('p')
        item_travel.className = 'item-travel';
        item_travel.innerHTML= "Travel Time to Dest: " + recs['recs'][index]['travel_to'] + " min(s)"
        // Set Travel Time from Destination to Next Event
        // Set Total Travel Time
        var item_travel_from = document.createElement('p')
        item_travel_from.className = 'item-travel-from';
        item_travel_from.innerHTML= "Travel Time To Next Event: " + recs['recs'][index]['travel_to_next'] + " min(s)"
        // Set Select Button
        var select_btn = document.createElement('buttton')
        select_btn.className = 'add-rec btn btn-default'
        select_btn.type='button';
        select_btn.innerHTML = 'Select';
        select_btn.style.background = 'linear-gradient(to bottom right, #344CD1, #B3BEFF)';
        select_btn.style.color = 'white';

        // Add all elements to the div element
        
        rec_item.appendChild(item_name);
        rec_item.appendChild(item_addr);
        rec_item.appendChild(item_date);
        rec_item.appendChild(item_start);
        rec_item.appendChild(item_end);
        rec_item.appendChild(item_travel);
        rec_item.appendChild(item_travel_from);
        rec_item.appendChild(select_btn);

        // Add rec item to rec list
        rec_items.appendChild(rec_item)
    }
    $(".recommendation-item").slideDown(300)
}

function addRec(rec_item){
    let rec_name = $(rec_item).children('.item-name').text();
    let rec_addr = $(rec_item).children('.item-addr').text();
    let rec_start = $(rec_item).children('.item-date').children('.item-date-date').text() + 'T' + $(rec_item).children('.item-start').children('.item-start-time').text()
    let rec_end = $(rec_item).children('.item-date').children('.item-date-date').text() + 'T' + $(rec_item).children('.item-end').children('.item-end-time').text()

    params = {'rec_name' : rec_name,
              'rec_addr' : rec_addr,
              'rec_start': rec_start,
              'rec_end'  : rec_end }
    location.href=Flask.url_for('main.add_rec', params);
}


function remove_recs(){
    var rec_items = document.getElementsByClassName('rec-items')[0]
    
    while(rec_items.firstChild){
        
        rec_items.removeChild(rec_items.lastChild)
    }
}
