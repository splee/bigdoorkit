import restkit
import hashlib
import json
from uuid import uuid4
from time import time as unix_time
from urllib import urlencode

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
        return uuid4().hex

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

    def _sign_getish(self, url, params):
        """Used to sign get-like requests ("GET" and "DELETE")"""
        if params is None:
            params = {}
        if not "time" in params:
            params["time"] = str(unix_time())
        sig = self.generate_signature(url, params)
        params["sig"] = sig
        return params

    def _sign_postish(self, url, params):
        """Used to sign post-like requests ("POST" and "PUT")"""
        # Split the parameters for use in the query string and the
        # request body
        if params is None:
            params = {}
        get_keys = ['sig', 'time', 'format']
        get_params = {}
        body_params = {}
        for k, v in params.iteritems():
            if k in get_keys:
                get_params[k] = v
            else:
                body_params[k] = v
        if 'time' in get_params:
            body_params['time'] = get_params['time']

        # add a token if it's missing
        if not 'token' in body_params:
            body_params['token'] = self.generate_token()
        body_params = self._sign_getish(url, body_params)
        get_params['sig'] = body_params['sig']
        del body_params['sig']
        return get_params, body_params

    def _abs_from_rel(self, url):
        return "%s/%s" % (self.base_url, url)

    def get(self, endpoint, params=None):
        url = self._abs_from_rel(endpoint)
        params = self._sign_getish(url, params)
        r = self.conn.get(url, **params)
        return json.loads(r.body)

    def delete(self, endpoint, params=None):
        url = self._abs_from_rel(endpoint)
        params = self._sign_getish(url, params)
        r = self.conn.delete(url, **params)
        return json.loads(r.body)

    def post(self, endpoint, params=None):
        url = self._abs_from_rel(endpoint)
        get_params, body_params = self._sign_postish(url, params)
        body = urlencode(body_params)
        r = self.conn.post(url, payload=body, **get_params)
        return json.loads(r.body)

    def put(self, endpoint, params=None):
        url = self._abs_from_rel(endpoint)
        get_params, body_params = self._sign_postish(url, params)
        body = urlencode(body_params)
        r = self.conn.put(url, payload=body, **params)
        return json.loads(r.body)
