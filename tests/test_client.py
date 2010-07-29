from nose.tools import assert_equal
from nose import SkipTest
from unittest import TestCase
import os

# Note: Below are two fake keys used for testing. They
# were created using an MD5 hash of 'test_app_key' and
# 'test_app_secret' respectively.
TEST_APP_KEY = '28d3da80bf36fad415ab57b3130c6cb6'
TEST_APP_SECRET = 'B66F956ED83AE218612CB0FBAC2EF01C'

class Bunch(dict):
    """A dict like object with the ability to get/set
    data via attribute access.

    >>> data = Bunch(foo='bar', baz=1)
    >>> data.foo
    'bar'
    >>> data['foo']
    'bar'
    >>> data.baz
    1
    >>> data['baz']
    1
    """
    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError:
            raise AttributeError("%s not found" % attr)

    def __setattr__(self, attr, value):
        self[attr] = value

class MockRestkitResponse(object):
    def __init__(self, body):
        self.body = body

    def body_string(self):
        return self.body

class MockRestkitResource(object):
    def __init__(self, host_str):
        self.host_str = host_str

    def fake_request(self, method, endpoint, **params):
        here = __file__.split("/")
        here = "/".join(here[:-1])

        short_endpoint = "%s_" % method
        short_endpoint += "_".join(endpoint.split("/")[4:])
        short_endpoint += ".json"

        path = os.path.join(here, "data", short_endpoint)
        path = os.path.abspath(path)
        f = open(path, 'r')
        resp = MockRestkitResponse(f.read())
        f.close()
        return resp

    def get(self, endpoint, **params):
        return self.fake_request("get", endpoint, **params)

    def delete(self, endpoint, **params):
        return self.fake_request("delete", endpoint, **params)

    def post(self, endpoint, **params):
        return self.fake_request("post", endpoint, **params)

    def put(self, endpoint, **params):
        return self.fake_request("put", endpoint, **params)

# monkeypatch the mock restkit.Resource
import restkit
_original_resource = restkit.Resource
restkit.Resource = MockRestkitResource

from bigdoorkit import Client

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
