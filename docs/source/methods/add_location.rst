Add Location
============

:strong:`Method Name:` :literal:`add_location`

:strong:`Permission Level:` |lit_user|_

:strong:`Argumentation:`

    * **uuid** *(string)* |lit_conditionally_optional|_ -- This is your |lit_UUID|_.

    * **type** *(string)* -- This must be a |lit_location_type|_. It is the type of location you want to create.

    * **name** *(string)* -- This is the name of the location you are creating.

    * **address** *(string)* -- This is the address of the location you are creating.

    * **latitude** *(float)* -- This is the latitude of the location you are creating.

    * **longitude** *(float)* -- This is the longitude of the location you are creating.

    * **details** *(string)* -- This is an arbitrary string with details about your location.

    * **representative**

        * **title** *(string)* -- This must be a |lit_representative_title|_. It is the title of the location's representative.

        * **first_name** *(string)* -- This is the first name of the location's representative.

        * **last_name** *(string)* --  This is the last name of the location's representative.

        * **contact_info** *(string)* -- This is the contact info of the location's representative. It can be whatever is easiest. E.g. email, phone, etc.

:strong:`Response Members:`

    This method returns the boolean :code:`true` upon success.

:strong:`Example Request:`

    Find out about the assumptions made when writing this example code, here_.

    .. code-block:: javascript

        {
            "jsonrpc": "2.0",
            "method": "add_location",
            "params": {
                "type": "mine",
                "name": "Kelsey Lake",
                "address": "Murfreesboro, Pike, Ouachita Mountains, Arkansas, United States",
                "latitude": 34.1,
                "longitude": 93.4,
                "details": "Commercial mining ventures failed, only diamond mine accessible to the general public. World's only perfect diamond found here.",
                "representative": {
                    "title": "MR",
                    "first_name": "John",
                    "last_name": "Doe",
                    "john.doe@gmail.com"
                }
            },
            "id": 1
        }

:strong:`Example Response:`

    Find out about the assumptions made when writing this example code, here_.

    .. code-block:: javascript

        {
            "jsonrpc": "2.0",
            "result": true,
            "id": 1
        }

:strong:`Notes`

    This method is intended to be used when creating a new location. When this method is called a few things happen. First, the location is created and added to the database. Second, the location and user are linked to each other.

:strong:`Example Assumptions`

    .. _here:

    The examples above require an assumption to make sense. They assume the user sending the request is logged in.

.. |lit_representative_title| replace:: :literal:`representative title`
.. |lit_conditionally_optional| replace:: :literal:`conditionally optional`
.. |lit_location_type| replace:: :literal:`location type`
.. |lit_user| replace:: :literal:`user`
.. |lit_UUID| replace:: :literal:`UUID`

.. _lit_representative_title: ../constants/titles.html
.. _lit_conditionally_optional: ../miscellaneous/optional_arguments.html
.. _lit_location_type: ../constants/location_types.html
.. _lit_user: ../miscellaneous/permissions.html
.. _lit_UUID: ../constants/uuids.html
