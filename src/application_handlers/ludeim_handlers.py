import utils.response_constants as const
import utils.jsonrpc2 as rpc
import utils.logging as file_logger
import utils.typing as t
import utils.database_helpers as db
import utils.ludeim_generic_helpers as ludeim
import utils.ludeim_constants as lconst
from classes.ClassUser import User
from classes.ClassLocation import Location
from classes.ClassWrappedErrorResponse import WrappedErrorResponse
import json
import traceback, sys


# NOTE: not transaction wrapped
def __get_user_type(_id, conn, uuid):
    try:
        user = db.load_user(conn, uuid, _id)
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
def __get_user_username(_id, conn, uuid):
    try:
        user = db.load_user(conn, uuid, _id)
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
def __get_user_password_hash(_id, conn, uuid):
    try:
        user = db.load_user(conn, uuid, _id)
        return user.password_hash
    except WrappedErrorResponse as e:
        e.methods.append("__get_user_password_hash")
        raise e
    except Exception as e:
        raise WrappedErrorResponse(
            rpc.make_error_resp(const.GET_USER_PASSWORD_HASH_UNKNOWN_CODE, const.GET_USER_PASSWORD_HASH_UNKNOWN, _id),
            e,
            "__get_user_password_hash"
        )


# NOTE: not transaction wrapped
def __get_user_avatar(_id, conn, uuid):
    try:
        user = db.load_user(conn, uuid, _id)
        return user.avatar
    except WrappedErrorResponse as e:
        e.methods.append("__get_user_avatar")
        raise e
    except Exception as e:
        raise WrappedErrorResponse(
            rpc.make_error_resp(const.GET_USER_AVATAR_UNKNOWN_CODE, const.GET_USER_AVATAR_UNKNOWN, _id),
            e,
            "__get_user_avatar"
        )


# NOTE: not transaction wrapped
def __get_user_location_uuids(_id, conn, uuid):
    try:
        return db.get_user_locs(conn, uuid)
    except WrappedErrorResponse as e:
        e.methods.append("__get_user_location_uuids")
        raise e
    except Exception as e:
        raise WrappedErrorResponse(
            rpc.make_error_resp(const.GET_USER_LOCATION_UUIDS_UNKNOWN_CODE, const.GET_USER_LOCATION_UUIDS_UNKNOWN, _id),
            e,
            "__get_user_location_uuids"
        )


# NOTE: not transaction wrapped
def __is_username_taken(_id, conn, username):
    return len(conn.execute("""SELECT * FROM users WHERE username = ?""", (username,)).fetchall()) != 0


# TODO
#  - further username validation
#  - further password hash validation
def add_user(params, _id, conn, logger, config, session):
    try:
        schemes = t.typize_config(config)
        if not t.check_params_against_scheme_set(schemes["add_user"], params):
            return rpc.make_error_resp(
                const.INVALID_PARAMS_CODE,
                const.INVALID_PARAMS,
                _id
            )
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
            if __is_username_taken(_id, conn, params["username"]):
                return rpc.make_error_resp(const.USERNAME_TAKEN_CODE, const.USERNAME_TAKEN, _id)
            db.save_new_user(conn, user)
        session["uuid"] = user.uuid
        session["type"] = user.type
        return rpc.make_success_resp({"type": user.type, "uuid": user.uuid}, _id)
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


# TODO
#  - narrow scope of valid locations for different user types
#  - validate location address
#  - validate location details (what are details even?)
#  - validate location representative
def add_location(params, _id, conn, logger, config, session):
    try:
        schemes = t.typize_config(config)
        if not t.check_params_against_scheme_set(schemes["add_location"], params):
            return rpc.make_error_resp(
                const.INVALID_PARAMS_CODE,
                const.INVALID_PARAMS,
                _id
            )
        if "uuid" in params:
            uuid = params["uuid"]
        elif "uuid" in session:
            uuid = session["uuid"]
        else:
            return rpc.make_error_resp(const.NOT_LOGGED_IN_CODE, const.NOT_LOGGED_IN, _id)
        location = Location(_type=params["type"],
                            name=params["name"],
                            address=params["address"],
                            details=params["details"],
                            latitude=params["latitude"],
                            longitude=params["longitude"],
                            representative=params["representative"])
        if location.type not in lconst.LOCATION_TYPES:
            return rpc.make_error_resp(const.INVALID_LOCATION_TYPE_CODE, const.INVALID_LOCATION_TYPE, _id)
        if location.representative["title"] not in lconst.TITLES:
            return rpc.make_error_resp(const.INVALID_REPRESENTATIVE_TITLE_CODE, const.INVALID_REPRESENTATIVE_TITLE, _id)
        with conn:
            conn.execute("BEGIN EXCLUSIVE")
            db.save_new_location(c=conn, loc_obj=location)
            db.link(c=conn, user_uuid=uuid, loc_uuid=location.uuid)
        return rpc.make_success_resp(
            True,
            _id)
    except WrappedErrorResponse as e:
        file_logger.log_error({
            "method": "add_location" + str(e.methods),
            "params": params,
            "error": str(e.exception)
        })
        return e.response_obj
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        file_logger.log_error({
            "method": "add_location",
            "params": params,
            "error": str(e),
            "trace": str(traceback.extract_tb(exc_traceback))
        })
        return rpc.make_error_resp(
            const.INTERNAL_ERROR_CODE,
            const.INTERNAL_ERROR,
            _id)


def login(params, _id, conn, logger, config, session):
    try:
        schemes = t.typize_config(config)
        if not t.check_params_against_scheme_set(schemes["login"], params):
            return rpc.make_error_resp(
                const.INVALID_PARAMS_CODE,
                const.INVALID_PARAMS,
                _id
            )
        uuid = ludeim.generate_user_uuid(username=params["username"],
                                         password_hash=params["password_hash"])
        with conn:
            conn.execute("BEGIN EXCLUSIVE")
            _type = __get_user_type(_id, conn, uuid)
        session["uuid"] = uuid
        session["type"] = _type
        return rpc.make_success_resp({"type": _type, "uuid": uuid}, _id)
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
        return rpc.make_error_resp(
            const.INTERNAL_ERROR_CODE,
            const.INTERNAL_ERROR,
            _id)


def logout(params, _id, conn, logger, config, session):
    try:
        schemes = t.typize_config(config)
        if not t.check_params_against_scheme_set(schemes["logout"], params):
            return rpc.make_error_resp(
                const.INVALID_PARAMS_CODE,
                const.INVALID_PARAMS,
                _id
            )
        session.pop("uuid")
        session.pop("type")
        return rpc.make_success_resp(True, _id)
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
        return rpc.make_error_resp(
            const.INTERNAL_ERROR_CODE,
            const.INTERNAL_ERROR,
            _id)


def get_user_location_uuids(params, _id, conn, logger, config, session):
    try:
        schemes = t.typize_config(config)
        if not t.check_params_against_scheme_set(schemes["get_user_location_uuids"], params):
            return rpc.make_error_resp(
                const.INVALID_PARAMS_CODE,
                const.INVALID_PARAMS,
                _id
            )
        with conn:
            conn.execute("BEGIN EXCLUSIVE")
            try:
                r = db.get_user_locs(conn,
                                     conn.execute("""SELECT uuid FROM users WHERE username = ?""",
                                                  (params["username"],)).fetchone()[0])
            except WrappedErrorResponse as e:
                raise e
            except Exception as e:
                rpc.make_error_resp(const.NO_CORRESPONDING_USER_CODE, const.NO_CORRESPONDING_USER, _id)
        return rpc.make_success_resp(json.loads(json.dumps(r)), _id)
    except WrappedErrorResponse as e:
        file_logger.log_error({
            "method": "get_user_location_uuids",
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
        return rpc.make_error_resp(
            const.INTERNAL_ERROR_CODE,
            const.INTERNAL_ERROR,
            _id)


def get_all_usernames(params, _id, conn, logger, config, session):
    try:
        schemes = t.typize_config(config)
        if not t.check_params_against_scheme_set(schemes["get_all_usernames"], params):
            return rpc.make_error_resp(
                const.INVALID_PARAMS_CODE,
                const.INVALID_PARAMS,
                _id
            )
        with conn:
            conn.execute("BEGIN EXCLUSIVE")
            try:
                r = conn.execute("""SELECT username FROM users""").fetchall()
            except WrappedErrorResponse as e:
                raise e
            except Exception as e:
                raise WrappedErrorResponse(
                    rpc.make_error_resp(const.NO_CORRESPONDING_USER_CODE, const.NO_CORRESPONDING_USER, _id),
                    e,
                    "database transaction")
            r = list(map(lambda x: x[0], r))
        return rpc.make_success_resp(r, _id)
    except WrappedErrorResponse as e:
        file_logger.log_error({
            "method": "get_all_usernames",
            "params": params,
            "error": str(e.exception)
        })
        return e.response_obj
    except Exception as e:
        file_logger.log_error({
            "method": "get_all_usernames",
            "params": params,
            "error": str(e)
        })
        return rpc.make_error_resp(
            const.INTERNAL_ERROR_CODE,
            const.INTERNAL_ERROR,
            _id)