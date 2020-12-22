document.addEventListener('DOMContentLoaded', function() {
  var calendarEl = document.getElementById('calendar');

  var calendar = new FullCalendar.Calendar(calendarEl, {
    plugins: [ 'interaction', 'dayGrid', 'timeGrid' ],
    defaultView: 'timeGridWeek',
    header: {
        left: 'prev, next, today',
        center: 'title',
        right: 'dayGridMonth, timeGridWeek, timeGridDay'
    },
    eventRender: function(info) {
        info.el.addEventListener('contextmenu', function(e) {
            // Prevent Browser default right click
            e.preventDefault();
            // Calculate Position of Dropdown menu
            var top = e.pageY - 10;
            var left = e.pageX + 15;
            // Show Modal
            $("#context-menu-event").finish().toggle(100).css({
                display: 'block',
                top: top,
                left: left
            })
            $("#context-menu-event-edit").click(function(e) {
                location.href=Flask.url_for('main.edit_event', {"id":info.event['id']});
            })
            $("#context-menu-event-del").click(function(e) {
                location.href=Flask.url_for('main.delete_event', {"id":info.event['id']});
            })

            $("#context-menu-event-invite").click(function(e) { // Invitation System
                document.getElementById('event_id').value=info.event['id'];
                
                $('#invite_search_modal').modal('show');

            })

        });
    }
})
  calendar.render();

  for(let i=0; i<all_events.length; ++i) {
      let new_event = {
          id: all_events[i]['id'],
          title: all_events[i]['name'],
          start: all_events[i]['date'] + "T" + all_events[i]['startTime'],
          end: all_events[i]['date'] + "T" + all_events[i]['endTime'],
          location: all_events[i]['address'],
      }
      if(all_events[i]['repeating']){
          new_event['daysOfWeek'] = [((all_events[i]['weekday'] + 1) % 7)];
          new_event['startTime'] = all_events[i]['startTime'];
          new_event['endTime'] = all_events[i]['endTime'];
      }
      
      calendar.addEvent(new_event);
  }
});
document.addEventListener('click', function(e) {
    $('#context-menu-event').removeClass("show").hide();
});
