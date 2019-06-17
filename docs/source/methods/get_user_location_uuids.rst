Get User Location UUIDs
=======================

.. warning::

    .. deprecated:: 0.0.1
        use |func_get_user_locations|_ instead

:strong:`Method Name:` :literal:`get_user_location_uuids`

:strong:`Permission Level:` |lit_public|_

:strong:`Argumentation Schemes:`

    .. admonition:: Argumentation Scheme 1

        * **username** *(string)* -- When looking up another user's |lit_location_UUIDs|_ use this argumentation scheme using their username as the argument.

    .. admonition:: Argumentation Scheme 2

        * **user_id** *(string)* |lit_conditionally_optional|_  -- When looking up your own |lit_location_UUIDs|_ you may either call |func_login|_ and then omit any arguments to this method or not call |func_login|_ and instead send your |lit_user_id|_ as an argument to this method.

:strong:`Response Members:`

        This method returns a |lit_list_of_location_UUIDs|_. If no location UUIDs were found for the requested user, then the list will be empty. However, if the user being looked up simply doesn't exist, then the method will return an error rather than an empty list.

:strong:`Example Request:`

    Find out about the assumptions made when writing this example code, here_.

    .. code-block:: javascript

        {
            "jsonrpc": "2.0",
            "method": "get_user_location_uuids",
            "params": {
                "username": "joe.bloggs"
            },
            "id": 1
        }

:strong:`Example Response:`

    Find out about the assumptions made when writing this example code, here_.

    .. code-block:: javascript

        {
            "jsonrpc": "2.0",
            "result": [
                "6BFAC148DCCA31C7BF61287C572A6E35ADDA51792941F75013B1141473F482CE09051FE0B70F960E5A00DE979366B0AAB3CE52A05B03987FFABDD781F569465C",
                "9EBB1CA4388C13B7722A34AC63456C8FA1E59107374319115157D7B036656A7344647146AC743028AC3074C3DB9879766DEEAE3FC397D1FFDFBC121871508CCF",
                "961BC747674A4A83A0F0D7B1B68E704023171F0D52D0B68115EF36353CE653FFEC34AFBE58FB221BC9E7F242BF6628D4733DC57F08633C0334F429768C5F13FF"
            ],
            "id": 1
        }

:strong:`Notes`

    This method was originally intended to be used in conjunction with the |func_get_location|_ method. However, it is now recommended to simply use |func_get_user_locations|_ method instead as it combines the previous multi-request scheme into a single request.

:strong:`Example Assumptions`

    .. _here:

    The examples above require a few assumptions to make sense. First, they assume that at some point in the past a user was added to the system with the username *joe.bloggs*, and second, they assume that Joe has 3 different locations attached his account.


.. |lit_conditionally_optional| replace:: :literal:`conditionally optional`
.. |lit_public| replace:: :literal:`public`
.. |lit_location_UUIDs| replace:: :literal:`location UUIDs`
.. |lit_user_id| replace:: :literal:`user_id`
.. |lit_list_of_location_UUIDs| replace:: :literal:`list of location UUIDs`

.. |func_get_user_locations| replace:: :func:`get_user_locations`
.. |func_login| replace:: :func:`login`
.. |func_get_location| replace:: :func:`get_location`

.. _lit_conditionally_optional: ../miscellaneous/optional_arguments.html
.. _lit_public: ../miscellaneous/permissions.html
.. _lit_location_UUIDs: ../constants/uuids.html
.. _lit_user_id: ../constants/uuids.html
.. _lit_list_of_location_UUIDs: ../constants/uuids.html

.. _func_get_user_locations: ../methods/get_user_locations.html
.. _func_login: ../methods/login.html
.. _func_get_location: ../methods/get_location.html
