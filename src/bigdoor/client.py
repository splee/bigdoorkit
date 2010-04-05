import restkit
import hashlib
import json
from uuid import uuid4
from time import time as unix_time

__all__ = ["Client"]


class Client(object):
    """Requires `app_secret` and `app_key` as supplied by BigDoor.
    Optional `api_host` parameter allows for use with API compatible
    services and/or staging servers.
    """
    def __init__(self, app_secret, app_key, api_host=None):
        """Constructor for a `Client` object.

        more docs here please
        """
        self.app_secret = app_secret
        self.app_key = app_key
        if not api_host:
            api_host = "http://api.bigdoor.com"
        self.api_host = api_host
        self.base_url = "/api/publisher/%s" % self.app_key
        self.conn = restkit.Resource(self.api_host)

    def generate_token(self):
        return str(uuid4())

    def generate_signature(self, url, params=None):
        """Generates the appropriate signature given a url and optional
        params."""
        sig = url
        if params:
            sig += self._flatten_params(params)
        sig += self.app_secret
        return hashlib.sha256(sig).hexdigest()

    def _flatten_params(self, params):
        """Flattens a parameter dictionary for signature generation"""
        keys = params.keys()
        keys.sort()
        return "".join(["%s%s" % (k, params[k]) for k in keys if k not in ('sig', 'format')])

    def _sign_request(self, url, params):
        if params is None:
            params = {}
        if not "time" in params:
            params["time"] = str(unix_time())
        # force JSON encoding
        params["format"] = "json"
        sig = self.generate_signature(url, params)
        params["sig"] = sig
        return params

    def _abs_from_rel(self, url):
        return "%s/%s" % (self.base_url, url)

    def get(self, endpoint, params=None):
        url = self._abs_from_rel(endpoint)
        params = self._sign_request(url, params)
        r = self.conn.get(url, **params)
        return json.loads(r.body)

    def delete(self, endpoint, params=None):
        url = self._abs_from_rel(endpoint)
        params = self._sign_request(url, params)
        r = self.conn.delete(url, **params)
        return json.loads(r.body)

    def post(self, endpoint, params=None):
        url = self._abs_from_rel(endpoint)
        params = self._sign_request(url, params)
        r = self.conn.post(url, **params)
        return json.loads(r.body)

    def put(self, endpoint, params=None):
        url = self._abs_from_rel(endpoint)
        params = self._sign_request(url, params)
        r = self.conn.put(url, **params)
        return json.loads(r.body)
