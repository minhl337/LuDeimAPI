import json
import sqlite3
import utils.jsonrpc2 as rpc
import utils.response_constants as const
from classes.ClassAdmin import Admin
from classes.ClassUser import User
from classes.ClassLocation import Location
from classes.ClassItem import Item
from classes.ClassWrappedErrorResponse import WrappedErrorResponse
import sys


def get_connection():
    config = json.load(open("config.json", "r"))
    return sqlite3.connect(config["database_path"])


# # NOTE: not transaction wrapped
# def get_user_locs(c, user_id, _id):
#     try:
#         return tuple(json.loads(c.execute("""SELECT location_uuids FROM users WHERE user_id = ?""",
#                                           (user_id,)).fetchone()[0]))
#     except WrappedErrorResponse as e:
#         e.methods.append("database_helpers.get_user_locs")
#         raise e
#     except Exception as e:
#         raise WrappedErrorResponse(
#             rpc.make_error_resp(const.NONEXISTENT_USER_CODE, const.NONEXISTENT_USER, _id),
#             e,
#             "database_helpers.get_user_locs"
#         )
#
#
# # NOTE: not transaction wrapped
# def get_user_locs_w_uuid(c, uuid, _id):
#     try:
#         return json.loads(c.execute("""SELECT location_uuids FROM users WHERE uuid = ?""",
#                                           (uuid,)).fetchone()[0])
#     except WrappedErrorResponse as e:
#         e.methods.append("database_helpers.get_user_locs_w_uuid")
#         raise e
#     except Exception as e:
#         raise WrappedErrorResponse(
#             rpc.make_error_resp(const.NONEXISTENT_USER_CODE, const.NONEXISTENT_USER, _id),
#             e,
#             "database_helpers.get_user_locs_w_uuid"
#         )
#
#
# # NOTE: not transaction wrapped
# def get_user_items(c, user_id, _id):
#     try:
#         return json.loads(c.execute("""SELECT item_uuids FROM users WHERE user_id = ?""",
#                                           (user_id,)).fetchone()[0])
#     except WrappedErrorResponse as e:
#         e.methods.append("database_helpers.get_user_items")
#         raise e
#     except Exception as e:
#         raise WrappedErrorResponse(
#             rpc.make_error_resp(const.NONEXISTENT_USER_CODE, const.NONEXISTENT_USER, _id),
#             e,
#             "database_helpers.get_user_items"
#         )
#
#
# # NOTE: not transaction wrapped
# def get_user_incoming_items(c, user_id, _id):
#     try:
#         return json.loads(c.execute("""SELECT incoming_item_uuids FROM users WHERE user_id = ?""",
#                                           (user_id,)).fetchone()[0])
#     except WrappedErrorResponse as e:
#         e.methods.append("database_helpers.get_user_incoming_items")
#         raise e
#     except Exception as e:
#         raise WrappedErrorResponse(
#             rpc.make_error_resp(const.NONEXISTENT_USER_CODE, const.NONEXISTENT_USER, _id),
#             e,
#             "database_helpers.get_user_incoming_items"
#         )
#
#
# # NOTE: not transaction wrapped
# def get_user_outgoing_items(c, user_id, _id):
#     try:
#         return json.loads(c.execute("""SELECT outgoing_item_uuids FROM users WHERE user_id = ?""",
#                                           (user_id,)).fetchone()[0])
#     except WrappedErrorResponse as e:
#         e.methods.append("database_helpers.get_user_outgoing_items")
#         raise e
#     except Exception as e:
#         raise WrappedErrorResponse(
#             rpc.make_error_resp(const.NONEXISTENT_USER_CODE, const.NONEXISTENT_USER, _id),
#             e,
#             "database_helpers.get_user_outgoing_items"
#         )
#
#
# # NOTE: not transaction wrapped
# def get_user_items_w_uuid(c, uuid, _id):
#     try:
#         return tuple(json.loads(c.execute("""SELECT item_uuids FROM users WHERE uuid = ?""",
#                                           (uuid,)).fetchone()[0]))
#     except WrappedErrorResponse as e:
#         e.methods.append("database_helpers.get_user_items_w_uuid")
#         raise e
#     except Exception as e:
#         raise WrappedErrorResponse(
#             rpc.make_error_resp(const.NONEXISTENT_USER_CODE, const.NONEXISTENT_USER, _id),
#             e,
#             "database_helpers.get_user_items_w_uuid"
#         )
#
#
# # NOTE: not transaction wrapped
# def get_user_incoming_items_w_uuid(c, uuid, _id):
#     try:
#         return json.loads(c.execute("""SELECT incoming_item_uuids FROM users WHERE uuid = ?""",
#                                     (uuid,)).fetchone()[0])
#     except WrappedErrorResponse as e:
#         e.methods.append("database_helpers.get_user_incoming_items_w_uuid")
#         raise e
#     except Exception as e:
#         raise WrappedErrorResponse(
#             rpc.make_error_resp(const.NONEXISTENT_USER_CODE, const.NONEXISTENT_USER, _id),
#             e,
#             "database_helpers.get_user_incoming_items_w_uuid"
#         )
#
#
# # NOTE: not transaction wrapped
# def get_user_outgoing_items_w_uuid(c, uuid, _id):
#     try:
#         return json.loads(c.execute("""SELECT outgoing_item_uuids FROM users WHERE uuid = ?""",
#                                     (uuid,)).fetchone()[0])
#     except WrappedErrorResponse as e:
#         e.methods.append("database_helpers.get_user_outgoing_items_w_uuid")
#         raise e
#     except Exception as e:
#         raise WrappedErrorResponse(
#             rpc.make_error_resp(const.NONEXISTENT_USER_CODE, const.NONEXISTENT_USER, _id),
#             e,
#             "database_helpers.get_user_outgoing_items_w_uuid"
#         )
#
#
# # NOTE: not transaction wrapped
# def get_loc_users(c, loc_uuid, _id):
#     try:
#         return tuple(json.loads(c.execute("""SELECT user_uuids FROM locations WHERE uuid = ?""",
#                                           (loc_uuid,)).fetchone()[0]))
#     except WrappedErrorResponse as e:
#         e.methods.append("database_helpers.get_loc_users")
#         raise e
#     except Exception as e:
#         raise WrappedErrorResponse(
#             rpc.make_error_resp(const.NONEXISTENT_LOC_CODE, const.NONEXISTENT_LOC, _id),
#             e,
#             "database_helpers.get_loc_users"
#         )
#
#
# # NOTE: not transaction wrapped
# def get_loc_items(c, loc_uuid, _id):
#     try:
#         return tuple(json.loads(c.execute("""SELECT item_uuids FROM locations WHERE uuid = ?""",
#                                           (loc_uuid,)).fetchone()[0]))
#     except WrappedErrorResponse as e:
#         e.methods.append("database_helpers.get_loc_items")
#         raise e
#     except Exception as e:
#         raise WrappedErrorResponse(
#             rpc.make_error_resp(const.NONEXISTENT_LOC_CODE, const.NONEXISTENT_LOC, _id),
#             e,
#             "database_helpers.get_loc_items"
#         )
#
#
# # NOTE: not transaction wrapped
# def get_item_users(c, item_uuid, _id):
#     try:
#         return tuple(json.loads(c.execute("""SELECT user_uuids FROM items WHERE uuid = ?""",
#                                           (item_uuid,)).fetchone()[0]))
#     except WrappedErrorResponse as e:
#         e.methods.append("database_helpers.get_item_users")
#         raise e
#     except Exception as e:
#         raise WrappedErrorResponse(
#             rpc.make_error_resp(const.NONEXISTENT_ITEM_CODE, const.NONEXISTENT_ITEM, _id),
#             e,
#             "database_helpers.get_item_users"
#         )
#
#
# # NOTE: not transaction wrapped
# def get_item_locs(c, item_uuid, _id):
#     try:
#         return tuple(json.loads(c.execute("""SELECT location_uuids FROM items WHERE uuid = ?""",
#                                           (item_uuid,)).fetchone()[0]))
#     except WrappedErrorResponse as e:
#         e.methods.append("database_helpers.get_item_locs")
#         raise e
#     except Exception as e:
#         raise WrappedErrorResponse(
#             rpc.make_error_resp(const.NONEXISTENT_ITEM_CODE, const.NONEXISTENT_ITEM, _id),
#             e,
#             "database_helpers.get_item_locs"
#         )
#
#
# # NOTE: not transaction wrapped
# def save_user_locs(c, user_id, user_loc_uuids, _id):
#     try:
#         user_loc_uuids = json.dumps(user_loc_uuids)
#         c.execute("""UPDATE users SET location_uuids = ? WHERE user_id = ?""", (user_loc_uuids, user_id,))
#     except WrappedErrorResponse as e:
#         e.methods.append("database_helpers.save_user_locs")
#         raise e
#     except Exception as e:
#         raise WrappedErrorResponse(
#             rpc.make_error_resp(const.NONEXISTENT_USER_CODE, const.NONEXISTENT_USER, _id),
#             e,
#             "database_helpers.save_user_locs"
#         )
#
#
# # NOTE: not transaction wrapped
# def save_user_locs_w_uuid(c, uuid, user_loc_uuids, _id):
#     try:
#         user_loc_uuids = json.dumps(user_loc_uuids)
#         c.execute("""UPDATE users SET location_uuids = ? WHERE uuid = ?""", (user_loc_uuids, uuid,))
#     except WrappedErrorResponse as e:
#         e.methods.append("database_helpers.save_user_locs")
#         raise e
#     except Exception as e:
#         raise WrappedErrorResponse(
#             rpc.make_error_resp(const.NONEXISTENT_USER_CODE, const.NONEXISTENT_USER, _id),
#             e,
#             "database_helpers.save_user_locs"
#         )
#
#
# # NOTE: not transaction wrapped
# def save_user_items(c, user_id, user_item_uuids, _id):
#     try:
#         user_item_uuids = json.dumps(user_item_uuids)
#         c.execute("""UPDATE users SET item_uuids = ? WHERE user_id = ?""", (user_item_uuids, user_id,))
#     except WrappedErrorResponse as e:
#         e.methods.append("database_helpers.save_user_items")
#         raise e
#     except Exception as e:
#         raise WrappedErrorResponse(
#             rpc.make_error_resp(const.NONEXISTENT_USER_CODE, const.NONEXISTENT_USER, _id),
#             e,
#             "database_helpers.save_user_items"
#         )
#
#
# # NOTE: not transaction wrapped
# def save_user_items_w_uuid(c, uuid, user_item_uuids, _id):
#     try:
#         user_item_uuids = json.dumps(user_item_uuids)
#         c.execute("""UPDATE users SET item_uuids = ? WHERE uuid = ?""", (user_item_uuids, uuid,))
#     except WrappedErrorResponse as e:
#         e.methods.append("database_helpers.save_user_items_w_uuid")
#         raise e
#     except Exception as e:
#         raise WrappedErrorResponse(
#             rpc.make_error_resp(const.NONEXISTENT_USER_CODE, const.NONEXISTENT_USER, _id),
#             e,
#             "database_helpers.save_user_items_w_uuid"
#         )
#
#
# # NOTE: not transaction wrapped
# def save_loc_users(c, loc_uuid, loc_user_uuids, _id):
#     try:
#         loc_user_uuids = json.dumps(loc_user_uuids)
#         c.execute("""UPDATE locations SET user_uuids = ? WHERE uuid = ?""", (loc_user_uuids, loc_uuid,))
#     except WrappedErrorResponse as e:
#         e.methods.append("database_helpers.save_loc_users")
#         raise e
#     except Exception as e:
#         raise WrappedErrorResponse(
#             rpc.make_error_resp(const.NONEXISTENT_LOC_CODE, const.NONEXISTENT_LOC, _id),
#             e,
#             "database_helpers.save_loc_users"
#         )
#
#
# # NOTE: not transaction wrapped
# def save_loc_items(c, loc_uuid, loc_item_uuids, _id):
#     try:
#         loc_item_uuids = json.dumps(loc_item_uuids)
#         c.execute("""UPDATE locations SET item_uuids = ? WHERE uuid =?""", (loc_item_uuids, loc_uuid,))
#     except WrappedErrorResponse as e:
#         e.methods.append("database_helpers.save_loc_items")
#         raise e
#     except Exception as e:
#         raise WrappedErrorResponse(
#             rpc.make_error_resp(const.NONEXISTENT_LOC_CODE, const.NONEXISTENT_LOC, _id),
#             e,
#             "database_helpers.save_loc_items"
#         )
#
#
# # NOTE: not transaction wrapped
# def save_item_users(c, item_uuid, item_user_uuids, _id):
#     try:
#         item_user_uuids = json.dumps(item_user_uuids)
#         c.execute("""UPDATE items SET user_uuids = ?  WHERE uuid = ?""", (item_user_uuids, item_uuid,))
#     except WrappedErrorResponse as e:
#         e.methods.append("database_helpers.save_item_users")
#         raise e
#     except Exception as e:
#         raise WrappedErrorResponse(
#             rpc.make_error_resp(const.NONEXISTENT_ITEM_CODE, const.NONEXISTENT_ITEM, _id),
#             e,
#             "database_helpers.save_item_users"
#         )
#
#
# # NOTE: not transaction wrapped
# def save_item_locs(c, item_uuid, item_loc_uuids, _id):
#     try:
#         item_loc_uuids = json.dumps(item_loc_uuids)
#         c.execute("""UPDATE items SET location_uuids = ? WHERE uuid = ?""", (item_loc_uuids, item_uuid,))
#     except WrappedErrorResponse as e:
#         e.methods.append("database_helpers.save_item_locs")
#         raise e
#     except Exception as e:
#         raise WrappedErrorResponse(
#             rpc.make_error_resp(const.NONEXISTENT_ITEM_CODE, const.NONEXISTENT_ITEM, _id),
#             e,
#             "database_helpers.save_item_locs"
#         )
#
#
# # NOTE: not transaction wrapped
# def link_user_w_loc(c, user_uuid, loc_uuid, _id):
#     try:
#         loc_user_uuids = get_loc_users(c, loc_uuid, _id)
#         user_loc_uuids = get_user_locs_w_uuid(c, user_uuid, _id)
#         loc_user_uuids += (user_uuid,)
#         user_loc_uuids += (loc_uuid,)
#         save_loc_users(c, loc_uuid, loc_user_uuids, _id)
#         save_user_locs_w_uuid(c, user_uuid, user_loc_uuids, _id)
#     except WrappedErrorResponse as e:
#         e.methods.append("database_helpers.link_user_w_loc")
#         raise e
#     except Exception as e:
#         raise WrappedErrorResponse(
#             rpc.make_error_resp(const.DATABASE_FAILURE_CODE, const.DATABASE_FAILURE, _id),
#             e,
#             "database_helpers.link_user_w_loc"
#         )
#
#
# # NOTE: not transaction wrapped
# def unlink_user_w_loc(c, user_uuid, loc_uuid, _id):
#     try:
#         loc_user_uuids = get_loc_users(c, loc_uuid, _id)
#         user_loc_uuids = get_user_locs_w_uuid(c, user_uuid, _id)
#         loc_user_uuids = filter(lambda e: e != user_uuid, loc_user_uuids)
#         user_loc_uuids = filter(lambda e: e != loc_uuid, user_loc_uuids)
#         save_loc_users(c, loc_uuid, loc_user_uuids, _id)
#         save_user_locs(c, user_uuid, user_loc_uuids, _id)
#     except WrappedErrorResponse as e:
#         e.methods.append("database_helpers.unlink_user_w_loc")
#         raise e
#     except Exception as e:
#         raise WrappedErrorResponse(
#             rpc.make_error_resp(const.DATABASE_FAILURE_CODE, const.DATABASE_FAILURE, _id),
#             e,
#             "database_helpers.unlink_user_w_loc"
#         )
#
#
# # NOTE: not transaction wrapped
# def link_loc_w_item(c, loc_uuid, item_uuid, _id):
#     try:
#         loc_item_uuids = get_loc_items(c, loc_uuid, _id)
#         item_loc_uuids = get_item_locs(c, item_uuid, _id)
#         loc_item_uuids += (item_uuid,)
#         item_loc_uuids += (loc_uuid,)
#         save_loc_items(c, loc_uuid, loc_item_uuids, _id)
#         save_item_locs(c, item_uuid, item_loc_uuids, _id)
#     except WrappedErrorResponse as e:
#         e.methods.append("database_helpers.link_loc_w_item")
#         raise e
#     except Exception as e:
#         raise WrappedErrorResponse(
#             rpc.make_error_resp(const.DATABASE_FAILURE_CODE, const.DATABASE_FAILURE, _id),
#             e,
#             "database_helpers.link_loc_w_item"
#         )
#
#
# # NOTE: not transaction wrapped
# def unlink_loc_w_item(c, loc_uuid, item_uuid, _id):
#     try:
#         loc_item_uuids = get_loc_items(c, loc_uuid, _id)
#         item_loc_uuids = get_user_locs_w_uuid(c, item_uuid, _id)
#         loc_item_uuids = filter(lambda e: e != item_uuid, loc_item_uuids)
#         item_loc_uuids = filter(lambda e: e != loc_uuid, item_loc_uuids)
#         save_loc_users(c, loc_uuid, loc_item_uuids, _id)
#         save_user_locs(c, item_uuid, item_loc_uuids, _id)
#     except WrappedErrorResponse as e:
#         e.methods.append("database_helpers.unlink_loc_w_item")
#         raise e
#     except Exception as e:
#         raise WrappedErrorResponse(
#             rpc.make_error_resp(const.DATABASE_FAILURE_CODE, const.DATABASE_FAILURE, _id),
#             e,
#             "database_helpers.unlink_loc_w_item"
#         )
#
#
# # NOTE: not transaction wrapped
# def link_item_w_user(c, item_uuid, user_uuid, _id):
#     try:
#         item_user_uuids = get_item_users(c, item_uuid, _id)
#         user_item_uuids = get_user_items_w_uuid(c, user_uuid, _id)
#         item_user_uuids += (user_uuid,)
#         user_item_uuids += (item_uuid,)
#         save_item_users(c, item_uuid, item_user_uuids, _id)
#         save_user_items_w_uuid(c, user_uuid, user_item_uuids, _id)
#     except WrappedErrorResponse as e:
#         e.methods.append("database_helpers.link_loc_w_item")
#         raise e
#     except Exception as e:
#         raise WrappedErrorResponse(
#             rpc.make_error_resp(const.DATABASE_FAILURE_CODE, const.DATABASE_FAILURE, _id),
#             e,
#             "database_helpers.link_loc_w_item"
#         )
#
#
# # NOTE: not transaction wrapped
# def unlink_item_w_user(c, item_uuid, user_uuid, _id):
#     try:
#         item_user_uuids = get_item_users(c, item_uuid, _id)
#         user_item_uuids = get_user_items(c, user_uuid, _id)
#         item_user_uuids += filter(lambda e: e != user_uuid, item_user_uuids)
#         user_item_uuids += filter(lambda e: e != item_uuid, user_item_uuids)
#         save_item_users(c, item_uuid, item_user_uuids, _id)
#         save_user_items(c, user_uuid, user_item_uuids, _id)
#     except WrappedErrorResponse as e:
#         e.methods.append("database_helpers.unlink_item_w_user")
#         raise e
#     except Exception as e:
#         raise WrappedErrorResponse(
#             rpc.make_error_resp(const.DATABASE_FAILURE_CODE, const.DATABASE_FAILURE, _id),
#             e,
#             "database_helpers.unlink_item_w_user"
#         )

# NOTE: not transaction wrapped
def load_admin(c, user_id, _id):
    try:
        line = c.execute("""SELECT * FROM admins WHERE user_id = ?""", (user_id,)).fetchone()
        return User(line[0], line[1], line[2], line[3])
    except WrappedErrorResponse as e:
        e.methods.append("database_helpers.load_admin")
        raise e
    except Exception as e:
        raise WrappedErrorResponse(
            rpc.make_error_resp(const.NONEXISTENT_USER_CODE, const.NONEXISTENT_USER, _id),
            e,
            "database_helpers.load_admin"
        )


# NOTE: not transaction wrapped
def save_existing_admin(c, admin_obj: Admin, old_user_id, _id):
    try:
        c.execute("""UPDATE admins
                     SET user_id = ?, username = ?, password_hash = ?, avatar = ? 
                     WHERE user_id = ?""", (
            admin_obj.user_id,
            admin_obj.username,
            admin_obj.password_hash,
            admin_obj.avatar,
            old_user_id
        ))
    except WrappedErrorResponse as e:
        e.methods.append("database_helpers.save_existing_admin")
        raise e
    except Exception as e:
        raise WrappedErrorResponse(
            rpc.make_error_resp(const.DATABASE_FAILURE_CODE, const.DATABASE_FAILURE, _id),
            e,
            "database_helpers.save_existing_admin"
        )


# NOTE: not transaction wrapped
def save_new_admin(c, admin_obj: Admin, _id):
    try:
        c.execute("""INSERT INTO admins VALUES (?, ?, ?, ?)""", (
            admin_obj.user_id,
            admin_obj.username,
            admin_obj.password_hash,
            admin_obj.avatar
        ))
    except WrappedErrorResponse as e:
        e.methods.append("database_helpers.save_new_admin")
        raise e
    except Exception as e:
        raise WrappedErrorResponse(
            rpc.make_error_resp(const.DATABASE_FAILURE_CODE, const.DATABASE_FAILURE, _id),
            e,
            "database_helpers.save_new_admin"
        )


# NOTE: not transaction wrapped
def load_user_w_uuid(c, user_uuid, _id):
    try:
        line = c.execute("""SELECT * FROM users WHERE uuid = ?""", (user_uuid,)).fetchone()
        return User(line[0], line[1], line[2], line[3], line[4], line[5], set(json.loads(line[6])), set(json.loads(line[7])),
                    set(json.loads(line[8])), set(json.loads(line[9])))
    except WrappedErrorResponse as e:
        e.methods.append("database_helpers.load_user_w_uuid")
        raise e
    except Exception as e:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        raise WrappedErrorResponse(
            rpc.make_error_resp(const.NONEXISTENT_USER_CODE, const.NONEXISTENT_USER, _id),
            e,
            "database_helpers.load_user_w_uuid"
        )


# NOTE: not transaction wrapped
def load_user_w_user_id(c, user_id, _id):
    try:
        line = c.execute("""SELECT * FROM users WHERE user_id = ?""", (user_id,)).fetchone()

        return User(line[0], line[1], line[2], line[3], line[4], line[5], set(json.loads(line[6])), set(json.loads(line[7])),
                    set(json.loads(line[8])), set(json.loads(line[9])))
    except WrappedErrorResponse as e:
        e.methods.append("database_helpers.load_user_w_user_id")
        raise e
    except Exception as e:
        raise WrappedErrorResponse(
            rpc.make_error_resp(const.NONEXISTENT_USER_CODE, const.NONEXISTENT_USER, _id),
            e,
            "database_helpers.load_user_w_user_id"
        )


# NOTE: not transaction wrapped
def save_new_user(c, user_obj: User, _id):
    try:
        c.execute("""INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (
            user_obj.uuid,
            user_obj.user_id,
            user_obj.type,
            user_obj.username,
            user_obj.password_hash,
            user_obj.avatar,
            json.dumps(list(user_obj.location_uuids)),
            json.dumps(list(user_obj.item_uuids)),
            json.dumps(list(user_obj.incoming_item_uuids)),
            json.dumps(list(user_obj.outgoing_item_uuids))
        ))
    except WrappedErrorResponse as e:
        e.methods.append("database_helpers.save_new_user")
        raise e
    except Exception as e:
        raise WrappedErrorResponse(
            rpc.make_error_resp(const.DATABASE_FAILURE_CODE, const.DATABASE_FAILURE, _id),
            e,
            "database_helpers.save_new_user"
        )


# NOTE: not transaction wrapped
def save_existing_user(c, user_obj: User, _id):
    try:
        c.execute("""UPDATE users
                     SET uuid = ?, user_id = ?, type_ = ?, username = ?, password_hash = ?, avatar = ?, 
                     location_uuids = ?, item_uuids = ?, incoming_item_uuids = ?, outgoing_item_uuids = ?
                     WHERE uuid = ?""", (
            user_obj.uuid,
            user_obj.user_id,
            user_obj.type,
            user_obj.username,
            user_obj.password_hash,
            user_obj.avatar,
            json.dumps(list(user_obj.location_uuids)),
            json.dumps(list(user_obj.item_uuids)),
            json.dumps(list(user_obj.incoming_item_uuids)),
            json.dumps(list(user_obj.outgoing_item_uuids)),
            user_obj.uuid,
        ))
    except WrappedErrorResponse as e:
        e.methods.append("database_helpers.save_existing_user")
        raise e
    except Exception as e:
        raise WrappedErrorResponse(
            rpc.make_error_resp(const.DATABASE_FAILURE_CODE, const.DATABASE_FAILURE, _id),
            e,
            "database_helpers.save_existing_user"
        )


# NOTE: not transaction wrapped
def load_location(c, loc_uuid, _id):
    try:
        line = c.execute("""SELECT * FROM locations WHERE uuid = ?""", (loc_uuid,)).fetchone()
        return Location(line[0], line[1], set(json.loads(line[2])), set(json.loads(line[3])), set(json.loads(line[4])), set(json.loads(line[5])), line[6],
                        line[7], line[8], line[9], line[10], line[11], json.loads(line[12]))
    except WrappedErrorResponse as e:
        e.methods.append("database_helpers.load_location")
        raise e
    except Exception as e:
        raise WrappedErrorResponse(
            rpc.make_error_resp(const.NONEXISTENT_LOC_CODE, const.NONEXISTENT_LOC, _id),
            e,
            "database_helpers.load_location"
        )


# NOTE: not transaction wrapped
def save_existing_location(c, loc_obj: Location, _id):
    try:
        c.execute("""UPDATE locations
                     SET uuid = ?, type = ?, user_uuids = ?, item_uuids = ?, incoming_item_uuids = ?, 
                     outgoing_item_uuids = ?, name = ?, address = ?, latitude = ?, longitude = ?, details = ?, 
                     photo = ?, representative = ?
                     WHERE uuid = ?""", (
            loc_obj.uuid,
            loc_obj.type,
            json.dumps(list(loc_obj.user_uuids)),
            json.dumps(list(loc_obj.item_uuids)),
            json.dumps(list(loc_obj.incoming_item_uuids)),
            json.dumps(list(loc_obj.outgoing_item_uuids)),
            loc_obj.name,
            loc_obj.address,
            loc_obj.latitude,
            loc_obj.longitude,
            loc_obj.details,
            loc_obj.photo,
            json.dumps(loc_obj.representative),
            loc_obj.uuid,
        ))
    except WrappedErrorResponse as e:
        e.methods.append("database_helpers.save_existing_location")
        raise e
    except Exception as e:
        raise WrappedErrorResponse(
            rpc.make_error_resp(const.DATABASE_FAILURE_CODE, const.DATABASE_FAILURE, _id),
            e,
            "database_helpers.save_existing_location"
        )


# NOTE: not transaction wrapped
def save_new_location(c, loc_obj: Location, _id):
    try:
        c.execute("""INSERT INTO locations VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (
            loc_obj.uuid,
            loc_obj.type,
            json.dumps(list(loc_obj.user_uuids)),
            json.dumps(list(loc_obj.item_uuids)),
            json.dumps(list(loc_obj.incoming_item_uuids)),
            json.dumps(list(loc_obj.outgoing_item_uuids)),
            loc_obj.name,
            loc_obj.address,
            loc_obj.latitude,
            loc_obj.longitude,
            loc_obj.details,
            loc_obj.photo,
            json.dumps(loc_obj.representative),
        ))
    except WrappedErrorResponse as e:
        e.methods.append("database_helpers.save_new_location")
        raise e
    except Exception as e:
        raise WrappedErrorResponse(
            rpc.make_error_resp(const.DATABASE_FAILURE_CODE, const.DATABASE_FAILURE, _id),
            e,
            "database_helpers.save_new_location"
        )


# NOTE: not transaction wrapped
def load_item(c, item_uuid, _id):
    try:
        line = c.execute("""SELECT * FROM items WHERE uuid = ?""", (item_uuid,)).fetchone()
        return Item(line[0], line[1], json.loads(line[2]), json.loads(line[3]), line[4], json.loads(line[5]))
    except WrappedErrorResponse as e:
        e.methods.append("database_helpers.load_item")
        raise e
    except Exception as e:
        raise WrappedErrorResponse(
            rpc.make_error_resp(const.NONEXISTENT_USER_CODE, const.NONEXISTENT_USER, _id),
            e,
            "database_helpers.load_item"
        )


# NOTE: not transaction wrapped
def save_existing_item(c, item_obj: Item, _id):
    try:
        c.execute("""UPDATE items
                     SET uuid = ?, type_ = ?, location_uuids = ?, user_uuids = ?, status = ?, sister_items = ?
                     WHERE uuid = ?""", (
            item_obj.uuid,
            item_obj.type,
            json.dumps(item_obj.location_uuids),
            json.dumps(item_obj.user_uuids),
            item_obj.status,
            json.dumps(item_obj.sister_items),
            item_obj.uuid,
        ))
    except WrappedErrorResponse as e:
        e.methods.append("database_helpers.save_existing_item")
        raise e
    except Exception as e:
        raise WrappedErrorResponse(
            rpc.make_error_resp(const.DATABASE_FAILURE_CODE, const.DATABASE_FAILURE, _id),
            e,
            "database_helpers.save_existing_item"
        )


# NOTE: not transaction wrapped
def save_new_item(c, item_obj: Item, _id):
    try:
        c.execute("""INSERT INTO items VALUES (?, ?, ?, ?, ?, ?)""", (
            item_obj.uuid,
            item_obj.type,
            json.dumps(item_obj.location_uuids),
            json.dumps(item_obj.user_uuids),
            item_obj.status,
            json.dumps(item_obj.sister_items)
        ))
    except WrappedErrorResponse as e:
        e.methods.append("database_helpers.save_new_item")
        raise e
    except Exception as e:
        raise WrappedErrorResponse(
            rpc.make_error_resp(const.DATABASE_FAILURE_CODE, const.DATABASE_FAILURE, _id),
            e,
            "database_helpers.save_new_item"
        )