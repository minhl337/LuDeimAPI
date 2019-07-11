import utils.response_constants as const
import utils.jsonrpc2 as rpc
import utils.logging as file_logger
import utils.database_helpers as db
from classes.ClassWrappedErrorResponse import WrappedErrorResponse


# NOTE: not transaction wrapped, TODO: make def
__is_username_taken = lambda _id, conn, username: len(conn.execute("""SELECT * FROM users WHERE username = ?""", (username,)).fetchall()) != 0


# UNDOCUMENTED
# UNTESTED
def get_user_items(params, _id, conn, logger, config, session):
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
            # NOTE: load the target user
            if "uuid" in params:
                target = db.load_user_w_uuid(conn, params["uuid"], _id)
            else:
                target = db.load_user_w_user_id(conn, user_id, _id)
            # NOTE: load the target's items
            items = [db.load_item(conn, uuid, _id) for uuid in (target.item_uuids | target.incoming_item_uuids | target.outgoing_item_uuids)]
        # NOTE: form the predicate function for the filter
        stages = [target.incoming_item_uuids, target.item_uuids, target.outgoing_item_uuids]
        p = lambda item: (
                ("status_filter" not in params or
                 item.status == params.get("status_filter")) and
                ("ownership_filter" not in params or
                 (item.uuid in target.incoming_item_uuids) == params["ownership_filter"]) and
                ("location_uuid_filter" not in params or
                 item.location_uuids[-1] == params["location_uuid_filter"]) and
                ("stage_filter" not in params or
                 item.uuid in stages[params["stage_filter"]]))
        return rpc.make_success_resp([i.one_hot_jsonify() for i in items if p(i)], _id)
    except WrappedErrorResponse as e:
        file_logger.log_error({
            "method": "get_user_items" + str(e.methods),
            "params": params,
            "error": str(e.exception)
        })
        return e.response_obj
    except Exception as e:
        file_logger.log_error({
            "method": "get_user_items",
            "params": params,
            "error": str(e),
        })
        return rpc.make_error_resp(const.INTERNAL_ERROR_CODE, const.INTERNAL_ERROR, _id)


# UNDOCUMENTED
# UNTESTED
def get_location_items(params, _id, conn, logger, config, session):
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
            # NOTE: load the target location
            target = db.load_location(conn, params["uuid"], _id)
            # NOTE: load the target's items
            items = [db.load_item(conn, uuid, _id) for uuid in (target.item_uuids | target.incoming_item_uuids | target.outgoing_item_uuids)]
        # NOTE: form the predicate function for the filter
        stages = [target.incoming_item_uuids, target.item_uuids, target.outgoing_item_uuids]
        p = lambda item: (
                ("status_filter" not in params or
                 item.status == params.get("status_filter")) and
                ("user_uuid_filter" not in params or
                 item.user_uuids[-1] == params["user_uuid_filter"]) and
                ("stage_filter" not in params or
                 item.uuid in stages[params["stage_filter"]]))
        return rpc.make_success_resp([i.one_hot_jsonify() for i in items if p(i)], _id)
    except WrappedErrorResponse as e:
        file_logger.log_error({
            "method": "get_location_items" + str(e.methods),
            "params": params,
            "error": str(e.exception)
        })
        return e.response_obj
    except Exception as e:
        file_logger.log_error({
            "method": "get_location_items",
            "params": params,
            "error": str(e),
        })
        return rpc.make_error_resp(const.INTERNAL_ERROR_CODE, const.INTERNAL_ERROR, _id)


def get_all_users(params, _id, conn, logger, config, session):
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
            # NOTE: load partial users
            db_resp = conn.execute("""SELECT uuid, type_, username, avatar, location_uuids, item_uuids FROM users""").fetchall()
        return rpc.make_success_resp([{
            "uuid": line[0],
            "type": line[1],
            "username": line[2],
            "avatar": line[3],
            "location_uuids": line[4],
            "item_uuids": line[5]} for line in db_resp], _id)
    except WrappedErrorResponse as e:
        file_logger.log_error({
            "method": "get_all_users" + str(e.methods),
            "params": params,
            "error": str(e.exception)
        })
        return e.response_obj
    except Exception as e:
        file_logger.log_error({
            "method": "get_all_users",
            "params": params,
            "error": str(e)
        })
        return rpc.make_error_resp(const.INTERNAL_ERROR_CODE, const.INTERNAL_ERROR, _id)


def get_user_locations(params, _id, conn, logger, config, session):
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
        return rpc.make_success_resp([i.one_hot_jsonify() for i in locations], _id)
    except WrappedErrorResponse as e:
        file_logger.log_error({
            "method": "get_user_locations" + str(e.methods),
            "params": params,
            "error": str(e.exception)
        })
        return e.response_obj
    except Exception as e:
        file_logger.log_error({
            "method": "get_user_locations",
            "params": params,
            "error": str(e),
        })
        return rpc.make_error_resp(const.INTERNAL_ERROR_CODE, const.INTERNAL_ERROR, _id)


def get_sister_items(params, _id, conn, logger, config, session):
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
            # NOTE: load the target location
            target = db.load_item(conn, params["item_uuid"], _id)
            # NOTE: load the target's items
            items = [db.load_item(conn, uuid, _id) for uuid in target.sister_items]
        return rpc.make_success_resp([i.one_hot_jsonify() for i in items], _id)
    except WrappedErrorResponse as e:
        file_logger.log_error({
            "method": "get_sister_items" + str(e.methods),
            "params": params,
            "error": str(e.exception)
        })
        return e.response_obj
    except Exception as e:
        file_logger.log_error({
            "method": "get_sister_items",
            "params": params,
            "error": str(e),
        })
        return rpc.make_error_resp(const.INTERNAL_ERROR_CODE, const.INTERNAL_ERROR, _id)