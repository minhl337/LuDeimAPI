.. LuDeimAPI documentation master file, created by
   sphinx-quickstart on Tue Jun  4 16:20:31 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to the LuDeimAPI documentation
======================================

LuDeimAPI is a JSON-RPC 2.0 compliant API designed for use in the LuDeim diamond supply chain management system. The API has a companion API called LuDeimStorageAPI which handles the storage and retrieval of non-trivial size objects within the system. This documentation will not go over this companion API as it is not intended to be called directly from a front-end application.

.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Miscellaneous

   miscellaneous/sessions
   miscellaneous/rpc
   miscellaneous/batch_requests
   miscellaneous/permissions
   miscellaneous/optional_arguments

.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Constants, Structures, and Types

   constants/item_types
   constants/user_types
   constants/location_types
   constants/titles
   constants/uuids

.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Methods

   methods/login
   methods/logout
   methods/get_sess
   methods/put_sess
   methods/add_user
   methods/add_location
   methods/add_item
   methods/get_user_location_uuids
   methods/get_all_users
   methods/get_user_items
   methods/get_location
   methods/get_user_locations
   methods/change_username
