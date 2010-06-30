from bigdoorkit.resources.base import BDResource
from bigdoorkit.resources.user import EndUser

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
                 **kw
                ):
        self.named_award_collection_id = named_award_collection_id
        self.relative_weight = relative_weight
        self.collection_resource_uri = collection_resource_uri
        super(NamedAward, self).__init__(id, pub_title, pub_description,
                                         end_user_title, end_user_description,
                                         created_timestamp, modified_timestamp,
                                         **kw)

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
                 **kw
                ):
        self.end_user_login = end_user_login
        self.named_award_id = named_award_id
        super(Award, self).__init__(id, pub_title, pub_description,
                                    end_user_title, end_user_description,
                                    created_timestamp, modified_timestamp,
                                    **kw)
