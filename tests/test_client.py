from nose.tools import assert_equal
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

class MockRestkitResource(object):
    def __init__(self, host_str):
        self.host_str = host_str

    def fake_request(self, method, endpoint, **params):
        path = os.path.join(__file__, "%s_%s" % (method, endpoint))
        f = open(path, 'r')
        data = Bunch()
        data.body = f.read()
        f.close()
        return data

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

from bigdoor import Client

class TestClient(TestCase):
    def setUp(self):
        self.client = Client(TEST_APP_SECRET, TEST_APP_KEY)

    def test_client_init(self):
        # test the basics
        assert_equal(self.client.app_secret, TEST_APP_SECRET)
        assert_equal(self.client.app_key, TEST_APP_KEY)

    def test_generate_signature_with_params(self):
        expected_sig = '9d1550bb516ee2cc47d163b4b99f00e15c84b3cd32a82df9fd808aa0eb505f04'
        params = {'time': 1270503018.33, 'format': 'json'}
        url = "/api/publisher/%s/transaction_summary" % TEST_APP_KEY
        sig = self.client.generate_signature(url, params)
        assert_equal(expected_sig, sig)

    def test_generate_signature_without_params(self):
        expected_sig = 'fa5ae4f36a4d90abae0cbbe5fd3d59b73bae6638ff517e9c26be64569c696bcc'
        url = "/api/publisher/%s/transaction_summary" % TEST_APP_KEY
        sig = self.client.generate_signature(url)
        assert_equal(expected_sig, sig)
