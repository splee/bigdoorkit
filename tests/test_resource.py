import os
from nose.tools import assert_equal
from nose import SkipTest
from unittest import TestCase

from tests import *

from bigdoorkit.client import Client
from bigdoorkit.resources.level import NamedLevelCollection

class TestNamedLevelCollection(TestCase):

    def setUp(self):
        self.client = Client(TEST_APP_SECRET, TEST_APP_KEY)

    def test_get_no_params(self):
        """ test of getting a list of named level collections """

        named_level_collections = NamedLevelCollection.all(self.client)
        assert len(named_level_collections) == 1
        nlc = named_level_collections[0]
        assert_equal(nlc.pub_title, 'test title')
        assert_equal(nlc.pub_description, 'test description')
        assert_equal(nlc.end_user_title, 'test user title')
        assert_equal(nlc.end_user_description, 'test user description')
        assert_equal(nlc.currency_id, 4922)
