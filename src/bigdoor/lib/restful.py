import urllib2

__all__ = ["Request"]

class Request(urllib2.Request):
    """Implements a RESTful Request class based on urllib2.Request"""
    def __init__(self, url, data=None, headers={},
                 origin_req_host=None, unverifiable=False,
                 http_method=None):
        self.http_method = http_method
        super(Request, self).__init__(url, data, headers,
                                      origin_req_host, unverifiable)

    def get_method(self):
        if not self.http_method:
            return super(Request, self).get_method()
        return self.http_method
