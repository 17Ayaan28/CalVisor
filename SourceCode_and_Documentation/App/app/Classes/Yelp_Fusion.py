from .API import API
from .Place import Place
from .Coordinate import Coordinate
from app.modules import time_parser
import requests, re, datetime

class Yelp_Fusion(API):

    def search_business(self, term, coordinate, radius, num_recs):
        """
        Get business nearby given coordinate within given radius
        """

        # Define Headers
        headers = {'Authorization' : 'Bearer ' + self._api_key}
        # Define Parameters
        payload = {'term':term,
        'latitude': coordinate.get_lat(),
        'longitude': coordinate.get_lng(),
        'radius': radius,
        'limit': num_recs}

        business_search_ep = "https://api.yelp.com/v3/businesses/search"
        # Get Response
        response = requests.get(business_search_ep, headers=headers, params=payload)
        
        places = []
        # Get resulting places
        for res in response.json()['businesses']:
                name = res['name']
                addr = " ".join(res['location']['display_address'])

                new_place = {'name': name,
                             'addr': addr}

                places.append(new_place)


        return places

    def isOpen(self, id, day_of_week, time):
        """
        Returns True if Business (id given by business_search) is open
        day_of_week = 0 - 6 (MON-SUN)
        """
        business_api_url = "https://api.yelp.com/v3/businesses/" + id
        headers = {'Authorization' : 'Bearer ' + self._api_key}

        response = requests.get(business_api_url, headers=headers)
        try:
            # Get Start time and End time strings
            start_time_str = response.json()['hours'][0]['open'][day_of_week]['start']
            end_time_str = response.json()['hours'][0]['open'][day_of_week]['end']
            # Create Time Object
            start_time = time_parser.parse_time_str(start_time_str)
            end_time = time_parser.parse_time_str(end_time_str)
            # If time is within open and closing time, return True
            if time >= start_time or time <= end_time:
                return True
        except:
            return False

        return False
