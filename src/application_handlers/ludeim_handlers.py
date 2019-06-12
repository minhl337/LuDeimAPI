import utils.response_constants as const
import utils.jsonrpc2 as rpc
import utils.logging as file_logger
import utils.typing as t
import utils.database_helpers as db
import utils.ludeim_generic_helpers as ludeim
import utils.ludeim_constants as lconst
from classes.ClassUser import User
from classes.ClassLocation import Location
from classes.ClassItem import Item
from classes.ClassWrappedErrorResponse import WrappedErrorResponse
import json
import traceback
import sys


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
def __is_username_taken(_id, conn, username):
    return len(conn.execute("""SELECT * FROM users WHERE username = ?""", (username,)).fetchall()) != 0


# TODO:
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
            db.save_new_user(conn, user, _id)
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


# TODO:
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
            db.save_new_location(c=conn, loc_obj=location, _id=_id)
            db.link_user_w_loc(c=conn, user_uuid=uuid, loc_uuid=location.uuid, _id=_id)
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


# TODO:
#  - catch invalid user uuid
#  - catch invalid location uuid
def add_item(params, _id, conn, logger, config, session):
    try:
        schemes = t.typize_config(config)
        if not t.check_params_against_scheme_set(schemes["add_item"], params):
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
        if "type" not in params:
            _type = lconst.DIAMOND
        else:
            if params["params"] not in lconst.ITEM_TYPES:
                return rpc.make_error_resp(const.INVALID_ITEM_TYPE_CODE, const.INVALID_ITEM_TYPE, _id)
            _type = params["type"]
        item = Item(_type=_type,
                    location_uuids=(),
                    user_uuids=())
        with conn:
            conn.execute("BEGIN EXCLUSIVE")
            db.save_new_item(c=conn, item_obj=item, _id=_id)
            db.link_item_w_user(c=conn, user_uuid=uuid, item_uuid=item.uuid, _id=_id)
            db.link_loc_w_item(c=conn, loc_uuid=params["location_uuid"], item_uuid=item.uuid, _id=_id)
        return rpc.make_success_resp(True, _id)
    except WrappedErrorResponse as e:
        file_logger.log_error({
            "method": "add_item" + str(e.methods),
            "params": params,
            "error": str(e.exception)
        })
        return e.response_obj
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        file_logger.log_error({
            "method": "add_item",
            "params": params,
            "error": str(e),
            "trace": str(traceback.extract_tb(exc_traceback))
        })
        return rpc.make_error_resp(
            const.INTERNAL_ERROR_CODE,
            const.INTERNAL_ERROR,
            _id)


# WARNING: session updated
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


# WARNING: session updated
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


# TODO:
#  - optimize to not get username when a uuid is given
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
                if "username" not in params:
                    if "uuid" in params:
                        username = __get_user_username(_id, conn, params["uuid"])
                    else:
                        username = __get_user_username(_id, conn, session["uuid"])
                else:
                    username = params["username"]
                r = db.get_user_locs(conn,
                                     conn.execute("""SELECT uuid FROM users WHERE username = ?""",
                                                  (username,)).fetchone()[0],
                                     _id)
            except WrappedErrorResponse as e:
                raise e
            except Exception as e:
                return rpc.make_error_resp(const.NO_CORRESPONDING_USER_CODE, const.NO_CORRESPONDING_USER, _id)
        return rpc.make_success_resp(json.loads(json.dumps(r)), _id)
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
            "method": "get_all_usernames" + str(e.methods),
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


# TODO:
#  - optimize to not get username when a uuid is given
def get_user_item_uuids(params, _id, conn, logger, config, session):
    try:
        schemes = t.typize_config(config)
        if not t.check_params_against_scheme_set(schemes["get_user_item_uuids"], params):
            return rpc.make_error_resp(
                const.INVALID_PARAMS_CODE,
                const.INVALID_PARAMS,
                _id
            )
        with conn:
            conn.execute("BEGIN EXCLUSIVE")
            try:
                if "username" not in params:
                    if "uuid" in params:
                        username = __get_user_username(_id, conn, params["uuid"])
                    else:
                        username = __get_user_username(_id, conn, session["uuid"])
                else:
                    username = params["username"]
                r = db.get_user_items(conn,
                                      conn.execute("""SELECT uuid FROM users WHERE username = ?""",
                                                   (username,)).fetchone()[0],
                                      _id)
            except WrappedErrorResponse as e:
                raise e
            except Exception as e:
                rpc.make_error_resp(const.NO_CORRESPONDING_USER_CODE, const.NO_CORRESPONDING_USER, _id)
        return rpc.make_success_resp(json.loads(json.dumps(r)), _id)
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
        return rpc.make_error_resp(
            const.INTERNAL_ERROR_CODE,
            const.INTERNAL_ERROR,
            _id)


def get_sess(params, _id, conn, logger, config, session):
    try:
        schemes = t.typize_config(config)
        if not t.check_params_against_scheme_set(schemes["get_sess"], params):
            return rpc.make_error_resp(
                const.INVALID_PARAMS_CODE,
                const.INVALID_PARAMS,
                _id
            )
        r = dict()
        for k in session:
            r[k] = session[k]
        return rpc.make_success_resp(r, _id)
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
        return rpc.make_error_resp(
            const.INTERNAL_ERROR_CODE,
            const.INTERNAL_ERROR,
            _id)


# WARNING: session updated
def put_sess(params, _id, conn, logger, config, session):
    try:
        schemes = t.typize_config(config)
        if not t.check_params_against_scheme_set(schemes["put_sess"], params):
            return rpc.make_error_resp(
                const.INVALID_PARAMS_CODE,
                const.INVALID_PARAMS,
                _id
            )
        session[params["key"]] = params["value"]
        return rpc.make_success_resp(True, _id)
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
        return rpc.make_error_resp(
            const.INTERNAL_ERROR_CODE,
            const.INTERNAL_ERROR,
            _id)


def get_location(params, _id, conn, logger, config, session):
    try:
        schemes = t.typize_config(config)
        if not t.check_params_against_scheme_set(schemes["get_location"], params):
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
        with conn:
            conn.execute("BEGIN EXCLUSIVE")
            try:
                r = db.load_location(conn, params["location_uuid"], _id)
            except WrappedErrorResponse as e:
                raise e
            except Exception as e:
                raise WrappedErrorResponse(
                    rpc.make_error_resp(const.DATABASE_FAILURE_CODE, const.DATABASE_FAILURE, _id),
                    e,
                    "database transaction")
        return rpc.make_success_resp(r.one_hot_encode(), _id)
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
        return rpc.make_error_resp(
            const.INTERNAL_ERROR_CODE,
            const.INTERNAL_ERROR,
            _id)
