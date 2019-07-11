import utils.response_constants as const
import utils.jsonrpc2 as rpc
import utils.logging as file_logger
import utils.database_helpers as db
import utils.ludeim_constants as lconst
from classes.ClassItem import Item
from classes.ClassWrappedErrorResponse import WrappedErrorResponse


# UNTESTED
# TODO: update docs
def change_username(params, _id, conn, logger, config, session):
	try:
		# CHECK: is the username valid?
		length = len(params["new_username"])
		if length < lconst.MIN_USERNAME_LEN or length > lconst.MAX_USERNAME_LEN:
			return rpc.make_error_resp(const.INVALID_USER_USERNAME_CODE,
									   const.INVALID_USER_USERNAME, _id)
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
			if len(conn.execute("""SELECT * FROM users WHERE username = ?""",
								(params["new_username"],)).fetchall()) != 0:
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
		return rpc.make_success_resp(caller.one_hot_jsonify(), _id)
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
		return rpc.make_error_resp(const.INTERNAL_ERROR_CODE,
								   const.INTERNAL_ERROR, _id)


# UNTESTED
# UNDOCUMENTED
def change_password_hash(params, _id, conn, logger, config, session):
	try:
		# CHECK: is the password_hash valid?
		length = len(params["new_password_hash"])
		if length < lconst.MIN_PASSWORD_HASH_LEN or length > lconst.MAX_PASSWORD_HASH_LEN:
			return rpc.make_error_resp(const.INVALID_USER_PASSWORD_HASH_CODE,
									   const.INVALID_USER_PASSWORD_HASH, _id)
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
		return rpc.make_success_resp(caller.one_hot_jsonify(), _id)
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
		return rpc.make_error_resp(const.INTERNAL_ERROR_CODE,
								   const.INTERNAL_ERROR, _id)


# UNTESTED
# UNDOCUMENTED
def change_avatar(params, _id, conn, logger, config, session):
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
			# NOTE: load the caller's user
			caller = db.load_user_w_user_id(conn, user_id, _id)
			# NOTE: update the caller's username
			caller.avatar = params["new_avatar"]
			# NOTE: save the caller
			db.save_existing_user(conn, caller, _id)
		return rpc.make_success_resp(caller.one_hot_jsonify(), _id)
	except WrappedErrorResponse as e:
		file_logger.log_error({
			"method": "change_avatar" + str(e.methods),
			"params": params,
			"error": str(e.exception)
		})
		return e.response_obj
	except Exception as e:
		file_logger.log_error({
			"method": "change_avatar",
			"params": params,
			"error": str(e)
		})
		return rpc.make_error_resp(const.INTERNAL_ERROR_CODE,
								   const.INTERNAL_ERROR, _id)


# UNTESTED
# UNDOCUMENTED
def change_item_detail(params, _id, conn, logger, config, session):
	try:
		# NOTE: find user_id
		user_id = params.get("user_id", session.get("user_id", None))
		# CHECK: was a user_id found?
		if user_id is None:
			return rpc.make_error_resp(
				0,
				"PROBLEM: There was no `user_id` argument provided and no "
				"user_id could be located in the session.\n"
				"SUGGESTION: Either either try again with a `user_id` "
				"argument, call login() then try again, or use put_sess() to "
				"manually add your user_id to your session then try again.",
				_id
			)
		with conn:
			# NOTE: get a lock on the database
			conn.execute("BEGIN EXCLUSIVE")
			# NOTE: load the caller's user
			caller = db.load_user_w_user_id(conn, user_id, _id)
			# NOTE: load the item
			item = db.load_item(conn, params["item_uuid"], _id)
			# CHECK: does the caller own this item?
			if item.uuid not in caller.item_uuids | caller.outgoing_item_uuids:
				return rpc.make_error_resp(
					0,
					"PROBLEM: You don't own the item you're trying to edit.\n"
					"SUGGESTION: Try editing an edit you own or ensure you're "
					"not logged in to someone else's account.",
					_id
				)
			# CHECK: is the item stationary?
			if item.status != lconst.STATIONARY:
				return rpc.make_error_resp(
					0,
					"PROBLEM: You can't edit a non-stationary item.\n"
					"SUGGESTION: Rescind the transfer then try again.",
					_id
				)
			# NOTE: update the item's details field
			item.details[params["key"]] = params["value"]
			# NOTE: save the item
			db.save_existing_item(conn, item, _id)
		return rpc.make_success_resp(item.one_hot_jsonify(), _id)
	except WrappedErrorResponse as e:
		file_logger.log_error({
			"method": "change_item_detail" + str(e.methods),
			"params": params,
			"error": str(e.exception)
		})
		return e.response_obj
	except Exception as e:
		file_logger.log_error({
			"method": "change_item_detail",
			"params": params,
			"error": str(e)
		})
		return rpc.make_error_resp(
			const.INTERNAL_ERROR_CODE,
			const.INTERNAL_ERROR, _id
		)


# UNTESTED
# UNDOCUMENTED
def split_item(params, _id, conn, logger, config, session):
	try:
		# NOTE: find user_id
		user_id = params.get("user_id", session.get("user_id", None))
		# CHECK: was a user_id found?
		if user_id is None:
			return rpc.make_error_resp(
				0,
				"PROBLEM: There was no `user_id` argument provided and no "
				"user_id could be located in the session.\n"
				"SUGGESTION: Either either try again with a `user_id` "
				"argument, call login() then try again, or use put_sess() to "
				"manually add your user_id to your session then try again.",
				_id
			)
		with conn:
			# NOTE: get a lock on the database
			conn.execute("BEGIN EXCLUSIVE")
			# NOTE: load the caller's user
			caller = db.load_user_w_user_id(conn, user_id, _id)
			# NOTE: load the item
			item = db.load_item(conn, params["item_uuid"], _id)
			# CHECK: does the caller own this item?
			if item.uuid not in caller.item_uuids | caller.outgoing_item_uuids:
				return rpc.make_error_resp(
					0,
					"PROBLEM: You don't own the item you're trying to edit.\n"
					"SUGGESTION: Try editing an edit you own or ensure you're "
					"not logged in to someone else's account.",
					_id
				)
			# CHECK: is the item stationary?
			if item.status != lconst.STATIONARY:
				return rpc.make_error_resp(
					0,
					"PROBLEM: You can't edit a non-stationary item.\n"
					"SUGGESTION: Rescind the transfer then try again.",
					_id
				)
			# NOTE: load the item's location
			location = db.load_location(conn, item.location_uuids[-1], _id)
			# NOTE: make n new items with the parent item's
			children = {Item(
				_type=item.type,
				location_uuids=item.location_uuids,
				user_uuids=item.user_uuids,
				status=item.status,
				details=item.details
			) for _ in range(params.get("ways", 2))}
			# NOTE: generate the set of sister item uuids
			sister_uuids =\
				{child.uuid for child in children} | set(item.sister_items)
			for child in children:
				# NOTE: add the sisters to the child
				child.sister_items = list(sister_uuids - {child.uuid})
				# NOTE: save the new child
				db.save_new_item(conn, child, _id)
				# NOTE: add the child to the location's item_uuids list
				location.item_uuids.add(child.uuid)
				# NOTE: add the child to the caller's item_uuids list
				caller.item_uuids.add(child.uuid)
			# NOTE: update the item's status to `split`
			item.status = lconst.SPLIT
			# NOTE: remove the item from the location's item_uuids list
			location.item_uuids.discard(item.uuid)
			# NOTE: remove the item from the caller's item_uuids list
			caller.item_uuids.discard(item.uuid)
			# NOTE save everything
			db.save_existing_item(conn, item, _id)
			db.save_existing_location(conn, location, _id)
			db.save_existing_user(conn, caller, _id)
		children = [child.one_hot_jsonify() for child in children]
		return rpc.make_success_resp(list(children), _id)
	except WrappedErrorResponse as e:
		file_logger.log_error({
			"method": "split_item" + str(e.methods),
			"params": params,
			"error": str(e.exception)
		})
		return e.response_obj
	except Exception as e:
		file_logger.log_error({
			"method": "split_item",
			"params": params,
			"error": str(e)
		})
		return rpc.make_error_resp(
			const.INTERNAL_ERROR_CODE,
			const.INTERNAL_ERROR, _id
		)
