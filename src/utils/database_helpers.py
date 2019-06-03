import json
import sqlite3
import utils.jsonrpc2 as rpc
import utils.response_constants as const
from classes.ClassUser import User
from classes.ClassLocation import Location
from classes.ClassWrappedErrorResponse import WrappedErrorResponse


def get_connection():
    config = json.load(open("config.json", "r"))
    return sqlite3.connect(config["database_path"])


# NOTE: not transaction wrapped
def get_user_locs(c, user_uuid):
    return tuple(json.loads(c.execute("""SELECT location_uuids FROM users WHERE uuid = ?""",
                                      (user_uuid,)).fetchone()[0]))


# NOTE: not transaction wrapped
def get_loc_users(c, loc_uuid):
    return tuple(json.loads(c.execute("""SELECT user_uuids FROM locations WHERE uuid = ?""",
                                      (loc_uuid,)).fetchone()[0]))


# NOTE: not transaction wrapped
def save_user_locs(c, user_uuid, user_loc_uuids):
    user_loc_uuids = json.dumps(user_loc_uuids)
    c.execute("""UPDATE users SET location_uuids = ? WHERE uuid = ?""", (user_loc_uuids, user_uuid,))


# NOTE: not transaction wrapped
def save_loc_users(c, loc_uuid, loc_user_uuids):
    loc_user_uuids = json.dumps(loc_user_uuids)
    c.execute("""UPDATE locations SET user_uuids = ? WHERE uuid = ?""", (loc_user_uuids, loc_uuid,))


# NOTE: not transaction wrapped
def link(c, user_uuid, loc_uuid):
    loc_user_uuids = get_loc_users(c, loc_uuid)
    user_loc_uuids = get_user_locs(c, user_uuid)
    loc_user_uuids += (user_uuid,)
    user_loc_uuids += (loc_uuid,)
    save_loc_users(c, loc_uuid, loc_user_uuids)
    save_user_locs(c, user_uuid, user_loc_uuids)


# NOTE: not transaction wrapped
def unlink(c, user_uuid, loc_uuid):
    loc_user_uuids = get_loc_users(c, loc_uuid)
    user_loc_uuids = get_user_locs(c, user_uuid)
    loc_user_uuids = filter(lambda e: e != user_uuid, loc_user_uuids)
    user_loc_uuids = filter(lambda e: e != loc_uuid, user_loc_uuids)
    save_loc_users(c, loc_uuid, loc_user_uuids)
    save_user_locs(c, user_uuid, user_loc_uuids)


# NOTE: not transaction wrapped
def load_user(c, user_uuid, _id):
    try:
        line = c.execute("""SELECT * FROM users WHERE uuid = ?""", (user_uuid,)).fetchone()
        return User(line[0], line[1], line[2], line[3], line[4], tuple(json.loads(line[5])))
    except Exception as e:
        raise WrappedErrorResponse(
            rpc.make_error_resp(const.NONEXISTENT_USER_CODE, const.NONEXISTENT_USER, _id),
            e,
            "load_user"
        )


# NOTE: not transaction wrapped
def save_new_user(c, user_obj: User):
    c.execute("""INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)""", (
        user_obj.uuid,
        user_obj.type,
        user_obj.username,
        user_obj.password_hash,
        user_obj.avatar,
        json.dumps(user_obj.location_uuids),
    ))


# NOTE: not transaction wrapped
def save_existing_user(c, user_obj: User):
    c.execute("""UPDATE users
                 SET uuid = ?, type = ?, username = ?, password_hash = ?, avatar = ?, location_uuids = ?
                 WHERE uuid = ?""", (
        user_obj.uuid,
        user_obj.type,
        user_obj.username,
        user_obj.password_hash,
        user_obj.avatar,
        json.dumps(user_obj.location_uuids),
        user_obj.uuid,
    ))


# NOTE: not transaction wrapped
def load_location(c, loc_uuid):
    c.execute("""SELECT * FROM locations WHERE uuid = ?""", (loc_uuid,))
    line = c.fetchone()
    return Location(line[0], line[1], tuple(json.loads(line[2])), line[3], line[4], line[5], line[6], line[7],
                    line[8], json.loads(line[9]))


# NOTE: not transaction wrapped
def save_existing_location(c, loc_obj: Location):
    c.execute("""UPDATE locations
                 SET uuid = ?, type = ?, user_uuids = ?, name = ?, address = ?, latitude = ?, longitude = ?,
                 details = ?, photo = ?, representative = ?
                 WHERE uuid = ?""", (
        loc_obj.uuid,
        loc_obj.type,
        json.dumps(loc_obj.user_uuids),
        loc_obj.name,
        loc_obj.address,
        loc_obj.latitude,
        loc_obj.longitude,
        loc_obj.details,
        loc_obj.photo,
        json.dumps(loc_obj.representative),
        loc_obj.uuid,
    ))


# NOTE: not transaction wrapped
def save_new_location(c, loc_obj: Location):
    c.execute("""INSERT INTO locations VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", (
        loc_obj.uuid,
        loc_obj.type,
        json.dumps(loc_obj.user_uuids),
        loc_obj.name,
        loc_obj.address,
        loc_obj.latitude,
        loc_obj.longitude,
        loc_obj.details,
        loc_obj.photo,
        json.dumps(loc_obj.representative),
    ))
