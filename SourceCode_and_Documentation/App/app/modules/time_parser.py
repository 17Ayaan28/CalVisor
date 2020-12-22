import re, datetime
from app import db

def parse_time_str(str):
    """
    Converts a 24-hour str (e.g. 2330) to a datetime.time obj
    """
    # Get Hr & Min str
    result = re.search(r'(\d\d)(\d\d)', str)
    hr = result.group(1)
    min = result.group(2)
    # Create datetime object

    time = datetime.time(hour=int(hr), minute=int(min))
    return time

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
