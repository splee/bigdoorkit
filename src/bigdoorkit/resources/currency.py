from bigdoorkit.resources.base import BDResource

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

