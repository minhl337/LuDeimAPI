import utils.response_constants as const
import utils.jsonrpc2 as rpc
import utils.logging as file_logger
from classes.ClassWrappedErrorResponse import WrappedErrorResponse
import utils.ludeim_generic_helpers as ludeim
import utils.database_helpers as db
import apihandler


def get_sess(params, _id, conn, logger, config, session):
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
        # NOTE: dictize session for response
        return rpc.make_success_resp(apihandler.dictize_session(session), _id)
    except WrappedErrorResponse as e:
        file_logger.log_error({
            "method": "get_sess" + str(e.methods),
            "params": params,
            "error": str(e.exception)
        })
        return e.response_obj
    except Exception as e:
        file_logger.log_error({
            "method": "get_sess",
            "params": params,
            "error": str(e)
        })
        return rpc.make_error_resp(const.INTERNAL_ERROR_CODE, const.INTERNAL_ERROR, _id)


def put_sess(params, _id, conn, logger, config, session):
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
        # NOTE: update the session
        session[params["key"]] = params["value"]
        # NOTE: dictize session for response
        return rpc.make_success_resp(apihandler.dictize_session(session), _id)
    except WrappedErrorResponse as e:
        file_logger.log_error({
            "method": "put_sess" + str(e.methods),
            "params": params,
            "error": str(e.exception)
        })
        return e.response_obj
    except Exception as e:
        file_logger.log_error({
            "method": "put_sess",
            "params": params,
            "error": str(e)
        })
        return rpc.make_error_resp(const.INTERNAL_ERROR_CODE, const.INTERNAL_ERROR, _id)


def login(params, _id, conn, logger, config, session):
    try:
        # NOTE: calculate user_id
        user_id = params.get("user_id", ludeim.generate_user_user_id(params["username"], params["password_hash"]))
        with conn:
            # NOTE: get a lock on the database
            conn.execute("BEGIN EXCLUSIVE")
            # NOTE: get the user's type
            user = db.load_user_w_user_id(conn, user_id, _id)
        # NOTE: add the user's user_id to the session
        session["user_id"] = user.user_id
        # NOTE: add the user's type to the session
        session["type"] = user.type
        return rpc.make_success_resp(user.one_hot_encode(), _id)
    except WrappedErrorResponse as e:
        file_logger.log_error({
            "method": "login" + str(e.methods),
            "params": params,
            "error": str(e.exception)
        })
        return e.response_obj
    except Exception as e:
        file_logger.log_error({
            "method": "login",
            "params": params,
            "error": str(e)
        })
        return rpc.make_error_resp(const.INTERNAL_ERROR_CODE, const.INTERNAL_ERROR, _id)


def logout(params, _id, conn, logger, config, session):
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
        # NOTE: remove user_id from session
        session.pop("user_id", None)
        # NOTE: remove user_id from session
        session.pop("type", None)
        # NOTE: dictize the session to return
        return rpc.make_success_resp(apihandler.dictize_session(session), _id)
    except WrappedErrorResponse as e:
        file_logger.log_error({
            "method": "logout" + str(e.methods),
            "params": params,
            "error": str(e.exception)
        })
        return e.response_obj
    except Exception as e:
        file_logger.log_error({
            "method": "logout",
            "params": params,
            "error": str(e)
        })
        return rpc.make_error_resp(const.INTERNAL_ERROR_CODE, const.INTERNAL_ERROR, _id)