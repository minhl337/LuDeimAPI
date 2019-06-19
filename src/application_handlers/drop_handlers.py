import utils.response_constants as const
import utils.jsonrpc2 as rpc
import utils.logging as file_logger
import utils.database_helpers as db
import utils.ludeim_constants as lconst
from classes.ClassWrappedErrorResponse import WrappedErrorResponse


# UNTESTED
# UNDOCUMENTED
def drop_item(params, _id, conn, logger, config, session):
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
        with conn:
            # NOTE: get a lock on the database
            conn.execute("BEGIN EXCLUSIVE")
            # NOTE: load the user
            user = db.load_user_w_user_id(conn, user_id, _id)
            # CHECK: is the item attached to the user?
            if params["item_uuid"] not in user.item_uuids | user.outgoing_item_uuids:
                return rpc.make_error_resp(0,
                                           "PROBLEM: The designated item uuid doesn't correspond to an item "
                                           "owned by the user.\n"
                                           "SUGGESTIONS: Try again with a valid item uuid.",
                                           _id)
            # NOTE: load the item
            item = db.load_item(conn, params["item_uuid"], _id)
            # CHECK: is the item stationary?
            if item.status != lconst.STATIONARY:
                return rpc.make_error_resp(0,
                                           "PROBLEM: The designated item uuid corresponds to a non-stationary item.\n"
                                           "SUGGESTION: Try calling rescind_transfer() then trying again.",
                                           _id)
            # NOTE: load the item's location
            location = db.load_location(conn, item.location_uuids[-1], _id)
            # NOTE: set status to retired
            item.status = lconst.RETIRED
            # NOTE: remove the item from the user's item_uuids list
            user.item_uuids.discard(item.uuid)
            # NOTE: remove the item from the location's item_uuids list
            location.item_uuids.discard(item.uuid)
            # NOTE: save everything
            db.save_existing_item(conn, item, _id)
            db.save_existing_user(conn, user, _id)
            db.save_existing_location(conn, location, _id)
        return rpc.make_success_resp(item.one_hot_encode(), _id)
    except WrappedErrorResponse as e:
        file_logger.log_error({
            "method": "drop_item" + str(e.methods),
            "params": params,
            "error": str(e.exception)
        })
        return e.response_obj
    except Exception as e:
        file_logger.log_error({
            "method": "drop_item",
            "params": params,
            "error": str(e),
        })
        return rpc.make_error_resp(const.INTERNAL_ERROR_CODE, const.INTERNAL_ERROR, _id)


# UNTESTED
# UNDOCUMENTED
def drop_location(params, _id, conn, logger, config, session):
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
            # CHECK: is the location empty of items?
            if len(location.item_uuids) != 0:
                return rpc.make_error_resp(0,
                                           "PROBLEM: The designated location uuid corresponds to a non-empty "
                                           "location.\n"
                                           "SUGGESTION: Try transferring all items then trying again.",
                                           _id)
            # NOTE: remove the location from the user's location_uuids list
            user.location_uuids.discard(location.uuid)
            # NOTE: save everything
            db.save_existing_location(conn, location, _id)
        return rpc.make_success_resp(location.one_hot_encode(), _id)
    except WrappedErrorResponse as e:
        file_logger.log_error({
            "method": "drop_location" + str(e.methods),
            "params": params,
            "error": str(e.exception)
        })
        return e.response_obj
    except Exception as e:
        file_logger.log_error({
            "method": "drop_location",
            "params": params,
            "error": str(e),
        })
        return rpc.make_error_resp(const.INTERNAL_ERROR_CODE, const.INTERNAL_ERROR, _id)


# UNTESTED
# UNDOCUMENTED
def drop_user(params, _id, conn, logger, config, session):
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
        with conn:
            # NOTE: get a lock on the database
            conn.execute("BEGIN EXCLUSIVE")
            # NOTE: load the user
            user = db.load_user_w_user_id(conn, user_id, _id)
            # CHECK: does the user have no items?
            if len(user.item_uuids | user.incoming_item_uuids | user.outgoing_item_uuids) != 0:
                return rpc.make_error_resp(0,
                                           "PROBLEM: The designated user has at least 1 item under their ownership or "
                                           "currently incoming.\n"
                                           "SUGGESTION: Try transferring/dropping/reject all items then trying again.",
                                           _id)
            # CHECK: does the user have no locations?
            if len(user.location_uuids) != 0:
                return rpc.make_error_resp(0,
                                           "PROBLEM: The designated user has at least 1 location attached to their "
                                           "account.\n"
                                           "SUGGESTION: Try dropping all locations then trying again.",
                                           _id)
            # NOTE: delete the user
            conn.execute("""DELETE FROM users WHERE uuid = ?""", (user.uuid,))
        return rpc.make_success_resp(True, _id)
    except WrappedErrorResponse as e:
        file_logger.log_error({
            "method": "drop_user" + str(e.methods),
            "params": params,
            "error": str(e.exception)
        })
        return e.response_obj
    except Exception as e:
        file_logger.log_error({
            "method": "drop_user",
            "params": params,
            "error": str(e),
        })
        return rpc.make_error_resp(const.INTERNAL_ERROR_CODE, const.INTERNAL_ERROR, _id)