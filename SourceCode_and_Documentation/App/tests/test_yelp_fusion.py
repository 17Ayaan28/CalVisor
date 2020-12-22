import unittest, datetime
from app.Classes.Yelp_Fusion import Yelp_Fusion
from app.Classes.Coordinate import Coordinate

YELP_API_KEY = "fO8TiLtHX-rUF2d0_0l19QelvQoQmHghyQP395yuiRjmPI-5Oj6173IDuZ_Yo2tIBbnr8bxzv29wsgc9IYmCvUMcvjm1lsxHa2oVP_BbA2l69nr9kRFOT5P6-_tdXnYx"

class TestBusinessSearch(unittest.TestCase):

    def test_business_search(self):
        # Init Class
        yelp_fusion_api = Yelp_Fusion(YELP_API_KEY)
        # Define Parameters
        term = "food"
        coordinate = Coordinate(-33.9182011, 151.2301125) # Keith Burrows Theatre, UNSW
        radius = 250 # Metres

        # Get places
        time = datetime.time(hour=12, minute=30)
        places = yelp_fusion_api.search_business(term, coordinate, radius, 2, time)

        # Assertions
        self.assertTrue(places != -1)
        print(len(places))
        self.assertTrue(len(places) > 1 and len(places) <= 5)
        first_plc = places[0]
        self.assertTrue(first_plc.get_name() == "The Lounge")
        self.assertTrue(first_plc.get_addr() == "Library Rd Level 11 Unsw Library Building Kensington New South Wales 2033 Australia")
        self.assertTrue(first_plc.get_rating() == 4)
