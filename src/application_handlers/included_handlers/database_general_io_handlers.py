import utils.response_constants as const
import utils.jsonrpc2 as rpc
import utils.logging as file_logger
import utils.typing as t
from application_handlers.included_handlers.users_handlers import *  # handler dependency
import hashlib

#
# handler dependencies: users_handlers.py
#


# Notice that unless I actually specify this helepr in my config.json it will be invisible to the api.
# This is useful when you want to break you code up but don't want to clutter your api.
def __helper(params, _id, conn, logger, config):
    resp = get_user_type(params, _id, conn, logger, config)
    if "result" not in resp:
        return resp
    user_type = resp["result"]["type"]
    if user_type != "database_general_io_user":
        return rpc.make_error_resp(
            const.INSUFFICIENT_PERMISSIONS_CODE,
            const.INSUFFICIENT_PERMISSIONS,
            _id
        )
    return True


# Done
#
# Only callable by database_general_io_user's
#
def backup_database(params, _id, conn, logger, config):
    try:
        schemes = t.typize_config(config)
        if not t.check_params_against_scheme_set(schemes["backup_database"], params):
            return rpc.make_error_resp(
                const.INVALID_PARAMS_CODE,
                const.INVALID_PARAMS,
                _id
            )
        resp = __helper(params, _id, conn, logger, config)
        if resp is not True:
            return resp
        with open(config["database_path"] + ".backup", "w+") as f:
            for line in conn.iterdump():
                f.write('%s\n' % line)
        file_logger.log_general({  # database backups are probably worth writing to a general log file
            "method": "backup_database",
            "params": params,
        })
        return rpc.make_success_resp({"success": True}, _id)
    except Exception as e:
        file_logger.log_error({
            "method": "backup_database",
            "params": params,
            "error": str(e)
        })
        return rpc.make_error_resp(
            const.INTERNAL_ERROR_CODE,
            const.INTERNAL_ERROR,
            _id)


# Done
#
# Only callable by database_general_io_user's
#
def get_table_names(params, _id, conn, logger, config):
    try:
        schemes = t.typize_config(config)
        if not t.check_params_against_scheme_set(schemes["get_table_names"], params):
            return rpc.make_error_resp(
                const.INVALID_PARAMS_CODE,
                const.INVALID_PARAMS,
                _id
            )
        resp = __helper(params, _id, conn, logger, config)
        if resp is not True:
            return resp
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table';")
        resp = c.fetchall()
        ret = list()
        for table_tuple in resp:
            ret.append(table_tuple[0])
        return rpc.make_success_resp(ret, _id)
    except Exception as e:
        file_logger.log_error({
            "method": "backup_database",
            "params": params,
            "error": str(e)
        })
        return rpc.make_error_resp(
            const.INTERNAL_ERROR_CODE,
            const.INTERNAL_ERROR,
            _id)