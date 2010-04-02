import uuid, hashlib, urllib
from urllib2 import urlopen
from urllib import urlencode
from lib.restful import Request
from time import time as unix_time
from uuid import uuid4
import json

__version__ = "0.1"

__all__ = ["BigdoorClient", "BigdoorException"]

class BigdoorException(Exception):
    """The base Exception type for this library"""

class BigdoorClient(object):
    """Implements a client for the BigDoor API"""

    def __init__(self, app_key, app_secret, api_host=None):
        if not api_host:
            api_host = "http://api.bigdoor.com"
        self.api_host = api_host
        self.app_key = app_key
        # TODO: validation of secret
        self.app_secret = app_secret
        self.url_base = "%s/publisher/%s" % (self.api_host, self.app_key)

    def transaction_summary(self, neo, end_user, currency,
                           named_transaction_group, named_transaction,
                            transaction_group_id, options=None):
        params = self._validate_options(options)
        params.update(dict(neo=neo, end_user=end_user, currency=currency,
                           named_transaction_group=named_transaction_group,
                           named_transaction=named_transaction,
                           transaction_group_id=transaction_group_id)
                     )
        return self.get("transaction_summary", params)

    def award_summary(self, named_award, named_award_collection, end_user,
                      options=None):
        params = self._validate_options(options)
        params.update(dict(named_award=named_award,
                           named_award_collection=named_award_collection,
                           end_user=end_user))
        return self.get("award_summary", params)

    def level_summary(self, named_level, named_level_collection, end_user,
                      options=None):
        params = self._validate_options(options)
        params.update(dict(named_level=named_level,
                           named_level_collection=named_level_collection,
                           end_user=end_user)
                     )
        return self.get("level_summary", params)

    def good_summary(self, named_good, named_good_collection, end_user,
                     good_sender, good_receiver, currency,
                     named_transaction, transaction_group_id,
                     options=None):
        params = self._validate_options(options)
        params.update(dict(named_good=named_good,
                           named_good_collection=named_good_collection,
                           end_user=end_user,
                           good_sender=good_sender,
                           good_receiver=good_receiver,
                           currency=currency,
                           named_transaction=named_transaction,
                           transaction_group_id=transaction_group_id)
                     )
        return self.get("good_summary", params)

    def end_user(self, user_id, options=None):
        params = self._validate_options(options)
        return self.get("end_user/%s" % user_id, params)

    def end_user_balance(self, user_id, currency_id=None, options=None):
        params = self._validate_options(options)
        url = "end_user/%s/balance" % user_id
        if currency_id:
            url += "/%s" % currency_id
        return self.get(url, params)

    def end_user_transaction(self, user_id, transaction_id=None,
                             options=None):
        params = self._validate_options(options)
        url = "end_user/%s/transaction" % user_id
        if transaction_id:
            url += "/%s" % transaction_id
        return self.get(url, params)

    def end_user_level(self, user_id, level_id=None, options=None):
        params = self._validate_options(options)
        url = "end_user/%s/level" % user_id
        if level_id:
            url += "/%s" % level_id
        return self.get(url, params)

    def end_user_award(self, user_id, award_id=None, options=None):
        params = self._validate_options(options)
        url = "end_user/%s/award" % user_id
        if award_id:
            url += "/%s" % level_id
        return self.get(url, params)

    def end_user_good(self, user_id, good_id=None, options=None):
        params = self._validate_options(options)
        url = "end_user/%s/good" % user_id
        if good_id:
            url += "/%s" % good_id
        return self.get(url, params)

    def end_user_currency(self, user_id, currency_id=None, options=None):
        params = self._validate_options(options)
        url = "end_user/%s/currency" % user_id
        if currency_id:
            url += "/%s" % currency_id
        return self.get(url, params)

    def create_named_transaction_group(self):
        raise NotImplementedError

    def named_transaction_group(self, trans_group_id=None, options=None):
        params = self._validate_options(options)
        url = "named_transaction_group"
        if trans_group_id:
            url += "/%s" % trans_group_id
        return self.get(url, params)

    def execute_named_transaction_group(self, trans_group_id, end_user_id,
                                        options=None):
        params = self._validate_options(options)
        url = "named_transaction_group/%s/execute/%s" % (trans_group_id,
                                                         end_user_id)
        return self.post(url, params)

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
        return "".join(["%s%s" % (k, params[k]) for k in keys])

    def _validate_options(self, options):
        if options is None:
            options = {}
        if not isinstance(options, dict):
            raise ValueError("options parameter must be of type dict, not %s" % type(options))
        return options.copy()

    def _sign_request_params(self, url, params):
        if not "time" in params:
            params["time"] = str(unix_time())
        sig = self.generate_signature(url, params)
        params["sig"] = sig

        return params

    def _preprocess_request(self, url, params):
        url = "%s/%s" % (self.base_url, url)
        params = self._sign_request_params(url, params)
        return url, params

    def post(self, url, params=None):
        """Sends a POST request.  This method automatically signs your
        request for you."""
        url, params = self._preprocess_request(url, params)
        req = Request(url, urlencode(params), http_method="POST")
        return self._send_request(req)

    def put(self, url, params=None):
        """Sends a PUT reqeust.  This method automatically signs your
        request for you."""
        url, params = self._preprocess_request(url, params)
        req = Request(url, urlencode(params), http_method="PUT")
        return self._send_request(req)

    def get(self, url, params=None):
        """Sends a GET request.  This method automatically signs your
        request for you."""
        url, params = self._preprocess_request(url, params)
        req = Request("%s?%s" % (url, urlencode(params)), http_method="GET")
        return self._send_request(req)

    def delete(self, url, params=None):
        """Sends a DELETE request.  This method automatically signs your
        request for you."""
        url, params = self._preprocess_request(url, params)
        req = Request("%s?%s" % (url, urlencode(params)), http_method="DELETE")
        return self._send_request(req)

    def _send_request(self, request):
        """Sends a request object and returns the resulting data"""
        #TODO: there needs to be much more error checking here
        response = json.loads(urlopen(request).read())
        return response
