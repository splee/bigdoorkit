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
