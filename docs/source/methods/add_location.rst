Add Location
============

**METHOD NAME**
    *add_location*

**PERMISSION LEVEL**
    *public*

**ARGUMENTS**
    * **[optional if logged in]** **uuid:** string
    * **type:** string
    * **name:** string
    * **address:** string
    * **latitude:** float
    * **longitude:** float
    * **details:** string
    * **representative:** object

        * **title:** string
        * **first_name:** string
        * **last_name:** string
        * **contact_info:** string

**ARGUMENT CONSTRAINTS**
    * The type must be one of the valid types defined in the *Location Types* section
    * The representative's title must be one of the valid titles defined in the *Titles* section

**RESPONSE MEMBERS**
    * Response is just the boolean, *True*.

**EXAMPLE REQUEST**
    .. code-block:: javascript

        {
            "jsonrpc": "2.0",
            "method": "add_location",
            "params": {
                "type": "mine",
                "name": "abcdefghijk",
                "address": "1234 Mountain Rd.",
                "latitude": 125.5,
                "longitude": 36.7,
                "details": "lorem ipsum",
                "representative": {
                    "title": "MR",
                    "first_name": "john",
                    "last_name": "doe",
                    "contact_info": "john.doe@company.com"
                }
            },
            "id": 1
        }