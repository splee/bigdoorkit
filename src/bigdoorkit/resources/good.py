from bigdoorkit.resources.base import BDResource
from bigdoorkit.resources.user import EndUser

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
                 **kw
                ):
        self.named_good_collection_id = named_good_collection_id
        self.relative_weight = relative_weight
        self.collection_resource_uri = collection_resource_uri
        super(NamedGood, self).__init__(id, pub_title, pub_description,
                                        end_user_title, end_user_description,
                                        created_timestamp, modified_timestamp,
                                        **kw)

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
                 **kw
                ):
        self.sender_end_user_login = sender_end_user_login
        self.reciever_end_user_login = reciever_end_user_login
        self.named_good_id = named_good_id
        self.end_user_message_subject = end_user_message_subject
        self.end_user_message_body = end_user_message_body
        super(Good, self).__init__(id, pub_title, pub_description,
                                   end_user_title, end_user_description,
                                   created_timestamp, modified_timestamp,
                                   **kw)
