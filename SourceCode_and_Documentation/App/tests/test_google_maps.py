import unittest
from app.Classes.Google_Maps import Google_Maps

API_KEY = "AIzaSyDNSQlkoM44anY1fYWt-c84gFf_2S40lbg"

class TestGetDistance(unittest.TestCase):

    def test_travel_time(self):
        google_maps_api = Google_Maps(API_KEY)

        origin = "Colombo House, University of New South Wales, Sydney, Australia"
        dest = "Keith Burrows Theatre, Univeristy of New South Wales, Sydney, Australia"
        res = google_maps_api.get_travel_time(origin, dest, 'walking')
        self.assertTrue(res == 4)

class TestGeocode(unittest.TestCase):

    def test_geocode(self):
        google_maps_api = Google_Maps(API_KEY)

        loc = "University of New South Wales, Sydney, Australia"
        coordinate = google_maps_api.get_geocode(loc)
        self.assertTrue(coordinate.get_lat() == -33.917347)
        self.assertTrue(coordinate.get_lng() == 151.2312675)
