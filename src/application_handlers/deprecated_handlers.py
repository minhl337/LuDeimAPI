import utils.response_constants as const
import utils.jsonrpc2 as rpc
import utils.logging as file_logger
import utils.database_helpers as db
from classes.ClassWrappedErrorResponse import WrappedErrorResponse


# NOTE: not transaction wrapped
__is_username_taken = lambda _id, conn, username: len(conn.execute("""SELECT * FROM users WHERE username = ?""", (username,)).fetchall()) != 0


# UNDOCUMENTED
# DEPRECATED: use get_user_locations instead
def get_user_location_uuids(params, _id, conn, logger, config, session):
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
        if "username" in params:
            with conn:
                # NOTE: get a lock on the database
                conn.execute("BEGIN EXCLUSIVE")
                # CHECK: is there a user associated with the given username?
                if not __is_username_taken(_id, conn, params["username"]):
                    return rpc.make_error_resp(0,
                                               "PROBLEM: No user in the system exists with the designated username.\n"
                                               "SUGGESTION: Try a different username.",
                                               _id)
                # NOTE: load the target user
                target = db.load_user_w_uuid(conn,
                                             conn
                                             .execute("""SELECT uuid FROM users WHERE username = ?""",
                                                      (params["username"],))
                                             .fetchone()[0],
                                             _id)
                # NOTE: load the target's locations
                locations = [db.load_location(conn, uuid, _id) for uuid in target.location_uuids]
        else:
            with conn:
                # NOTE: get a lock on the database
                conn.execute("BEGIN EXCLUSIVE")
                # NOTE: load the caller's user
                caller = db.load_user_w_user_id(conn, user_id, _id)
                # NOTE: load the caller's locations
                locations = [db.load_location(conn, uuid, _id) for uuid in caller.location_uuids]
        return rpc.make_success_resp([i.uuid for i in locations], _id)
    except WrappedErrorResponse as e:
        file_logger.log_error({
            "method": "get_user_location_uuids" + str(e.methods),
            "params": params,
            "error": str(e.exception)
        })
        return e.response_obj
    except Exception as e:
        file_logger.log_error({
            "method": "get_user_location_uuids",
            "params": params,
            "error": str(e),
        })
        return rpc.make_error_resp(const.INTERNAL_ERROR_CODE, const.INTERNAL_ERROR, _id)


# UNDOCUMENTED
# DEPRECATED: use get_user_items instead
def get_user_item_uuids(params, _id, conn, logger, config, session):
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
        if "username" in params:
            with conn:
                # NOTE: get a lock on the database
                conn.execute("BEGIN EXCLUSIVE")
                # CHECK: is there a user associated with the given username?
                if not __is_username_taken(_id, conn, params["username"]):
                    return rpc.make_error_resp(0,
                                               "PROBLEM: No user in the system exists with the designated username.\n"
                                               "SUGGESTION: Try a different username.",
                                               _id)
                # NOTE: load the target user
                target = db.load_user_w_uuid(conn,
                                             conn
                                             .execute("""SELECT uuid FROM users WHERE username = ?""",
                                                      (params["username"],))
                                             .fetchone()[0],
                                             _id)
                # NOTE: load the target's items
                items = [db.load_item(conn, uuid, _id) for uuid in target.item_uuids | target.incoming_item_uuids | target.outgoing_item_uuids]
        else:
            with conn:
                # NOTE: get a lock on the database
                conn.execute("BEGIN EXCLUSIVE")
                # NOTE: load the caller's user
                caller = db.load_user_w_user_id(conn, user_id, _id)
                # NOTE: load the caller's items
                items = [db.load_item(conn, uuid, _id) for uuid in caller.item_uuids | caller.incoming_item_uuids | caller.outgoing_item_uuids]
        return rpc.make_success_resp([i.uuid for i in items], _id)
    except WrappedErrorResponse as e:
        file_logger.log_error({
            "method": "get_user_item_uuids" + str(e.methods),
            "params": params,
            "error": str(e.exception)
        })
        return e.response_obj
    except Exception as e:
        file_logger.log_error({
            "method": "get_user_item_uuids",
            "params": params,
            "error": str(e),
        })
        return rpc.make_error_resp(const.INTERNAL_ERROR_CODE, const.INTERNAL_ERROR, _id)


# DEPRECATED: use get_user_location instead
def get_location(params, _id, conn, logger, config, session):
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
            # NOTE: get target
            target = db.load_location(conn, params["location_uuid"], _id)
        return rpc.make_success_resp(target.one_hot_encode(), _id)
    except WrappedErrorResponse as e:
        file_logger.log_error({
            "method": "get_location" + str(e.methods),
            "params": params,
            "error": str(e.exception)
        })
        return e.response_obj
    except Exception as e:
        file_logger.log_error({
            "method": "get_location",
            "params": params,
            "error": str(e)
        })
        return rpc.make_error_resp(const.INTERNAL_ERROR_CODE, const.INTERNAL_ERROR, _id)