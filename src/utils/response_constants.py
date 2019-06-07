# JSON-RPC 2.0 STANDARD
PARSE_ERR = "Parse error"
PARSE_ERR_CODE = -32700
INVALID_REQ = "Invalid Request"
INVALID_REQ_CODE = -32600
NO_METHOD = "Method not found"
NO_METHOD_CODE = -2601
INVALID_PARAMS = "Invalid params"
INVALID_PARAMS_CODE = -32602
INTERNAL_ERROR = "Internal error"
INTERNAL_ERROR_CODE = -32603

# APPLICATION SPECIFIC
GET_USER_TYPE_UNKNOWN_CODE = -1
GET_USER_TYPE_UNKNOWN = "An exception occurred while trying to get a user's type"
GET_USER_USERNAME_UNKNOWN_CODE = -2
GET_USER_USERNAME_UNKNOWN = "An exception occurred while trying to get a user's username"
GET_USER_PASSWORD_HASH_UNKNOWN_CODE = -3
GET_USER_PASSWORD_HASH_UNKNOWN = "An exception occurred while trying to get a user's password hash"
GET_USER_AVATAR_UNKNOWN_CODE = -4
GET_USER_AVATAR_UNKNOWN = "An exception occurred while trying to get a user's avatar"
GET_USER_LOCATION_UUIDS_UNKNOWN_CODE = -5
GET_USER_LOCATION_UUIDS_UNKNOWN = "An exception occurred while trying to get a user's location uuids"
NOT_LOGGED_IN_CODE = -6
NOT_LOGGED_IN = "User must be logged in to call this method"
NONEXISTENT_USER_CODE = -7
NONEXISTENT_USER = "The provided credentials don't correspond to an existing user"
NO_RESPONSE_CODE = -8
NO_RESPONSE = "NO RESPONSE"
USERNAME_TAKEN_CODE = -9
USERNAME_TAKEN = "The provided username is already in use"
INVALID_USER_TYPE_CODE = -10
INVALID_USER_TYPE = "The provided user type is not a valid user type"
INVALID_USER_USERNAME_CODE = -11
INVALID_USER_USERNAME = "The provided username does not conform to one or more of this application's minimum " \
                        "username requirements"
INVALID_USER_PASSWORD_HASH_CODE = -12
INVALID_USER_PASSWORD_HASH = "The provided password hash does not conform to one or more of this application's " \
                             "minimum password hash requirements"
INVALID_LOCATION_TYPE_CODE = -13
INVALID_LOCATION_TYPE = "The provided location type is not a valid location type"
NO_CORRESPONDING_USER_CODE = -14
NO_CORRESPONDING_USER = "There was no corresponding user to the information you provided"
INVALID_REPRESENTATIVE_TITLE_CODE = -15
INVALID_REPRESENTATIVE_TITLE = "The provided representative title is not valid"
NONEXISTENT_LOC_CODE = -16
NONEXISTENT_LOC = "There was a problem looking up a location"
GET_LOC_TYPE_UNKNOWN_CODE = -17
GET_LOC_TYPE_UNKNOWN = "An exception occurred while trying to get a location's type"
GET_USER_ITEM_UUIDS_UNKNOWN_CODE = -18
GET_USER_ITEM_UUIDS_UNKNOWN = "An exception occurred while trying to get a user's item uuids"
GET_LOC_USER_UUIDS_UNKNOWN_CODE = -19
GET_LOC_USER_UUIDS_UNKNOWN = "An exception occurred while trying to get a location's user uuids"
GET_LOC_ITEM_UUIDS_UNKNOWN_CODE = -20
GET_LOC_ITEM_UUIDS_UNKNOWN = "An exception occurred while trying to get a location's item uuids"
INVALID_ITEM_TYPE_CODE = -21
INVALID_ITEM_TYPE = "The provided item type is not a valid item type"

