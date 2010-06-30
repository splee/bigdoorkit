from bigdoorkit.resources.base import BDResource

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
                 **kw):
        self.guid = guid
        self.end_user_login = end_user_login
        super(EndUser, self).__init__(id, pub_title, pub_description,
                                      end_user_title, end_user_description,
                                      created_timestamp, modified_timestamp,
                                      **kw)
