import unittest
from app.Classes.Recommendation_System import Recommendation_System
from app.Classes.Models import User
import datetime


class TestRecommendationSystem(unittest.TestCase):

    def test_recommend_food(self):
        Rec_Sys = Recommendation_System()

        owner = User(email="Bob@gmail.com", username="Bob", password="password")

        origin = "Main Library, University of New South Wales, Sydney, Australia"
        radius = 500
        day_of_week = 2
        start_time = datetime.time(hour=13, minute=30) # start : 1:30pm
        end_time = datetime.time(17, 0, 0) # next class: 5:00pm
        owner_id = 1

        events = Rec_Sys.recommend_food(owner, origin, radius, day_of_week, start_time, end_time)
        self.assertTrue(len(events) >= 1)
        # To print during pytest, uncomment False Assertion
        for event in events:
            event.user_id = owner.id
            print("########################")
            print("name: ", event.name)
            print("addr: ", event.addr)
            print("start: ", event.start_time)
            print("end: ", event.end_time)

        #assert False
