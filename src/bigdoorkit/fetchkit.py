from google.appengine.api import urlfetch
from urllib import urlencode

class Response(object):
    """A simple compatibilty layer for RESTkit's responses on GAE.
    """
    def __init__(self, resp):
        self.resp = resp

    def body_string(self):
        return self.resp.content

class Resource(object):
    """A simple compatibility layer for RESTkit on GAE.
    """
    def __init__(self, host):
        self.host = host
        self.form_headers = {'Content-Type':
                             'application/x-www-form-urlencoded'}

    def _build_url(self, url, params):
        encoded_params = urlencode(params)
        if encoded_params:
            url = "%s?%s" % (url, encoded_params)
        url = "%s%s" % (self.host, url)
        return url

    def get(self, url, **params):
        url = self._build_url(url, params)
        resp = urlfetch.fetch(url=url)
        return Response(resp)

    def post(self, url, payload=None, **params):
        if payload is None:
            payload = {}
        encoded_payload = urlencode(payload)

        url = self._build_url(url, params)
        resp = urlfetch.fetch(url=url,
                              payload=encoded_payload,
                              method=urlfetch.POST,
                              headers=self.form_headers)
        return Response(resp)

    def put(self, url, payload=None, **params):
        if payload is None:
            payload = {}
        encoded_payload = urlencode(payload)

        url = self._build_url(url, params)
        resp = urlfetch.fetch(url=url,
                              payload=encoded_payload,
                              method=urlfetch.PUT,
                              headers=self.form_headers)
        return Response(resp)

    def delete(self, url, **params):
        url = self._build_url(url, params)
        resp = urlfetch.fetch(url=url,
                              method=urlfetch.DELETE)
        return Response(resp)
