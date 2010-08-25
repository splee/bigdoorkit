import os
from nose.tools import assert_equal
from nose import SkipTest
from unittest import TestCase

from tests import TEST_APP_KEY, TEST_APP_SECRET

from bigdoorkit.client import Client
from bigdoorkit.resources.level import NamedLevelCollection, NamedLevel
from bigdoorkit.resources.award import NamedAwardCollection, NamedAward
from bigdoorkit.resources.good import NamedGoodCollection, NamedGood

class TestNamedLevelCollection(TestCase):

    def setUp(self):
        self.client = Client(TEST_APP_SECRET, TEST_APP_KEY)

    def test_get(self):
        """ test of getting a list of named level collections """

        named_level_collections = NamedLevelCollection.all(self.client)
        assert len(named_level_collections) == 1
        nlc = named_level_collections[0]
        assert_equal(nlc.pub_title, 'test title')
        assert_equal(nlc.pub_description, 'test description')
        assert_equal(nlc.end_user_title, 'test user title')
        assert_equal(nlc.end_user_description, 'test user description')
        assert_equal(nlc.currency_id, 4920)

class TestNamedLevel(TestCase):

    def setUp(self):
        self.client = Client(TEST_APP_SECRET, TEST_APP_KEY)
        
    def test_get(self):
        named_level = NamedLevel.get(7859, self.client)
        assert named_level
        assert named_level.named_level_collection_id
        assert_equal(named_level.named_level_collection_id, 2092)

class TestNamedAward(TestCase):

    def setUp(self):
        self.client = Client(TEST_APP_SECRET, TEST_APP_KEY)

    def test_get(self):
        
        named_award = NamedAward.get(7193, self.client)
        assert named_award.named_award_collection_id
        assert_equal(named_award.named_award_collection_id, 1920)
        assert_equal(named_award.pub_title, 'obligatory early achievement')
        assert_equal(named_award.pub_description, 'early achievement')
        assert_equal(named_award.end_user_title, 'just breath')
        assert_equal(named_award.end_user_description, 'congratulations')
        assert_equal(named_award.id, 7193)

class TestNamedAwardCollection(TestCase):

    def setUp(self):
        self.client = Client(TEST_APP_SECRET, TEST_APP_KEY)

    
    def test_all(self):

        nac = NamedAwardCollection.all(self.client)
        assert nac
        assert len(nac) == 1
        nac = nac[0]
        assert_equal(nac.pub_title, 'application achievements')
        assert_equal(nac.pub_description, 'a set of achievements that the '+\
                        'user can earn')
        assert_equal(nac.end_user_title, 'achievements')
        assert_equal(nac.end_user_description, 'things you can get')
        assert_equal(nac.id, 1920)

class TestNamedGood(TestCase):

    def setUp(self):
        self.client = Client(TEST_APP_SECRET, TEST_APP_KEY)

    def test_get(self):

        ng = NamedGood.get(6169, self.client)
        assert ng
        assert_equal(ng.pub_title, 'example good')
        assert_equal(ng.pub_description, 'something you can purchase')
        assert_equal(ng.end_user_title, 'example good')
        assert_equal(ng.end_user_description, 'something you can purchase')
        assert_equal(ng.id, 6169)
        assert_equal(ng.id, 6169)
