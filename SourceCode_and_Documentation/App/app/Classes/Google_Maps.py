from .API import API
from .Place import Place
from .Coordinate import Coordinate
import requests
import re

class Google_Maps(API):

    def get_travel_time(self, origin, dest, mode):
        """
        Returns the number minutes between `origin` and `dest` when travelling by `mode`
        """

        # define Endpoint
        distance_api_url = "https://maps.googleapis.com/maps/api/distancematrix/json"
        # Define Request Parameters
        payload = {'unit':'metric',
                   'origins': origin,
                   'destinations': dest,
                   'mode': mode,
                   'key': self._api_key}

        # GET Request
        json_response = requests.get(distance_api_url, params=payload).json()
        
        duration = 0
        # Try to Parse String, otherwise return Error
        try:
            dur_str = json_response['rows'][0]['elements'][0]['duration']['text']
            

            # Get mins
            m = re.search(r'(\d*) mins?', dur_str)
            if(m != None):
                duration += int((m.group(1)))

            # Get hours
            h = re.search(r'(\d*) hours?', dur_str)
            if(h != None):
                duration += int((h.group(1)))

            # Get Days
            d = re.search(r'(\d*) days?', dur_str)
            if(d != None):
                duration += int((d.group(1)))

        except:
            return -1

        return duration

    def get_geocode(self, address):
        """
        Returns the Coordinate (lat, lng) of `address`
        """

        # Define endpoint
        geocode_api_url = "https://maps.googleapis.com/maps/api/geocode/json"

        # Define Request Parameters
        payload = {'address':address, 'key':self._api_key }

        # Get JSON Response
        json_response = requests.get(geocode_api_url, params=payload).json()
        
        # Try to Parse the String, otherwise return Error
        try:
            lat_str = json_response['results'][0]['geometry']['location']['lat']
            lng_str = json_response['results'][0]['geometry']['location']['lng']


        except:
            return -1

        # Create new coordinate Object
        new_coord = Coordinate(float(lat_str), float(lng_str))
        return new_coord

    def search_place(self, search_term, origin=None):
        
        """
        Searches for nearby place given the search term
        Returns Place instance that is the closest match to search_term (if successful)
        Returns -1 if error
        """


        # Define endpoint
        search_place_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json"




        # Define Request Parameters
        params = {'key': self._api_key,
                  'input': search_term,
                  'inputtype': 'textquery',
                  'fields': 'formatted_address,name'}

        if(origin!=None and origin!=""):
           coord = self.get_geocode(origin)
           
           lat = str(coord.get_lat())
           lng = str(coord.get_lng())
           params['locationbias'] = 'point:'+lat+','+lng

        # GET Request to API
        res = requests.get(search_place_url, params=params)
        

        try:
            address = res.json()['candidates'][0]['formatted_address']
            name = res.json()['candidates'][0]['name']

            place = Place(name, address)
            retval = place
        except:
            empty_place = Place("","")
            return empty_place

        return retval
