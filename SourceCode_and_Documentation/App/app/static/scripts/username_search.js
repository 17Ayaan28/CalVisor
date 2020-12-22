// Search Button
$(".search").click(function(e){
    $('.search-username').slideDown()
    $('.menu-bar').slideUp()
    $('.search-bar').focus()
    var search_bar = document.getElementsByClassName('search-bar')[0];
    search_bar.setSelectionRange(0,0);
})

$(".search-cancel").click(function(e){
    $('.search-username').slideUp()
    $('.menu-bar').slideDown()
})

$('.search-submit').click(function(e) {
    var search_query = document.getElementById("searchQuery").value
    e.preventDefault()
    search_query = search_query.trim()
    if(search_query.length == 0){
        e.preventDefault()
    } else {
        
        location.href=Flask.url_for('main.search_username', {"username": search_query})
    }
})
