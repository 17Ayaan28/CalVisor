from flask_login import current_user
from .Google_Maps import Google_Maps
from .Yelp_Fusion import Yelp_Fusion
from .Models import Event
import datetime
from datetime import datetime as dt

YELP_API_KEY = "fO8TiLtHX-rUF2d0_0l19QelvQoQmHghyQP395yuiRjmPI-5Oj6173IDuZ_Yo2tIBbnr8bxzv29wsgc9IYmCvUMcvjm1lsxHa2oVP_BbA2l69nr9kRFOT5P6-_tdXnYx"
GOOGLE_MAPS_API_KEY = "AIzaSyDNSQlkoM44anY1fYWt-c84gFf_2S40lbg"
EATING_DUR_MINS = 30
DEFAULT_RADIUS = 700
DEFAULT_HANG_ACTIVITY_RADIUS = 2000

class Recommendation_System:

    def __init__(self):
        self.Google_Maps_Api = Google_Maps(GOOGLE_MAPS_API_KEY)
        self.Yelp_Fusion_Api = Yelp_Fusion(YELP_API_KEY)


    def get_recs(self, events, event_duration, category, num_recs=5, current_loc=None):

        # Convert current_loc actual address

        searched_place = self.Google_Maps_Api.search_place(current_loc)

        if(searched_place == -1):
            return {'recs': []}


        # Get time gap in schedule
        time_gap_details = self.find_time_gap(events, searched_place.addr)
        # Get nearby places from APIs

        nearby_places = []
        coord = self.Google_Maps_Api.get_geocode(time_gap_details['starting_loc'])

        if category == 'Eat':
            nearby_places += self.rec_food(coord, num_recs=num_recs)
        elif category == 'Study':
            nearby_places += self.rec_study(coord, num_recs=num_recs)
        elif category == 'Hangout':
            nearby_places += self.rec_hangout(coord, num_recs=num_recs)
        elif category == 'Exercise':
            nearby_places += self.rec_physical(coord, num_recs=num_recs)

        sorted_nearby_events = self.sort_places(nearby_places,
                                                event_duration,
                                                time_gap_details['starting_loc'],
                                                time_gap_details['ending_loc'])
        rec_dict = {'recs': []}
        curr_datetime = dt.now()
        for nearby_place in sorted_nearby_events:



            # Start Time = start of break + travel time to location
            start_time = (dt.combine(dt.today(), time_gap_details['start']) + datetime.timedelta(minutes=nearby_place['travel_to'])).time()
            # End Time = start time + break duration
            end_time = (dt.combine(dt.today(), start_time) + datetime.timedelta(minutes=event_duration)).time()
            # Convert start time from time obj to datetime object
            start_time = curr_datetime.replace(hour=start_time.hour,
                                               minute=start_time.minute,
                                               second=start_time.second)

            # Convert End time from time obj to datetime obj
            end_time = curr_datetime.replace(hour=end_time.hour,
                                         minute=end_time.minute,
                                         second=end_time.second)



            clashing = end_time.time() > time_gap_details['end']
            rec = {'place':nearby_place['place'],
                   'date': dt.now().date().strftime('%Y-%m-%d'),
                   'start':start_time.strftime('%H:%M:%S'),
                   'end': end_time.strftime('%H:%M:%S'),
                   'travel_to': nearby_place['travel_to'],
                   'travel_to_next':nearby_place['travel_from'],
                   'clashing': clashing}


            rec_dict['recs'].append(rec)


        return rec_dict


    def find_time_gap(self, events, starting_loc=None):

        # Define Initial Values
        break_start = datetime.datetime.now().time()
        break_end = datetime.time(23, 59)
        origin = starting_loc
        ending_loc = ""
        curr_time = dt.now().time()
        last_checked_event = Event(name = 'Now',
                                    addr = origin,
                                    date = datetime.datetime.now().date(),
                                    start_time = curr_time,
                                    end_time = curr_time,
                                    repeating_event = False,
                                    user_id = current_user.id)

        # Sort Events
        sorted_events = sorted(events, key=lambda x: x.start_time)
        curr_event = last_checked_event
        for event in sorted_events:
            curr_event = event
            # if event has passed (may or may not be finished) - conitinue
            if(event.start_time <= curr_time
                or event.start_time <= last_checked_event.end_time):
                last_checked_event = event
                continue

        # Set Starting Loc as previous event's loc
        origin = last_checked_event.addr
        # Set Start of Break
        if(last_checked_event.end_time >= curr_time):
            break_start = last_checked_event.end_time
        else:
            break_start = curr_time

        if(curr_event != last_checked_event):
            break_end = event.start_time
            ending_loc = event.addr


        return {'start':break_start,
                'end': break_end,
                'starting_loc': origin,
                'ending_loc':ending_loc}


    def rec_food(self, coord, radius=DEFAULT_RADIUS, num_recs=5):
        food_places = []
        res = 0
        res = self.Yelp_Fusion_Api.search_business('food', coord, radius, num_recs)
        if res != -1:
            food_places += res

        return food_places

    def rec_study(self, coord, radius=DEFAULT_RADIUS, num_recs=5):
        study_places = []
        res = 0
        res = self.Yelp_Fusion_Api.search_business('libraries', coord, radius, num_recs)
        if res != -1:
            study_places += res
        res = self.Yelp_Fusion_Api.search_business('cafes', coord, radius, num_recs)
        if res != -1:
            study_places += res

        return study_places

    def rec_hangout(self, coord, radius=DEFAULT_HANG_ACTIVITY_RADIUS, num_recs=5):
        hangout_places = []
        res = 0
        res = self.Yelp_Fusion_Api.search_business('parks', coord, radius, num_recs)
        if res != -1:
            hangout_places += res
        res = self.Yelp_Fusion_Api.search_business('bars', coord, radius, num_recs)
        if res != -1:
            hangout_places += res
        res = self.Yelp_Fusion_Api.search_business('movietheaters', coord, radius, num_recs)
        if res != -1:
            hangout_places += res
        res = self.Yelp_Fusion_Api.search_business('spas', coord, radius, num_recs)
        if res != -1:
            hangout_places += res

        return hangout_places

    def rec_physical(self, coord, radius=DEFAULT_HANG_ACTIVITY_RADIUS, num_recs=5):
        physical_places = []
        res = 0
        res = self.Yelp_Fusion_Api.search_business('active', coord, radius, num_recs)
        if res != -1:
            physical_places += res
        res = self.Yelp_Fusion_Api.search_business('gyms', coord, radius, num_recs)
        if res != -1:
            physical_places += res
        res = self.Yelp_Fusion_Api.search_business('parks', coord, radius, num_recs)
        if res != -1:
            physical_places += res

        return physical_places

    def sort_places(self, places, event_duration, starting_loc, ending_loc):

        timed_places = []
        for place in places:
            start_travel_time = self.Google_Maps_Api.get_travel_time(starting_loc, place['addr'], 'walking')
            if ending_loc == "":
                end_travel_time = 0
            else:
                end_travel_time = self.Google_Maps_Api.get_travel_time(place['addr'], ending_loc, 'walking')

            total_travel_time = start_travel_time + end_travel_time
            total_time = start_travel_time + end_travel_time + event_duration
            timed_place = {"place":place,
                           'travel_to':start_travel_time,
                           'travel_from':end_travel_time,
                           "total_time":total_time,
                           "total_travel":total_travel_time}
            timed_places.append(timed_place)

        sorted_timed_places = sorted(timed_places, key=lambda dict: dict['total_time'])
        return sorted_timed_places

    def schedule_place(self, current_loc, place_name, break_duration):



        all_events = Event.query.filter_by(date=dt.now().date()).filter_by(user_id=current_user.id).all()
        # Get nearest time gap in schedule
        time_gap_details = self.find_time_gap(all_events, current_loc)

        ret_val = {'recs': []}

        place_obj = self.Google_Maps_Api.search_place(place_name, origin=time_gap_details['starting_loc'])
        # Check if place found, return empty dict if not found
        if place_obj == -1:
            return retval


        # Calculate time after travelling to searched place from current location
        travel_to_mins = self.Google_Maps_Api.get_travel_time(time_gap_details['starting_loc'], place_obj.addr, 'walking')
        # Get time object from mins
        start_time = (dt.combine(dt.today(), time_gap_details['start']) + datetime.timedelta(minutes=travel_to_mins)).time()

        # Calculate time after traveling from searched place to next event
        travel_from_mins = 0
        if(time_gap_details['ending_loc'] != ""):
            travel_from_mins = self.Google_Maps_Api.get_travel_time(place_obj.addr, time_gap_details['ending_loc'], 'walking')
        # Get time object of start_time + duration
        end_time = (dt.combine(dt.today(), start_time) + datetime.timedelta(minutes=break_duration)).time()
        # Get time object of start_time + duration + travel from searched place to next event
        time_post_travel_from = (dt.combine(dt.today(), end_time) + datetime.timedelta(minutes=travel_from_mins)).time()



        place = {'name':place_obj.name,
                 'addr':place_obj.addr}
        rec = {'place': place,
               'date': dt.now().date().strftime('%Y-%m-%d'),
               'start': start_time.strftime('%H:%M:%S'),
               'end': end_time.strftime('%H:%M:%S'),
               'travel_to': travel_to_mins,
               'travel_to_next': travel_from_mins,
               'clashing': False}


        if(time_post_travel_from > time_gap_details['end']):
            rec['clashing'] = True


        ret_val['recs'].append(rec)

        return ret_val
