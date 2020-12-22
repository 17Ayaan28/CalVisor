from flask_login import current_user
from .Google_Maps import Google_Maps
from .Yelp_Fusion import Yelp_Fusion
from .Recommendation_System import Recommendation_System as recommendation
from app.Classes.Models import Event, User, Invites, Accepted_Inviters, Scheduling_Invites

from .Models import Event
import datetime
from datetime import datetime as dt

from ..modules import time_parser

YELP_API_KEY = "fO8TiLtHX-rUF2d0_0l19QelvQoQmHghyQP395yuiRjmPI-5Oj6173IDuZ_Yo2tIBbnr8bxzv29wsgc9IYmCvUMcvjm1lsxHa2oVP_BbA2l69nr9kRFOT5P6-_tdXnYx"
GOOGLE_MAPS_API_KEY = "AIzaSyDNSQlkoM44anY1fYWt-c84gFf_2S40lbg"


class Invitation_System:

    def __init__(self):
        self.Google_Maps_Api = Google_Maps(GOOGLE_MAPS_API_KEY)
        self.Yelp_Fusion_Api = Yelp_Fusion(YELP_API_KEY)
    def find_time_gap (self, event_start_time, event_end_time, events):
        sorted_events= sorted(events, key=lambda x: x.start_time)
        success = True
        failure = False
        for index in range(len(sorted_events)):
            if sorted_events[index].start_time < event_start_time and sorted_events[index].end_time < event_start_time: #The event ends before the invited event starts
                if index != len(sorted_events) - 1 and sorted_events[index+1].start_time > event_end_time: # The next event is after this event ends
                    return success, sorted_events[index].id, sorted_events[index+1].id
                elif index == len(sorted_events) -1: # The last event ends before the invited events
                    return success, sorted_events[index].id, None
                else:
                    return failure, -1, -1
            elif index == 0: # Looking at the first event
                if sorted_events[index].end_time < event_start_time: # The first event ended before the invited event
                    return success, None, sorted_events[index].id
                elif sorted_events[index].start_time > event_end_time:
                    return success, None, sorted_events[index].id
                else:
                    return failure, -1, -1
            elif sorted_events[index].start_time > event_start_time: # The event started in the middle of the invited event
                return failure, -1, -1
            elif event_start_time < sorted_events[index].end_time < event_end_time: # The event ends in the middle of the event
                return failure, -1, -1
            else:
                return failure, -1, -1
        return success, None, None
