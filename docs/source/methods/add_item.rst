Add Item
========

**METHOD NAME**
    *add_item*

**PERMISSION LEVEL**
    *user*

**ARGUMENTS**
    * **[optional if logged in and requesting one's own items]** **uuid:** string
    * **[optional, defaults to diamond]** **type:** string
    * **location_uuid:** string

**ARGUMENT CONSTRAINTS**
    * The type must be one of the valid types defined in the *Item Types* section of this document

**RESPONSE MEMBERS**
    * Response is just the boolean, *True*.

**EXAMPLE REQUEST**
    .. code-block:: javascript

        {
            "jsonrpc": "2.0",
            "method": "add_item",
            "params": {
                "location_uuid": "abcdefghabcdefghabcdefghabcdefghabcdefghabcdefghabcdefghabcdefgh"
            },
            "id": 1
        }

**EXAMPLE SUCCESSFUL RESPONSE**
    .. code-block:: javascript

        {
            "jsonrpc": "2.0",
            "result": true,
            "id": 1
        }

**NOTES**
    This endpoint is intended to be used when registering a new item. Every item has to have at least one location and user associated with it. No item may have more than one user associated with it. When calling this endpoint it is assumed that the uuid in the user's session should be used to create the item, however, a custom uuid can be specified. This intended for use by third-party interfaces NOT for general frontend development. Additionally, a list of a user's location uuids can be gotten from the **get_user_location_uuids** method.