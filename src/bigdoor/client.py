import restkit
import weakref
import hashlib
import json
from urllib import urlencode
from bigdoor.exc import MissingClient
from types import MethodType
from uuid import uuid4
from time import time as unix_time
from datetime import datetime

__all__ = ["Client", "Currency", "Level"]

# This variable holds the latest incarnation of a client object
# allowing for resource specific objects to use client methods
# without requiring the app_secret and app_key every time they're
# instantiated.
#
# setting it to lambda: None allows the variable to behave as a
# weakref would before any Client object is instantiated.
__client_weakref = lambda: None

# non-class specific helper methods
def get_client(client=None):
    """Helper method for BDResource"""
    client = client or __client_weakref()
    if client is not None:
        return client
    raise MissingClient()

def clean_obj_keys(data):
    """JSON returns unicode keys which cannot be passed to
    __init__ methods directly. Here we convert the keys to strings.
    """
    return dict([(str(k), v) for k, v in data.items()])

class Client(object):

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
        __client_weakref = weakref.ref(self)

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

class BDResource(object):
    endpoint = None
    parent_class = None
    parent_id_attr = None

    def __init__(self,
                 id=None,
                 pub_title=None,
                 pub_description=None,
                 end_user_title=None,
                 end_user_description=None,
                 created_timestamp=None,
                 modified_timestamp=None,
                 **kw
                ):
        self.id = id
        self.pub_title = pub_title
        self.pub_description = pub_description
        self.end_user_title = end_user_title
        self.end_user_description = end_user_description

        if isinstance(created_timestamp, (int, float)):
            created_timestamp = datetime.fromtimestamp(created_timestamp)
        self.created_timestamp = created_timestamp

        if isinstance(modified_timestamp, (int, float)):
            modified_timestamp = datetime.fromtimestamp(modified_timestamp)
        self.modified_timestamp = modified_timestamp

        # make the delete method an instance method
        self.delete = MethodType(self.__instance_delete, self, self.__class__)

        self._undefined_kw = kw

    @classmethod
    def all(cls, client=None):
        """Retrives all of the available objects"""
        client = get_client(client)
        if cls.parent_class and not getattr(self, cls.parent_id_attr, None):
            raise MissingParentDetails()
        endpoint = cls.endpoint
        if cls.parent_class:
            endpoint = "%s/%s/%s" % (cls.parent_class.endpoint,
                                     getattr(self, cls.parent_id_attr),
                                     cls.endpoint)
        data = client.get(endpoint)
        return [cls(**clean_obj_keys(i)) for i in data[0]]

    @classmethod
    def get(cls, id, client=None):
        """Retrieves an object with the given `id`, using the `client` object
        if passed.
        """
        client = get_client(client)
        data = client.get("%s/%s" % (cls.endpoint, id))
        return cls(**clean_obj_keys(data[0]))

    def save(self, client=None):
        """Create or Update this object.

        If the object has an id, this method will try to PUT, otherwise
        the HTTP method will be POST.
        """
        client = get_client(client)
        if not self.id:
            client.post(self.endpoint, self.to_dict())
        else:
            data = client.put(self.endpoint, self.to_dict())
            # XXX: This is pretty dirty. We'll see how it works out.
            self = self.__class__(**data)

    def __class_delete(cls, id, client=None):
        """Deletes an object identified by `id`"""
        client = get_client(client)
        client.delete(self.endpoint, id)

    delete = classmethod(__class_delete)

    def __instance_delete(self, client=None):
        # XXX: may need to change to self.__class__.delete(self.id, client)
        return self.__class_delete(self.id, client)

class EndUser(BDResource):
    endpoint = "end_user"

    def __init__(self,
                 id=None,
                 pub_title=None,
                 pub_description=None,
                 end_user_title=None,
                 end_user_description=None,
                 created_timestamp=None,
                 modified_timestamp=None,
                 guid=None,
                 end_user_login=None,
                ):
        self.guid = guid
        self.end_user_login = end_user_login
        super(EndUser, self).__init__(id, pub_title, pub_description,
                                      end_user_title, end_user_description,
                                      created_timestamp, modified_timestamp)


class Currency(BDResource):
    endpoint = "currency"

    def __init__(self,
                 id=None,
                 pub_title=None,
                 pub_description=None,
                 end_user_title=None,
                 end_user_description=None,
                 created_timestamp=None,
                 modified_timestamp=None,
                 currency_type_id=None,
                 currency_type_description=None,
                 currency_type_title=None,
                 exchange_rate=None,
                 relative_weight=None,
                 **kw):
        self.currency_type_id = currency_type_id
        self.currency_type_description = currency_type_description
        self.currency_type_title = currency_type_title
        self.exchange_rate = exchange_rate
        self.relative_weight = relative_weight
        super(Currency, self).__init__(id, pub_title, pub_description,
                                       end_user_title, end_user_description,
                                       created_timestamp, modified_timestamp,
                                       **kw)

class Level(BDResource):
    endpoint = "level"
    parent_class = EndUser
    parent_id_attr = "end_user_login"

    def __init__(self,
                 id=None,
                 pub_title=None,
                 pub_description=None,
                 end_user_title=None,
                 end_user_description=None,
                 created_timestamp=None,
                 modified_timestamp=None,
                 end_user_login=None,
                 named_level_id=None,
                 transaction_group_id=None,
                 next_level_uri=None,
                 previous_level_uri=None,
                ):
        self.end_user_login = end_user_login
        self.named_level_id = named_level_id
        self.transaction_group_id = transaction_group_id
        self.next_level_uri = next_level_uri
        self.previous_level_uri = previous_level_uri
        super(Level, self).__init__(id, pub_title, pub_description,
                                    end_user_title, end_user_description,
                                    created_timestamp, modified_timestamp)


class NamedLevelCollection(BDResource):
    endpoint = "named_level_collection"

    def __init__(self,
                 id=None,
                 pub_title=None,
                 pub_description=None,
                 end_user_title=None,
                 end_user_description=None,
                 created_timestamp=None,
                 modified_timestamp=None,
                 currency_id=None,
                ):
        self.currency_id = currency_id
        super(NamedLevel, self).__init__(id, pub_title, pub_description,
                                         end_user_title, end_user_description,
                                         created_timestamp, modified_timestamp)

class NamedLevel(BDResource):
    endpoint = "named_level"
    parent_class = NamedLevelCollection
    parent_id_attr = "named_level_collection_id"

    def __init__(self,
                 id=None,
                 pub_title=None,
                 pub_description=None,
                 end_user_title=None,
                 end_user_description=None,
                 created_timestamp=None,
                 modified_timestamp=None,
                 named_level_collection_id=None,
                 threshold=None,
                 collection_resource_uri=None,
                ):
        self.named_level_collection_id = named_level_collection_id
        self.threshold = threshold
        self.collection_resource_uri = collection_resource_uri
        super(NamedLevel, self).__init__(id, pub_title, pub_description,
                                         end_user_title, end_user_description,
                                         created_timestamp, modified_timestamp)

class NamedGoodCollection(BDResource):
    endpoint = "named_good_collection"

class NamedGood(BDResource):
    endpoint = "named_good"
    parent_class = NamedGoodCollection
    parent_id_attr = "named_good_collection_id"

    def __init__(self,
                 id=None,
                 pub_title=None,
                 pub_description=None,
                 end_user_title=None,
                 end_user_description=None,
                 created_timestamp=None,
                 modified_timestamp=None,
                 named_good_collection_id=None,
                 relative_weight=None,
                 collection_resource_uri=None,
                ):
        self.named_good_collection_id = named_good_collection_id
        self.relative_weight = relative_weight
        self.collection_resource_uri = collection_resource_uri

class Good(BDResource):
    endpoint = "good"
    parent_class = EndUser
    parent_id_attr = "reciever_end_user_login"

    def __init__(self,
                 id=None,
                 pub_title=None,
                 pub_description=None,
                 end_user_title=None,
                 end_user_description=None,
                 created_timestamp=None,
                 modified_timestamp=None,
                 sender_end_user_login=None,
                 reciever_end_user_login=None,
                 named_good_id=None,
                 end_user_message_subject=None,
                 end_user_message_body=None,
                ):
        self.sender_end_user_login = sender_end_user_login
        self.reciever_end_user_login = reciever_end_user_login
        self.named_good_id = named_good_id
        self.end_user_message_subject = end_user_message_subject
        self.end_user_message_body = end_user_message_body
        super(Good, self).__init__(id, pub_title, pub_description,
                                   end_user_title, end_user_description,
                                   created_timestamp, modified_timestamp)

class NamedAwardCollection(BDResource):
    endpoint = "named_award_collection"

class NamedAward(BDResource):
    endpoint = "named_award"
    parent_class = NamedAwardCollection
    parent_id_attr = "named_award_collection_id"

    def __init__(self,
                 id=None,
                 pub_title=None,
                 pub_description=None,
                 end_user_title=None,
                 end_user_description=None,
                 created_timestamp=None,
                 modified_timestamp=None,
                 named_award_collection_id=None,
                 relative_weight=None,
                 collection_resource_uri=None,
                ):
        self.named_award_collection_id = named_award_collection_id
        self.relative_weight = relative_weight
        self.collection_resource_uri = collection_resource_uri
        super(NamedAward, self).__init__(id, pub_title, pub_description,
                                         end_user_title, end_user_description,
                                         created_timestamp, modified_timestamp)

class Award(BDResource):
    endpoint = "award"
    parent_class = EndUser
    parent_id_attr = "end_user_login"

    def __init__(self,
                 id=None,
                 pub_title=None,
                 pub_description=None,
                 end_user_title=None,
                 end_user_description=None,
                 created_timestamp=None,
                 modified_timestamp=None,
                 end_user_login=None,
                 named_award_id=None,
                ):
        self.end_user_login = end_user_login
        self.named_award_id = named_award_id
        super(Award, self).__init__(id, pub_title, pub_description,
                                    end_user_title, end_user_description,
                                    created_timestamp, modified_timestamp)
