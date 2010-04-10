import restkit
import hashlib
try:
    import json
except ImportError, e:
    import simplejson as json

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

    def generate_signature(self, url, query_params=None, body_params=None):
        """Generates the appropriate signature given a url and optional
        params."""
        sig = url
        if query_params:
            sig += self._flatten_params(query_params)
        if body_params:
            sig += self._flatten_params(body_params)
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
        """Used to sign post-like requests ("POST" and "PUT")

        This method automatically splits the parameters that are
        required in the query string from the rest of the parameters
        and signs the request's data appropriately.
        """
        # Split the parameters for use in the query string and the
        # request body
        if params is None:
            params = {}
        query_keys = ['sig', 'time', 'format']
        query_params = {}
        body_params = {}
        for k, v in params.iteritems():
            if k in query_keys:
                query_params[k] = v
            else:
                body_params[k] = v

        # add a time if it's missing
        if not 'time' in query_params and not 'time' in body_params:
            body_params['time'] = query_params['time'] = str(unix_time())
        elif 'time' in query_params:
            body_params['time'] = query_params['time']
        else:
            query_params['time'] = body_params['time']

        # add a token if it's missing
        if not 'token' in body_params:
            body_params['token'] = self.generate_token()

        query_params['sig'] = self.generate_signature(url, query_params, body_params)
        return query_params, body_params

    def _abs_from_rel(self, url):
        return "%s/%s" % (self.base_url, url)

    def _get(self, endpoint, params=None):
        url = self._abs_from_rel(endpoint)
        params = self._sign_getish(url, params)
        return self.conn.get(url, **params)

    def get(self, endpoint, params=None):
        r = self._get(endpoint, params)
        return json.loads(r.body)

    def _delete(self, endpoint, params=None):
        url = self._abs_from_rel(endpoint)
        params = self._sign_getish(url, params)
        return self.conn.delete(url, **params)

    def delete(self, endpoint, params=None):
        r = self._delete(endpoint, params)
        return json.loads(r.body)

    def _post(self, endpoint, params=None):
        url = self._abs_from_rel(endpoint)
        get_params, body_params = self._sign_postish(url, params)
        return self.conn.post(url, payload=body_params, **get_params)

    def post(self, endpoint, params=None):
        r = self._post(endpoint, params)
        return json.loads(r.body)

    def _put(self, endpoint, params=None):
        url = self._abs_from_rel(endpoint)
        get_params, body_params = self._sign_postish(url, params)
        #raise Exception("\nquery: %s\nbody: %s" % (get_params, body_params))
        return self.conn.put(url, payload=body_params, **get_params)

    def put(self, endpoint, params=None):
        r = self._put(endpoint, params)
        return json.loads(r.body)
