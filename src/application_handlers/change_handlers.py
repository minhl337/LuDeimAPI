import utils.response_constants as const
import utils.jsonrpc2 as rpc
import utils.logging as file_logger
import utils.typing as t
import utils.database_helpers as db
import utils.ludeim_constants as lconst
from classes.ClassWrappedErrorResponse import WrappedErrorResponse


# UNTESTED
# TODO: update docs
def change_username(params, _id, conn, logger, config, session):
    try:
        # CHECK: is the username valid?
        length = len(params["new_username"])
        if length < lconst.MIN_USERNAME_LEN or length > lconst.MAX_USERNAME_LEN:
            return rpc.make_error_resp(const.INVALID_USER_USERNAME_CODE, const.INVALID_USER_USERNAME, _id)
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
            # CHECK: is the username available?
            if len(conn.execute("""SELECT * FROM users WHERE username = ?""", (params["new_username"],)).fetchall()) != 0:
                return rpc.make_error_resp(0,
                                           "PROBLEM: The requested username is taken.\n"
                                           "SUGGESTION: Try again with a different username.",
                                           _id)
            # NOTE: load the caller's user
            caller = db.load_user_w_user_id(conn, user_id, _id)
            # NOTE: update the caller's username
            caller.username = params["new_username"]
            # NOTE: recalculate the caller's user_id
            caller.recalculate_user_id()
            # NOTE: save the caller
            db.save_existing_user(conn, caller, _id)
            # NOTE: update the user_id in the session
            session["user_id"] = caller.user_id
        return rpc.make_success_resp(caller.one_hot_encode(), _id)
    except WrappedErrorResponse as e:
        file_logger.log_error({
            "method": "change_username" + str(e.methods),
            "params": params,
            "error": str(e.exception)
        })
        return e.response_obj
    except Exception as e:
        file_logger.log_error({
            "method": "change_username",
            "params": params,
            "error": str(e)
        })
        return rpc.make_error_resp(const.INTERNAL_ERROR_CODE, const.INTERNAL_ERROR, _id)


# UNTESTED
# UNDOCUMENTED
def change_password_hash(params, _id, conn, logger, config, session):
    try:
        # CHECK: is the password_hash valid?
        length = len(params["new_password_hash"])
        if length < lconst.MIN_PASSWORD_HASH_LEN or length > lconst.MAX_PASSWORD_HASH_LEN:
            return rpc.make_error_resp(const.INVALID_USER_PASSWORD_HASH_CODE, const.INVALID_USER_PASSWORD_HASH, _id)
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
            # NOTE: load the caller's user
            caller = db.load_user_w_user_id(conn, user_id, _id)
            # NOTE: update the caller's username
            caller.password_hash = params["new_password_hash"]
            # NOTE: recalculate the caller's user_id
            caller.recalculate_user_id()
            # NOTE: save the caller
            db.save_existing_user(conn, caller, _id)
            # NOTE: update the user_id in the session
            session["user_id"] = caller.user_id
        return rpc.make_success_resp(caller.one_hot_encode(), _id)
    except WrappedErrorResponse as e:
        file_logger.log_error({
            "method": "change_password_hash" + str(e.methods),
            "params": params,
            "error": str(e.exception)
        })
        return e.response_obj
    except Exception as e:
        file_logger.log_error({
            "method": "change_password_hash",
            "params": params,
            "error": str(e)
        })
        return rpc.make_error_resp(const.INTERNAL_ERROR_CODE, const.INTERNAL_ERROR, _id)