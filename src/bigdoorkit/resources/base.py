from bigdoorkit.client import Client
from bigdoorkit.exc import MissingParentDetails
from datetime import datetime
from types import MethodType

def clean_obj_keys(data):
    """JSON returns unicode keys which cannot be passed to
    __init__ methods directly. Here we convert the keys to strings.
    """
    return dict([(str(k), v) for k, v in data.items()])

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
    def all(cls, client):
        """Retrieves all of the available objects"""
        if cls.parent_class and not getattr(cls, cls.parent_id_attr, None):
            raise MissingParentDetails()
        endpoint = cls.endpoint
        if cls.parent_class:
            endpoint = "%s/%s/%s" % (cls.parent_class.endpoint,
                                     getattr(cls, cls.parent_id_attr),
                                     cls.endpoint)
        data = client.get(endpoint)
        return [cls(**clean_obj_keys(i)) for i in data[0]]

    @classmethod
    def get(cls, id, client):
        """Retrieves an object with the given `id`, using the `client` object
        if passed.
        """
        data = client.get("%s/%s" % (cls.endpoint, id))
        return cls(**clean_obj_keys(data[0]))

    def save(self, client):
        """Create or Update this object.

        If the object has an id, this method will try to PUT, otherwise
        the HTTP method will be POST.
        """
        if not self.id:
            client.post(self.endpoint, self.to_dict())
        else:
            data = client.put(self.endpoint, self.to_dict())
            # XXX: This is pretty dirty. We'll see how it works out.
            self = self.__class__(**data)

    def __class_delete(cls, id, client=None):
        """Deletes an object identified by `id`"""
        if client is None:
            client = get_client()
        client.delete(cls.endpoint, id)

    delete = classmethod(__class_delete)

    def __instance_delete(self, obj, client=None):
        # XXX: may need to change to self.__class__.delete(self.id, client)
        return self.__class_delete(self.id, client)
