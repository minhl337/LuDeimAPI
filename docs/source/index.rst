.. LuDeimAPI documentation master file, created by
   sphinx-quickstart on Tue Jun  4 16:20:31 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to the LuDeimAPI documentation
======================================

LuDeimAPI is a JSON-RPC 2.0 compliant api designed for use in the LuDeim diamond supply chain management system. The api has a companion API called LuDeimStorageAPI which handles the storage and retrieval of non-trivial size objects within the system. This documentation will not go over this companion API as it is not intended to be called directly from a front-end application.

.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Miscellaneous

   miscellaneous/sessions
   miscellaneous/rpc
   miscellaneous/batch_requests


.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Constants

   constants/user_types
   constants/location_types
   constants/titles

.. toctree::
   :hidden:
   :maxdepth: 2
   :caption: Methods

   methods/add_user
   methods/add_location
   methods/login
   methods/logout
