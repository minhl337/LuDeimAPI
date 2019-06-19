import utils.response_constants as const
import utils.jsonrpc2 as rpc
import utils.logging as file_logger
import utils.database_helpers as db
import utils.ludeim_constants as lconst
from classes.ClassWrappedErrorResponse import WrappedErrorResponse


# UNDOCUMENTED
def begin_transfer(params, _id, conn, logger, config, session):
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
                                       "your session then try again.", _id)
        with conn:
            # NOTE: get a lock on the database
            conn.execute("BEGIN EXCLUSIVE")
            # NOTE: load item
            item = db.load_item(conn, params["item_uuid"], _id)
            # CHECK: is the item not stationary?
            if item.status != lconst.STATIONARY:
                return rpc.make_error_resp(0,
                                           "PROBLEM: The item designated by the `item_uuid` argument is not in "
                                           "stationary, and therefore, it cannot be transferred.\n"
                                           "SUGGESTION: Try calling this method with an `item_uuid` that corresponds to"
                                           " an item that is stationary, call redirect_transfer() instead, or call "
                                           "rescind_transfer() on this item then try again.",
                                           _id)
            # NOTE: load the caller's user
            caller = db.load_user_w_user_id(conn, user_id, _id)
            # CHECK: does the caller own the item?
            if item.uuid not in caller.item_uuids:
                return rpc.make_error_resp(0,
                                           "PROBLEM: The item begin transferred is not owned by this account.\n"
                                           "SUGGESTION: You may be logged in to someone else's account without "
                                           "realizing it. Try calling login() then trying again.",
                                           _id)
            # NOTE: load the receiver's user
            receiver = db.load_user_w_uuid(conn, params["destination_user_uuid"], _id)
            # NOTE: load the destination
            destination = db.load_location(conn, params["destination_location_uuid"], _id)
            # CHECK: is the destination attached to the receiver?
            if destination.uuid not in receiver.location_uuids:
                return rpc.make_error_resp(0,
                                           "PROBLEM: The designated receiver has no presence at the designated "
                                           "destination which is a contradiction.\n"
                                           "SUGGESTION: Try again with either a different receiver who has a presence "
                                           "at the destination, or a different destination where the receiver has a "
                                           "presence.",
                                           _id)
            # NOTE: set the item to transit
            item.status = lconst.TRANSIT
            # NOTE: add the destination to the item's location_uuids list
            item.location_uuids.append(destination.uuid)
            # NOTE: add the receiver to the item's user_uuids list
            item.user_uuids.append(receiver.uuid)
            # NOTE: save the edited item
            db.save_existing_item(conn, item, _id)
        return rpc.make_success_resp(item.one_hot_encode(), _id)
    except WrappedErrorResponse as e:
        file_logger.log_error({
            "method": "begin_transfer" + str(e.methods),
            "params": params,
            "error": str(e.exception),
        })
        return e.response_obj
    except Exception as e:
        file_logger.log_error({
            "method": "begin_transfer",
            "params": params,
            "error": str(e),
        })
        return rpc.make_error_resp(const.INTERNAL_ERROR_CODE, const.INTERNAL_ERROR, _id)


# UNTESTED
# UNDOCUMENTED
def accept_transfer(params, _id, conn, logger, config, session):
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
                                       "your session then try again.", _id)
        with conn:
            # NOTE: get a lock on the database
            conn.execute("BEGIN EXCLUSIVE")
            # NOTE: load item
            item = db.load_item(conn, params["item_uuid"], _id)
            # CHECK: is the item actually in transit?
            if item.status != lconst.TRANSIT:
                return rpc.make_error_resp(0,
                                           "PROBLEM: The item designated by the `item_uuid` argument is not in transit,"
                                           " and therefore, there is no transfer to accept.\n"
                                           "SUGGESTION: Try calling this method with an `item_uuid` that corresponds to"
                                           " an item that is in transit.",
                                           _id)
            # NOTE: load the caller's user
            caller = db.load_user_w_user_id(conn, user_id, _id)
            # CHECK: is the caller the designated receiver of this item?
            if item.user_uuids[-1] != caller.uuid:
                return rpc.make_error_resp(0,
                                           "PROBLEM: You are not the designated receiver for this item.\n"
                                           "SUGGESTION: Many things can cause this problem. The wrong user could have "
                                           "been selected when begin_transfer() was called, you may be logged in to "
                                           "someone else's account without realizing it, or the sender could have "
                                           "called redirect_transfer() or rescind_transfer() without you realizing it.",
                                           _id)
            # NOTE: set the item to stationary
            item.status = lconst.STATIONARY
            # NOTE: add the item to the caller's item_uuids list
            caller.item_uuids.append(item.uuid)
            # NOTE: load the sender's user
            sender = db.load_user_w_user_id(conn, item.user_uuids[-2], _id)
            # NOTE: remove the item from the sender's item_uuids list
            sender.item_uuids.remove(item.uuid)
            # NOTE: save everything
            db.save_existing_user(conn, caller, _id)
            db.save_existing_user(conn, sender, _id)
            db.save_existing_item(conn, item, _id)
        return rpc.make_success_resp(item.one_hot_encode(), _id)
    except WrappedErrorResponse as e:
        file_logger.log_error({
            "method": "accept_transfer" + str(e.methods),
            "params": params,
            "error": str(e.exception)
        })
        return e.response_obj
    except Exception as e:
        file_logger.log_error({
            "method": "accept_transfer",
            "params": params,
            "error": str(e)
        })
        return rpc.make_error_resp(const.INTERNAL_ERROR_CODE, const.INTERNAL_ERROR, _id)


# UNTESTED
# UNDOCUMENTED
def rescind_transfer(params, _id, conn, logger, config, session):
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
                                       "your session then try again.", _id)
        with conn:
            # NOTE: get a lock on the database
            conn.execute("BEGIN EXCLUSIVE")
            # NOTE: load item
            item = db.load_item(conn, params["item_uuid"], _id)
            # CHECK: is the item actually in transit?
            if item.status != lconst.TRANSIT:
                return rpc.make_error_resp(0,
                                           "PROBLEM: The item designated by the `item_uuid` argument is not in transit,"
                                           " and therefore, there is no transfer to rescind.\n"
                                           "SUGGESTION: Try calling this method with an `item_uuid` that corresponds to"
                                           " an item that is in transit.",
                                           _id)
            # NOTE: load the caller's user
            caller = db.load_user_w_user_id(conn, user_id, _id)
            # CHECK: does the caller own the item?
            if item.uuid not in caller.item_uuids:
                return rpc.make_error_resp(0,
                                           "PROBLEM: You are not the owner of this item, and therefore, can't rescind "
                                           "it's transfer\n"
                                           "SUGGESTION: You may be logged in to someone else's account without "
                                           "realizing it. Try calling login() then trying again.",
                                           _id)
            # NOTE: set the item to stationary
            item.status = lconst.STATIONARY
            # NOTE: remove the receiver from the item's user_uuids list
            item.user_uuids = item.user_uuids[:-1]
            # NOTE: remove the destination from the item's location_uuids list
            item.location_uuids = item.location_uuids[:-1]
            # NOTE: save the item
            db.save_existing_item(conn, item, _id)
        return rpc.make_success_resp(item.one_hot_encode(), _id)
    except WrappedErrorResponse as e:
        file_logger.log_error({
            "method": "rescind_transfer" + str(e.methods),
            "params": params,
            "error": str(e.exception)
        })
        return e.response_obj
    except Exception as e:
        file_logger.log_error({
            "method": "rescind_transfer",
            "params": params,
            "error": str(e)
        })
        return rpc.make_error_resp(const.INTERNAL_ERROR_CODE, const.INTERNAL_ERROR, _id)


# UNTESTED
# UNDOCUMENTED
def reject_transfer(params, _id, conn, logger, config, session):
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
                                       "your session then try again.", _id)
        with conn:
            # NOTE: get a lock on the database
            conn.execute("BEGIN EXCLUSIVE")
            # NOTE: load item
            item = db.load_item(conn, params["item_uuid"], _id)
            # CHECK: is the item actually in transit?
            if item.status != lconst.TRANSIT:
                return rpc.make_error_resp(0,
                                           "PROBLEM: The item designated by the `item_uuid` argument is not in transit,"
                                           " and therefore, there is no transfer to reject.\n"
                                           "SUGGESTION: Try calling this method with an `item_uuid` that corresponds to"
                                           " an item that is in transit.",
                                           _id)
            # NOTE: load the caller's user
            caller = db.load_user_w_user_id(conn, user_id, _id)
            # CHECK: is the caller the designated receiver of this item?
            if item.uuid not in caller.item_uuids:
                return rpc.make_error_resp(0,
                                           "PROBLEM: You are not the designated receiver of this item.\n"
                                           "SUGGESTION: You may be logged in to someone else's account without "
                                           "realizing it. Try calling login() then trying again.",
                                           _id)
            # NOTE: load the sender's user
            sender = db.load_user_w_uuid(conn, item.user_uuids[-2], _id)
            # NOTE: load the origin location
            origin = db.load_location(conn, item.location_uuids[-2], _id)
            # NOTE: remove the item from the sender's item_uuids list
            sender.item_uuids.remove(item.uuid)
            # NOTE: add the item to the caller's item_uuids list
            caller.item_uuids.append(item.uuid)
            # NOTE: add the sender to the item's user_uuids list
            item.user_uuids.append(sender.uuid)
            # NOTE: add the origin to the item's location_uuids list
            # OPT: use the uuid from item.location_uuids directly
            item.location_uuids.append(origin.uuid)
            # NOTE: save everything
            db.save_existing_user(conn, sender, _id)
            db.save_existing_user(conn, caller, _id)
            db.save_existing_item(conn, item, _id)
        return rpc.make_success_resp(item.one_hot_encode(), _id)
    except WrappedErrorResponse as e:
        file_logger.log_error({
            "method": "reject_transfer" + str(e.methods),
            "params": params,
            "error": str(e.exception)
        })
        return e.response_obj
    except Exception as e:
        file_logger.log_error({
            "method": "reject_transfer",
            "params": params,
            "error": str(e)
        })
        return rpc.make_error_resp(const.INTERNAL_ERROR_CODE, const.INTERNAL_ERROR, _id)


# UNTESTED
# UNDOCUMENTED
def redirect_transfer(params, _id, conn, logger, config, session):
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
            # NOTE: load item
            item = db.load_item(conn, params["item_uuid"], _id)
            # CHECK: is the item actually in transit?
            if item.status != lconst.TRANSIT:
                return rpc.make_error_resp(0,
                                           "PROBLEM: The item designated by the `item_uuid` argument is not in transit,"
                                           " and therefore, there is no transfer to redirect.\n"
                                           "SUGGESTION: Try calling this method with an `item_uuid` that corresponds to"
                                           " an item that is in transit.",
                                           _id)
            # NOTE: load the caller's user
            caller = db.load_user_w_user_id(conn, user_id, _id)
            # CHECK: is the caller the owner of this item?
            if item.uuid not in caller.item_uuids:
                return rpc.make_error_resp(0,
                                           "PROBLEM: You are not the owner of this item, and therefore, don't have the "
                                           "ability to redirect this transfer\n"
                                           "SUGGESTION: You may be logged in to someone else's account without "
                                           "realizing it. Try calling login() then trying again.",
                                           _id)
            # NOTE: load the new receiver's user
            new_receiver = db.load_user_w_uuid(conn, params["new_destination_user_uuid"], _id)
            # NOTE: load the new destination location
            new_destination = db.load_location(conn, params["new_destination_location_uuid"], _id)
            # CHECK: is the destination attached to the receiver?
            if new_destination.uuid not in new_receiver.location_uuids:
                return rpc.make_error_resp(0,
                                           "PROBLEM: The designated new receiver has no presence at the designated "
                                           "new destination which is a contradiction.\n"
                                           "SUGGESTION: Try again with either a different new receiver who has a "
                                           "presence at the destination, or a different new destination where the "
                                           "receiver has a presence.",
                                           _id)
            # NOTE: remove the old receiver from the item's user_uuids list
            item.user_uuids = item.user_uuids[:-1]
            # NOTE: remove the old destination from the item's location_uuids list
            item.location_uuids = item.location_uuids[:-1]
            # NOTE: add the new receiver to the item's user_uuids list
            # OPT: combine with the above step
            item.user_uuids.append(new_receiver.uuid)
            # NOTE: add the new destination to the item's location_uuids list
            # OPT: combine with the above step
            item.location_uuids.append(new_destination.uuid)
            # NOTE: save the item
            db.save_existing_item(conn, item, _id)
        return rpc.make_success_resp(item.one_hot_encode(), _id)
    except WrappedErrorResponse as e:
        file_logger.log_error({
            "method": "redirect_transfer" + str(e.methods),
            "params": params,
            "error": str(e.exception)
        })
        return e.response_obj
    except Exception as e:
        file_logger.log_error({
            "method": "redirect_transfer",
            "params": params,
            "error": str(e)
        })
        return rpc.make_error_resp(const.INTERNAL_ERROR_CODE, const.INTERNAL_ERROR, _id)