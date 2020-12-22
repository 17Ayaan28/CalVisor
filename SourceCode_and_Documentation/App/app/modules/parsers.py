import re, datetime
from app.Classes.Models import Event

def parse_events(id):

    all_events = list()
    events = Event.query.filter_by(user_id=id)
    for event in events:
        event_dict = dict()
        event_dict['id'] = event.id;
        event_dict['name'] = event.name
        event_dict['address'] = event.addr
        event_dict['date'] = event.date.strftime("%Y-%m-%d")
        event_dict['startTime'] = event.start_time.strftime("%H:%M:%S")
        event_dict['endTime'] =  event.end_time.strftime("%H:%M:%S")
        event_dict['repeating'] = int(event.repeating_event)
        event_dict['weekday'] = event.date.weekday()
        all_events.append(event_dict)

    return all_events
