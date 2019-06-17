Add Item
========

:strong:`Method Name:` :literal:`add_item`

:strong:`Permission Level:` |lit_user|_

:strong:`Argumentation:`

    * **user_id** *(string)* |lit_conditionally_optional|_ -- This is your |lit_user_id|_.

    * **type** *(string)* |lit_optional|_ -- This must be an |lit_item_type|_. It is the type of item you want to create, defaulting to :literal:`diamond`.

    * **location_uuid** *(string)* -- This must be a |lit_location_UUID|_. It indicates the location the item being added is at.

:strong:`Response Members:`

        This method returns the boolean :code:`true` upon success.

:strong:`Example Request:`

    Find out about the assumptions made when writing this example code, here_.

    .. code-block:: javascript

        {
            "jsonrpc": "2.0",
            "method": "add_item",
            "params": {
                "location_uuid": "9EBB1CA4388C13B7722A34AC63456C8FA1E59107374319115157D7B036656A7344647146AC743028AC3074C3DB9879766DEEAE3FC397D1FFDFBC121871508CCF"
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

    This method is intended to be used when creating a new item. Importantly, this is *not* the method called when accepting a transfer of an item into your inventory. That would be the |func_accept_transfer|_ method. When this method is called a few things happen. First, the item is created and added to the database. Second, the item and user are linked to each other. Thirdly, the item and location denoted by the :literal:`location_uuid` are linked to each other.

:strong:`Example Assumptions`

    .. _here:

    The examples above require a few assumptions to make sense. First, they assume the user sending the request is logged in, and second, they assume that the user is has a location attached to their account with the UUID 9EBB1...508CCF. Finally, this assumes the user is trying to create a :literal:`diamond`.

.. |lit_conditionally_optional| replace:: :literal:`conditionally optional`
.. |lit_item_type| replace:: :literal:`item type`
.. |lit_optional| replace:: :literal:`optional`
.. |lit_user| replace:: :literal:`user`
.. |lit_location_UUID| replace:: :literal:`location UUID`
.. |lit_user_id| replace:: :literal:`user_id`

.. |func_accept_transfer| replace:: :func:`accept_transfer`

.. _lit_item_type: ../constants/item_types.html
.. _lit_conditionally_optional: ../miscellaneous/optional_arguments.html
.. _lit_optional: ../miscellaneous/optional_arguments.html
.. _lit_user: ../miscellaneous/permissions.html
.. _lit_location_UUID: ../constants/uuids.html
.. _lit_user_id: ../constants/uuids.html

.. _func_accept_transfer: ../methods/accept_transfer.html
