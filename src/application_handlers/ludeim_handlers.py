import utils.response_constants as const
import utils.jsonrpc2 as rpc
import utils.logging as file_logger
import utils.database_helpers as db
import utils.ludeim_constants as lconst
from classes.ClassAdmin import Admin
from classes.ClassUser import User
from classes.ClassLocation import Location
from classes.ClassItem import Item
from classes.ClassWrappedErrorResponse import WrappedErrorResponse
import traceback
import sys


# NOTE: not transaction wrapped
def __get_user_type(_id, conn, user_id):
    try:
        user = db.load_user_w_user_id(conn, user_id, _id)
        return user.type
    except WrappedErrorResponse as e:
        e.methods.append("__get_user_type")
        raise e
    except Exception as e:
        raise WrappedErrorResponse(
            rpc.make_error_resp(const.GET_USER_TYPE_UNKNOWN_CODE, const.GET_USER_TYPE_UNKNOWN, _id),
            e,
            "__get_user_type"
        )


# NOTE: not transaction wrapped
def __get_user_username(_id, conn, user_id):
    try:
        user = db.load_user_w_user_id(conn, user_id, _id)
        return user.username
    except WrappedErrorResponse as e:
        e.methods.append("__get_user_username")
        raise e
    except Exception as e:
        raise WrappedErrorResponse(
            rpc.make_error_resp(const.GET_USER_USERNAME_UNKNOWN_CODE, const.GET_USER_USERNAME_UNKNOWN, _id),
            e,
            "__get_user_username"
        )


# NOTE: not transaction wrapped
# def __get_user_password_hash(_id, conn, uuid):
#     try:
#         user = db.load_user(conn, uuid, _id)
#         return user.password_hash
#     except WrappedErrorResponse as e:
#         e.methods.append("__get_user_password_hash")
#         raise e
#     except Exception as e:
#         raise WrappedErrorResponse(
#             rpc.make_error_resp(const.GET_USER_PASSWORD_HASH_UNKNOWN_CODE, const.GET_USER_PASSWORD_HASH_UNKNOWN, _id),
#             e,
#             "__get_user_password_hash"
#         )


# NOTE: not transaction wrapped
# def __get_user_avatar(_id, conn, uuid):
#     try:
#         user = db.load_user(conn, uuid, _id)
#         return user.avatar
#     except WrappedErrorResponse as e:
#         e.methods.append("__get_user_avatar")
#         raise e
#     except Exception as e:
#         raise WrappedErrorResponse(
#             rpc.make_error_resp(const.GET_USER_AVATAR_UNKNOWN_CODE, const.GET_USER_AVATAR_UNKNOWN, _id),
#             e,
#             "__get_user_avatar"
#         )


# NOTE: not transaction wrapped
# def __get_user_location_uuids(_id, conn, uuid):
#     try:
#         return db.get_user_locs(conn, uuid)
#     except WrappedErrorResponse as e:
#         e.methods.append("__get_user_location_uuids")
#         raise e
#     except Exception as e:
#         raise WrappedErrorResponse(
#             rpc.make_error_resp(const.GET_USER_LOCATION_UUIDS_UNKNOWN_CODE, const.GET_USER_LOCATION_UUIDS_UNKNOWN, _id),
#             e,
#             "__get_user_location_uuids"
#         )


# NOTE: not transaction wrapped
# def __get_user_item_uuids(_id, conn, uuid):
#     try:
#         return db.get_user_items(conn, uuid)
#     except WrappedErrorResponse as e:
#         e.methods.append("__get_user_item_uuids")
#         raise e
#     except Exception as e:
#         raise WrappedErrorResponse(
#             rpc.make_error_resp(const.GET_USER_ITEM_UUIDS_UNKNOWN_CODE, const.GET_USER_ITEM_UUIDS_UNKNOWN, _id),
#             e,
#             "__get_user_item_uuids"
#         )


# ----------------------------------------------------------------------------------------------------------------------


# NOTE: not transaction wrapped
# def __get_location_type(_id, conn, uuid):
#     try:
#         loc = db.load_location(conn, uuid, _id)
#         return loc.type
#     except WrappedErrorResponse as e:
#         e.methods.append("__get_location_type")
#         raise e
#     except Exception as e:
#         raise WrappedErrorResponse(
#             rpc.make_error_resp(const.GET_LOC_TYPE_UNKNOWN_CODE, const.GET_LOC_TYPE_UNKNOWN, _id),
#             e,
#             "__get_location_type"
#         )


# NOTE: not transaction wrapped
# def __get_location_user_uuids(_id, conn, uuid):
#     try:
#         return db.get_loc_users(conn, uuid)
#     except WrappedErrorResponse as e:
#         e.methods.append("__get_location_user_uuids")
#         raise e
#     except Exception as e:
#         raise WrappedErrorResponse(
#             rpc.make_error_resp(const.GET_LOC_USER_UUIDS_UNKNOWN_CODE, const.GET_LOC_USER_UUIDS_UNKNOWN, _id),
#             e,
#             "__get_location_user_uuids"
#         )


# NOTE: not transaction wrapped
# def __get_location_item_uuids(_id, conn, uuid):
#     try:
#         return db.get_loc_items(conn, uuid)
#     except WrappedErrorResponse as e:
#         e.methods.append("__get_location_item_uuids")
#         raise e
#     except Exception as e:
#         raise WrappedErrorResponse(
#             rpc.make_error_resp(const.GET_LOC_ITEM_UUIDS_UNKNOWN_CODE, const.GET_LOC_ITEM_UUIDS_UNKNOWN, _id),
#             e,
#             "__get_location_item_uuids"
#         )


# NOTE: not transaction wrapped
# def __get_location_name(_id, conn, uuid):
#     try:
#         loc = db.load_location(conn, uuid, _id)
#         return loc.name
#     except WrappedErrorResponse as e:
#         e.methods.append("__get_location_name")
#         raise e
#     except Exception as e:
#         raise WrappedErrorResponse(
#             rpc.make_error_resp(const.NONEXISTENT_LOC_CODE, const.NONEXISTENT_LOC, _id),
#             e,
#             "__get_location_name"
#         )


# NOTE: not transaction wrapped
# def __get_location_address(_id, conn, uuid):
#     try:
#         loc = db.load_location(conn, uuid, _id)
#         return loc.address
#     except WrappedErrorResponse as e:
#         e.methods.append("__get_location_address")
#         raise e
#     except Exception as e:
#         raise WrappedErrorResponse(
#             rpc.make_error_resp(const.NONEXISTENT_LOC_CODE, const.NONEXISTENT_LOC, _id),
#             e,
#             "__get_location_address"
#         )


# NOTE: not transaction wrapped
# def __get_location_latitude(_id, conn, uuid):
#     try:
#         loc = db.load_location(conn, uuid, _id)
#         return loc.latitude
#     except WrappedErrorResponse as e:
#         e.methods.append("__get_location_latitude")
#         raise e
#     except Exception as e:
#         raise WrappedErrorResponse(
#             rpc.make_error_resp(const.NONEXISTENT_LOC_CODE, const.NONEXISTENT_LOC, _id),
#             e,
#             "__get_location_latitude"
#         )


# NOTE: not transaction wrapped
# def __get_location_longitude(_id, conn, uuid):
#     try:
#         loc = db.load_location(conn, uuid, _id)
#         return loc.longitude
#     except WrappedErrorResponse as e:
#         e.methods.append("__get_location_longitude")
#         raise e
#     except Exception as e:
#         raise WrappedErrorResponse(
#             rpc.make_error_resp(const.NONEXISTENT_LOC_CODE, const.NONEXISTENT_LOC, _id),
#             e,
#             "__get_location_longitude"
#         )


# NOTE: not transaction wrapped
# def __get_location_details(_id, conn, uuid):
#     try:
#         loc = db.load_location(conn, uuid, _id)
#         return loc.details
#     except WrappedErrorResponse as e:
#         e.methods.append("__get_location_details")
#         raise e
#     except Exception as e:
#         raise WrappedErrorResponse(
#             rpc.make_error_resp(const.NONEXISTENT_LOC_CODE, const.NONEXISTENT_LOC, _id),
#             e,
#             "__get_location_details"
#         )


# NOTE: not transaction wrapped
# def __get_location_photo(_id, conn, uuid):
#     try:
#         loc = db.load_location(conn, uuid, _id)
#         return loc.photo
#     except WrappedErrorResponse as e:
#         e.methods.append("__get_location_photo")
#         raise e
#     except Exception as e:
#         raise WrappedErrorResponse(
#             rpc.make_error_resp(const.NONEXISTENT_LOC_CODE, const.NONEXISTENT_LOC, _id),
#             e,
#             "__get_location_photo"
#         )


# NOTE: not transaction wrapped
# def __get_location_representative(_id, conn, uuid):
#     try:
#         loc = db.load_location(conn, uuid, _id)
#         return loc.representative
#     except WrappedErrorResponse as e:
#         e.methods.append("__get_location_representative")
#         raise e
#     except Exception as e:
#         raise WrappedErrorResponse(
#             rpc.make_error_resp(const.NONEXISTENT_LOC_CODE, const.NONEXISTENT_LOC, _id),
#             e,
#             "__get_location_representative"
#         )


# ----------------------------------------------------------------------------------------------------------------------


# NOTE: not transaction wrapped
def __is_username_taken(conn, username):
    return len(conn.execute("""SELECT * FROM users WHERE username = ?""", (username,)).fetchall()) != 0


# NOTE: not transaction wrapped
def __is_adminname_taken(conn, username):
    return len(conn.execute("""SELECT * FROM admins WHERE username = ?""", (username,)).fetchall()) != 0


# WARNING: REFACTOR LINE - - - - - - - - - - - - - - - - - - - - - - - - -


# TODO:
#  - MAKE ADMIN ONLY
#  - further username validation
#  - further password hash validation
def add_user(params, _id, conn, logger, config, session):
    try:
        user = User(_type=params["type"],
                    username=params["username"],
                    password_hash=params["password_hash"])
        if user.type not in lconst.USER_TYPES:
            return rpc.make_error_resp(const.INVALID_USER_TYPE_CODE, const.INVALID_USER_TYPE, _id)
        if len(user.username) < lconst.MIN_USERNAME_LEN or len(user.username) > lconst.MAX_USERNAME_LEN:
            return rpc.make_error_resp(const.INVALID_USER_USERNAME_CODE, const.INVALID_USER_USERNAME, _id)
        if len(user.password_hash) < lconst.MIN_PASSWORD_HASH_LEN or len(user.password_hash) > lconst.MAX_PASSWORD_HASH_LEN:
            return rpc.make_error_resp(const.INVALID_USER_PASSWORD_HASH_CODE, const.INVALID_USER_PASSWORD_HASH, _id)
        with conn:
            conn.execute("BEGIN EXCLUSIVE")
            if __is_username_taken(conn, params["username"]):
                return rpc.make_error_resp(const.USERNAME_TAKEN_CODE, const.USERNAME_TAKEN, _id)
            db.save_new_user(conn, user, _id)
        return rpc.make_success_resp({"type": user.type, "user_id": user.user_id}, _id)
    except WrappedErrorResponse as e:
        file_logger.log_error({
            "method": "add_user " + str(e.methods),
            "params": params,
            "error": str(e.exception)
        })
        return e.response_obj
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        file_logger.log_error({
            "method": "add_user",
            "params": params,
            "error": str(e),
            "trace": str(traceback.extract_tb(exc_traceback))
        })
        return rpc.make_error_resp(
            const.INTERNAL_ERROR_CODE,
            const.INTERNAL_ERROR,
            _id)


# WARNING: REFACTOR LINE - - - - - - - - - - - - - - - - - - - - - - - - -


# TODO:
#  - narrow scope of valid locations for different user types
#  - validate location address
#  - validate location details (what are details even?)
#  - validate location representative
def add_location(params, _id, conn, logger, config, session):
    try:
        # NOTE: find user_id
        user_id = params.get("user_id", session.get("user_id", None))
        # CHECK: was a user_id found?
        if user_id is None:
            return rpc.make_error_resp(0,
                                       "PROBLEM: There was no `user_id` argument provided and no user_id could be "
                                       "located in the session.\n"
                                       "SUGGESTION: Either either try again with a `user_id` argument, call "
                                       "login() then try again, or use put_sess() to manually add your user_id to "
                                       "your session then try again.",
                                       _id)
        # CHECK: is the location type valid?
        if params["type"] not in lconst.LOCATION_TYPES:
            return rpc.make_error_resp(0,
                                       "PROBLEM: The provided location type is not valid.\n"
                                       "SUGGESTION: Try again with a valid location type.",
                                       _id)
        # CHECK: is the representative's title valid?
        if params["representative"]["title"] not in lconst.TITLES:
            return rpc.make_error_resp(0,
                                       "PROBLEM: The provided representative title is not valid.\n"
                                       "SUGGESTION: Try again with a valid representative title.",
                                       _id)
        location = Location(_type=params["type"],
                            name=params["name"],
                            address=params["address"],
                            details=params["details"],
                            latitude=params["latitude"],
                            longitude=params["longitude"],
                            representative=params["representative"])
        with conn:
            # NOTE: get a lock on the database
            conn.execute("BEGIN EXCLUSIVE")
            # NOTE: load the user
            user = db.load_user_w_user_id(conn, user_id, _id)
            # NOTE: add the location to the user's location_uuids list
            user.location_uuids.add(location.uuid)
            # NOTE: add the user to the location's user_uuids list
            location.user_uuids.add(user.uuid)
            # NOTE: save everything
            db.save_existing_user(conn, user, _id)
            db.save_new_location(conn, location, _id)
        return rpc.make_success_resp(location.one_hot_jsonify(), _id)
    except WrappedErrorResponse as e:
        file_logger.log_error({
            "method": "add_location" + str(e.methods),
            "params": params,
            "error": str(e.exception)
        })
        return e.response_obj
    except Exception as e:
        file_logger.log_error({
            "method": "add_location",
            "params": params,
            "error": str(e),
        })
        return rpc.make_error_resp(const.INTERNAL_ERROR_CODE, const.INTERNAL_ERROR, _id)


def add_item(params, _id, conn, logger, config, session):
    try:
        # NOTE: find user_id
        user_id = params.get("user_id", session.get("user_id", None))
        # CHECK: was a user_id found?
        if user_id is None:
            return rpc.make_error_resp(0,
                                       "PROBLEM: There was no `user_id` argument provided and no user_id could be "
                                       "located in the session.\n"
                                       "SUGGESTION: Either either try again with a `user_id` argument, call "
                                       "login() then try again, or use put_sess() to manually add your user_id to "
                                       "your session then try again.",
                                       _id)
        # NOTE: load the type
        _type = params.get("type", lconst.DIAMOND)
        # CHECK: is the type valid?
        if _type not in lconst.ITEM_TYPES:
            return rpc.make_error_resp(0,
                                       "PROBLEM: The designated type was not valid.\n"
                                       "SUGGESTION: Try again with a valid type.",
                                       _id)
        # NOTE: make the new item
        item = Item(_type=_type, location_uuids=[], user_uuids=[])
        # NOTE: make the item stationary
        item.status = lconst.STATIONARY
        with conn:
            # NOTE: get a lock on the database
            conn.execute("BEGIN EXCLUSIVE")
            # NOTE: load the user
            user = db.load_user_w_user_id(conn, user_id, _id)
            # CHECK: is the location attached to the user?
            if params["location_uuid"] not in user.location_uuids:
                return rpc.make_error_resp(0,
                                           "PROBLEM: The designated location uuid doesn't correspond to a location "
                                           "owned by the user.\n"
                                           "SUGGESTIONS: Try again with a valid location uuid.",
                                           _id)
            # NOTE: load the location
            location = db.load_location(conn, params["location_uuid"], _id)
            # NOTE: add the location to the item's location_uuids list
            item.location_uuids.append(location.uuid)
            # NOTE: add the user to the item's user_uuids list
            item.user_uuids.append(user.uuid)
            # NOTE: add the item to the user's item_uuids list
            user.item_uuids.add(item.uuid)
            # NOTE: add the item to the location's item_uuids list
            location.item_uuids.add(item.uuid)
            # NOTE: save everything
            db.save_new_item(conn, item, _id)
            db.save_existing_user(conn, user, _id)
            db.save_existing_location(conn, location, _id)
        return rpc.make_success_resp(item.one_hot_jsonify(), _id)
    except WrappedErrorResponse as e:
        file_logger.log_error({
            "method": "add_item" + str(e.methods),
            "params": params,
            "error": str(e.exception)
        })
        return e.response_obj
    except Exception as e:
        file_logger.log_error({
            "method": "add_item",
            "params": params,
            "error": str(e),
        })
        return rpc.make_error_resp(const.INTERNAL_ERROR_CODE, const.INTERNAL_ERROR, _id)


# UNTESTED
# UNDOCUMENTED
def add_admin(params, _id, conn, logger, config, session):
    try:
        # NOTE: make the new admin
        admin = Admin(username=params["username"], password_hash=params["password_hash"])
        with conn:
            # NOTE: get a lock on the database
            conn.execute("BEGIN EXCLUSIVE")
            # CHECK: is the admin-name free?
            if __is_adminname_taken(conn, params["username"]):
                return rpc.make_error_resp(const.USERNAME_TAKEN_CODE, const.USERNAME_TAKEN, _id)
            # NOTE: save the new admin
            db.save_new_admin(conn, admin, _id)
        return rpc.make_success_resp({"type": "admin", "user_id": admin.user_id}, _id)
    except WrappedErrorResponse as e:
        file_logger.log_error({
            "method": "add_admin " + str(e.methods),
            "params": params,
            "error": str(e.exception)
        })
        return e.response_obj
    except Exception as e:
        file_logger.log_error({
            "method": "add_admin",
            "params": params,
            "error": str(e)
        })
        return rpc.make_error_resp(const.INTERNAL_ERROR_CODE, const.INTERNAL_ERROR, _id)
