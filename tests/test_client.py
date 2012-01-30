# -*- coding: utf-8 -*-

from nose.tools import assert_equal
from nose import SkipTest
from unittest import TestCase

from bigdoorkit import Client

from tests import *

class TestClient(TestCase):
    def setUp(self):
        self.client = Client(TEST_APP_SECRET, TEST_APP_KEY)

    def test_client_init(self):
        # test the basics
        assert_equal(self.client.app_secret, TEST_APP_SECRET)
        assert_equal(self.client.app_key, TEST_APP_KEY)

    def test_generate_signature(self):
        expected_sig = '9d1550bb516ee2cc47d163b4b99f00e15c84b3cd32a82df9fd808aa0eb505f04'
        params = {'time': 1270503018.33}
        url = "/api/publisher/%s/transaction_summary" % TEST_APP_KEY
        sig = self.client.generate_signature(url, params)
        assert_equal(expected_sig, sig)

    def test_generate_signature_without_params(self):
        expected_sig = 'fa5ae4f36a4d90abae0cbbe5fd3d59b73bae6638ff517e9c26be64569c696bcc'
        url = "/api/publisher/%s/transaction_summary" % TEST_APP_KEY
        sig = self.client.generate_signature(url)
        assert_equal(expected_sig, sig)

    def test_generate_signature_with_whitelisted_params(self):
        expected_sig = 'fa5ae4f36a4d90abae0cbbe5fd3d59b73bae6638ff517e9c26be64569c696bcc'
        url = "/api/publisher/%s/transaction_summary" % TEST_APP_KEY
        params = {'format': 'json',
                  'sig': 'this_sig_is_fake!'}
        sig = self.client.generate_signature(url, params)
        assert_equal(expected_sig, sig)

    def test_generate_signature_with_post_params(self):
        from time import time
        expected_sig = 'cd073723c4901b57466694f63a2b7746caf1836c9bcdd4f98d55357334c2de64'
        url = "/api/publisher/%s/currency/1" % TEST_APP_KEY
        query_params = {'format': 'json',
                        'time': '1270517162.52'}
        body_params = {'end_user_description': 'Testing signature generation.',
                       'time': '1270517162.52',
                       'token': 'bd323c0ca7c64277ba2b0cd9f93fe463'}
        sig = self.client.generate_signature(url, query_params, body_params)
        assert_equal(expected_sig, sig)

    def test_generate_signature_with_unicode(self):
        expected_sig = 'bc41b88b9cf85434893169cd844da161530ee645fc18dc64c51568ed3b0de075'
        url = "/api/publisher/%s/currency/1" % TEST_APP_KEY

        title = 'Bashō\'s "old pond"'.decode('utf-8')
        description = '古池や蛙飛込む水の音'.decode('utf-8')

        query_params = {'format': 'json',
                        'time': '1270517162.52'}

        body_params = {'end_user_title': title,
                       'end_user_description': description,
                       'time': '1270517162.52',
                       'token': 'bd323c0ca7c64277ba2b0cd9f93fe463'}

        sig = self.client.generate_signature(url, query_params, body_params)
        assert_equal(expected_sig, sig)

    def test_get(self):
        result = self.client.get("transaction_summary")
        assert_equal(len(result[0][0]), 10)

    def test_delete(self):
        raise SkipTest()
        result = self.client.delete("currency/1")

    def test_post(self):
        raise SkipTest()
        result = self.client.post("currency")

    def test_put(self):
        raise SkipTest()
        result = self.client.put("currency/1")
