from .Models.Event import Event

class Calendar:

    def __init__(self, owner):
        self._owner = owner
        self._events = []

    def get_owner(self):
        return self._owner

    def add_event(self, new_event):
        self._events.append(new_event)

    def rem_event(self, event):
        if event in self._events:
            self._events.remove(event)

    def get_events_by_day(self, day):
        places = []
        for event in self._events:
            if event.get_day() == day:
                places.append(event)

        return places
