import sqlite3
import json
import hashlib
import os
from uuid import uuid4


def wipe_db():
    # reset file
    config = json.load(open("config.json", "r"))
    try:
        os.remove(config["database_path"])
    except:
        pass


def build_db():
    config = json.load(open("config.json", "r"))
    conn = sqlite3.connect(config["database_path"])
    c = conn.cursor()

    # make tables
    c.execute("""CREATE TABLE users (
        uuid text,
        type text,
        username text,
        password_hash text,
        avatar text,
        location_uuids text,
        item_uuids text
    )""")
    c.execute("""CREATE TABLE locations (
        uuid text,
        type text,
        user_uuids text,
        item_uuids text,
        name text,
        address text,
        latitude real,
        longitude real,
        details text,
        photo text,
        representative text
    )""")
    c.execute("""CREATE TABLE items (
        uuid text,
        type text,
        location_uuids text,
        user_uuids text
    )""")
    conn.commit()
    conn.close()


def auto_reset():
    wipe_db()
    build_db()


def reset():
    config = json.load(open("config.json", "r"))
    auto_reset()
    conn = sqlite3.connect(config["database_path"])
    c = conn.cursor()

    # users table initialization
    while "break" != input("type 'break' to stop entering new test users. Type anything else to continue: "):
        test_type = input("what type of user would you like to create (mining_co, distributor, jeweler)?\n")
        test_username = input("test user's username?\n")
        test_password = input("test user's password?\n")
        test_avatar = "https://picsum.photos/400"
        test_location_uuids = json.dumps(())
        test_items_uuids = json.dumps(())
        test_pass_hash = hashlib.sha256(test_password.encode("utf-8")).hexdigest()
        test_user_id = hashlib.sha256((test_username + test_pass_hash).encode("utf-8")).hexdigest()
        c.execute("""INSERT INTO users VALUES (?, ?, ?, ?, ?, ?)""",
                  (test_user_id, test_type, test_username, test_pass_hash, test_avatar, test_location_uuids,
                   test_items_uuids))
        print("your test user was successfully added to the database. Here's its info:")
        print("uuid: {}".format(test_user_id))
        print("type: {}".format(test_type))
        print("username: {}".format(test_username))
        print("password: {}".format(test_password))
        print("pass_hash: {}".format(test_pass_hash))
        print("avatar: {}".format(test_avatar))
        print("location_uuids: {}".format(test_location_uuids))

    # locations table initialization
    while "break" != input("type 'break' to stop entering new test locations. Type anything else to continue: "):
        test_uuid = uuid4().hex
        test_type = input("what type of location would you like to create (mine, warehouse, store)?\n")
        test_user_uuids = json.dumps(())
        test_items_uuids = json.dumps(())
        test_name = input("what's the name of this location?\n")
        test_address = input("what's the address of this location?\n")
        test_latitude = float(input("what's the latitude of this location?\n"))
        test_longitude = float(input("what's the longitude of this location?\n"))
        test_details = input("want to include any details? if so, type them here:\n")
        test_photo = "https://picsum.photos/400"
        test_representative_title = input("what's the title of the representative of this location (mr, miss, mrs, etc)?\n")
        test_representative_first_name = input("what's the first name of the representative of this location?\n")
        test_representative_last_name = input("what's the last name of the representative of this location?\n")
        test_representative_contact_info = input("what's the contact info of the representative of this location?\n")
        test_representative = json.dumps({
            "title": test_representative_title,
            "first_name": test_representative_first_name,
            "last_name": test_representative_last_name,
            "contact_info": test_representative_contact_info
        })
        c.execute("""INSERT INTO locations VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                  (test_uuid, test_type, test_user_uuids, test_items_uuids, test_name, test_address, test_latitude,
                   test_longitude, test_details, test_photo, test_representative,))
        print("your test location was successfully added to the database. Here's its uuid:")
        print("uuid: {}".format(test_uuid))

    # items table initialization
    while "break" != input("type 'break' to stop entering new test items. Type anything else to continue: "):
        test_uuid = uuid4().hex
        test_type = input("what type of item would you like to create (diamond)?\n")
        test_user_uuids = json.dumps(())
        test_location_uuids = json.dumps(())
        c.execute("""INSERT INTO items VALUES (?, ?, ?, ?)""",
                  (test_uuid, test_type, test_user_uuids, test_location_uuids,))
        print("your test location was successfully added to the database. Here's its uuid:")
        print("uuid: {}".format(test_uuid))

    # linking users with locations
    while "break" != input("type 'break' to stop linking users and locations. Type anything else to continue: "):
        loc_uuid = input("what's the uuid of the location you'd like to link?\n")
        user_uuid = input("what's the uuid of the user you'd like to link?\n")
        c.execute("""SELECT user_uuids FROM locations WHERE uuid = ?""", (loc_uuid,))
        loc_user_uuids = tuple(json.loads(c.fetchone()[0]))
        c.execute("""SELECT location_uuids FROM users WHERE uuid = ?""", (user_uuid,))
        user_loc_uuids = tuple(json.loads(c.fetchone()[0]))
        loc_user_uuids += (user_uuid,)
        user_loc_uuids += (loc_uuid,)
        loc_user_uuids = json.dumps(loc_user_uuids)
        user_loc_uuids = json.dumps(user_loc_uuids)
        c.execute("""UPDATE locations SET user_uuids = ? WHERE uuid = ?""", (loc_user_uuids, loc_uuid,))
        c.execute("""UPDATE users SET location_uuids = ? WHERE uuid = ?""", (user_loc_uuids, user_uuid,))
        print("link successfully made!")

    # linking locations with items
    while "break" != input("type 'break' to stop linking locations and items. Type anything else to continue: "):
        item_uuid = input("what's the uuid of the item you'd like to link?\n")
        loc_uuid = input("what's the uuid of the location you'd like to link?\n")
        c.execute("""SELECT location_uuids FROM items WHERE uuid = ?""", (item_uuid,))
        item_loc_uuids = tuple(json.loads(c.fetchone()[0]))
        c.execute("""SELECT item_uuids FROM locations WHERE uuid = ?""", (loc_uuid,))
        loc_item_uuids = tuple(json.loads(c.fetchone()[0]))
        item_loc_uuids += (loc_uuid,)
        loc_item_uuids += (item_uuid,)
        item_loc_uuids = json.dumps(item_loc_uuids)
        loc_item_uuids = json.dumps(loc_item_uuids)
        c.execute("""UPDATE items SET loc_uuids = ? WHERE uuid = ?""", (item_loc_uuids, item_uuid,))
        c.execute("""UPDATE locations SET item_uuids = ? WHERE uuid = ?""", (loc_item_uuids, loc_uuid,))
        print("link successfully made!")

    # linking items with users
    while "break" != input("type 'break' to stop linking items and users. Type anything else to continue: "):
        item_uuid = input("what's the uuid of the item you'd like to link?\n")
        user_uuid = input("what's the uuid of the user you'd like to link?\n")
        c.execute("""SELECT user_uuids FROM items WHERE uuid = ?""", (item_uuid,))
        item_user_uuids = tuple(json.loads(c.fetchone()[0]))
        c.execute("""SELECT item_uuids FROM users WHERE uuid = ?""", (user_uuid,))
        user_item_uuids = tuple(json.loads(c.fetchone()[0]))
        item_user_uuids += (user_uuid,)
        user_item_uuids += (item_uuid,)
        item_user_uuids = json.dumps(item_user_uuids)
        user_item_uuids = json.dumps(user_item_uuids)
        c.execute("""UPDATE items SET user_uuids = ? WHERE uuid = ?""", (item_user_uuids, item_uuid,))
        c.execute("""UPDATE users SET location_uuids = ? WHERE uuid = ?""", (user_item_uuids, user_uuid,))
        print("link successfully made!")

    # solidify changes
    conn.commit()
    conn.close()
