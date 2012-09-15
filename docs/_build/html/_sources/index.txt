.. BigDoorKit documentation master file, created by
   sphinx-quickstart on Mon Aug 16 14:44:11 2010.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

BigDoorKit Documentation
========================

BigDoorKit provides a pure python interface for BigDoor's REST API.

The `BigDoor`_ Platform allows developers to create and manage a virtual economy and meta-games for non-game websites.  The process of adding a meta-game layer to a website is commonly known as "gamification".

.. _BigDoor: http://www.bigdoor.com/

Installation
------------

BigDoorKit is available on pypi and can be installed with your favorite package installer.  To install via ``easy_install``::

    easy_install -U bigdoorkit

Basic Usage
-----------

The ``bigdoorkit`` client requires your app key and secret key as provided by BigDoor::

    >>> from bigdoorkit import Client
    >>> client = Client(app_secret, app_key)

The client instance can then be used to access any of the endpoints mentioned in the `BigDoor documentation`_ (requires signup).

.. note::
    The Client object provided by bigdoorkit allows you to discard the "boilerplate" section of the REST URLs shown in the BigDoor documentation.  This means that instead of using ``/api/publisher/[app_key]/currency_type`` as the ``endpoint`` parameter, you should pass the relative endpoint, i.e. ``currency_type``.

Since the ``currency_type`` endpoint is managed entirely by BigDoor you should be able to make the following request and get the same results without having to set up any information in your economy::

    >>> currency_types = client.get('currency_type')
    >>> from pprint import pprint
    >>> pprint(currency_types)
    [[{u'can_be_cross_publisher': 0,
       u'can_be_purchased': 1,
       u'can_be_rewarded': 0,
       u'created_timestamp': 1263933875,
       u'description': None,
       u'has_dollar_exchange_rate_integrity': 1,
       u'id': 1,
       u'modified_timestamp': 1263933875,
       u'read_only': 0,
       u'resource_name': u'currency_type',
       u'title': u'Purchase'},
      {u'can_be_cross_publisher': 0,
       u'can_be_purchased': 0,
       u'can_be_rewarded': 1,
       u'created_timestamp': 1263933875,
       u'description': None,
       u'has_dollar_exchange_rate_integrity': 0,
       u'id': 2,
       u'modified_timestamp': 1263933875,
       u'read_only': 0,
       u'resource_name': u'currency_type',
       u'title': u'Reward'},
      {u'can_be_cross_publisher': 0,
       u'can_be_purchased': 1,
       u'can_be_rewarded': 1,
       u'created_timestamp': 1263933875,
       u'description': u'',
       u'has_dollar_exchange_rate_integrity': 0,
       u'id': 3,
       u'modified_timestamp': 1264002256,
       u'read_only': 0,
       u'resource_name': u'currency_type',
       u'title': u'Hybrid'},
      {u'can_be_cross_publisher': 1,
       u'can_be_purchased': 0,
       u'can_be_rewarded': 0,
       u'created_timestamp': 1263933875,
       u'description': None,
       u'has_dollar_exchange_rate_integrity': 1,
       u'id': 4,
       u'modified_timestamp': 1263933875,
       u'read_only': 0,
       u'resource_name': u'currency_type',
       u'title': u'\xdcber'}],
     {}]

.. _BigDoor documentation: http://publisher.bigdoor.com/docs/endpoints

To get a specific object you simply add a valid ID to the endpoint::

    >>> reward_type = client.get('currency_type/2')
    >>> pprint(reward_type)
    [{u'can_be_cross_publisher': 0,
      u'can_be_purchased': 0,
      u'can_be_rewarded': 1,
      u'created_timestamp': 1263933875,
      u'description': u'',
      u'has_dollar_exchange_rate_integrity': 0,
      u'id': 2,
      u'modified_timestamp': 1263933875,
      u'read_only': 0,
      u'resource_name': u'currency_type',
      u'title': u'Redeemable Reward Currency'},
     {}]

Contributing
============

To contribute to BigDoorKit's development, please head to the official `BitBucket project page`_.

.. _BitBucket project page: http://bitbucket.org/splee/bigdoorkit
