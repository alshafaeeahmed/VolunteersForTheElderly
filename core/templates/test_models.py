import unittest
from django.test import TestCase
from core.models import Profile, PageUpdate, Site_Info, Post, Following, Follower, Comment, Contact_us, UrgentRequest


class TestProfile(unittest.TestCase):
    def setUp(self):
        Profile.user.create(name=Profile.user.name, is_valenteer=Ture)
        Profile.user.create(name=Profile.user.name, is_valenteer='False')

    def test_profile(self):
        user1 = Profile.user.get(name=Profile.user.name)
        user2 = Profile.user.get(name=Profile.user.name)
        self.assertEqual(user1.is_volunteer(), 'The user is volunteer')
        self.assertEqual(user2.speak(), 'The cat says "meow"')
