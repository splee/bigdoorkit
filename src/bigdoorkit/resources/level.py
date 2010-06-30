from bigdoorkit.resources.base import BDResource
from bigdoorkit.resources.user import EndUser

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
                 **kw
                ):
        self.currency_id = currency_id
        super(NamedLevel, self).__init__(id, pub_title, pub_description,
                                         end_user_title, end_user_description,
                                         created_timestamp, modified_timestamp,
                                         **kw)

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
                 **kw
                ):
        self.named_level_collection_id = named_level_collection_id
        self.threshold = threshold
        self.collection_resource_uri = collection_resource_uri
        super(NamedLevel, self).__init__(id, pub_title, pub_description,
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
                 **kw
                ):
        self.end_user_login = end_user_login
        self.named_level_id = named_level_id
        self.transaction_group_id = transaction_group_id
        self.next_level_uri = next_level_uri
        self.previous_level_uri = previous_level_uri
        super(Level, self).__init__(id, pub_title, pub_description,
                                    end_user_title, end_user_description,
                                    created_timestamp, modified_timestamp,
                                    **kw)
