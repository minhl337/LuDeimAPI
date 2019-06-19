import unittest
import reset
import random
import string
import json
import time
import utils.ludeim_constants as lconst
import utils.response_constants as rconst
import utils.ludeim_generic_helpers as ludeim
import utils.database_helpers as db
import app
import logging
import testing.utils.logging as l


endpoint = "/api/"


class TestApiMethodLogin(unittest.TestCase):
    def setUp(self):
        app.app.testing = True
        app.app.secret_key = "".join([
                    random.choice(string.ascii_letters + string.digits) for _ in range(128)
                ])
        self.app = app.app.test_client()
        logging.basicConfig(level=logging.NOTSET)
        dbg = logging.getLogger('dbg')
        dbg.setLevel(logging.DEBUG)
        self.dbg = dbg
        flask_logger = logging.getLogger('flask')
        flask_logger.setLevel(logging.CRITICAL)

    def test__login__valid__without_logout(self):
        l.log(self.dbg, "entering: test__login__valid__without_logout")
        for _ in range(10):  # NOTE: run 10 random iterations to for robustness
            l.log(self.dbg, "\tstarting round {}".format(_))
            l.log(self.dbg, "\tresetting the database")
            reset.auto_reset()  # NOTE: reset the database
            l.log(self.dbg, "\tresetting the application")
            self.setUp()  # NOTE: reset client to prevent carry over sessions
            l.log(self.dbg, "\tadding a user")
            _type = random.choice(lconst.USER_TYPES)
            username = "".join([
                random.choice(string.ascii_letters + string.digits) for _ in range(
                    random.randint(lconst.MIN_USERNAME_LEN, lconst.MAX_USERNAME_LEN)
                )
            ])
            password_hash = "".join([
                random.choice(string.ascii_letters + string.digits) for _ in range(
                    random.randint(lconst.MIN_PASSWORD_HASH_LEN, lconst.MAX_PASSWORD_HASH_LEN)
                )
            ])
            derived_user_id = ludeim.generate_user_user_id(username, password_hash)
            payload = {
                "jsonrpc": "2.0",
                "method": "add_user",
                "params": {
                    "type": _type,
                    "username": username,
                    "password_hash": password_hash
                },
                "id": 1
            }
            resp = self.app.post(endpoint, json=payload)
            expected_resp = {
                "jsonrpc": "2.0",
                "result": {
                    "type": _type,
                    "user_id": derived_user_id
                },
                "id": 1
            }
            l.log(self.dbg, "\tchecking that the user was created correctly")
            self.assertEqual(json.loads(resp.data.decode("utf-8")),
                             expected_resp,
                             "api response was incorrect")
            # TODO: implement replacement test
            # self.assertEqual(db.get_connection().execute("""SELECT * FROM users""").fetchall(),
            #                  [(derived_uuid, _type, username, password_hash, lconst.DEFAULT_USER_AVATAR, '[]', '[]')],
            #                  "database didn't update correctly")
            with self.app as c:
                with c.session_transaction() as sess:
                    self.assertEqual(sess.get("user_id", None),
                                     None,
                                     "user_id not cleared from session correctly")
                    self.assertEqual(sess.get("type", None),
                                     None,
                                     "type not cleared from session correctly")
            # NOTE: logging into the new user
            l.log(self.dbg, "\tlogging into the newly created user")
            payload = {
                "jsonrpc": "2.0",
                "method": "login",
                "params": {
                    "username": username,
                    "password_hash": password_hash
                },
                "id": 1
            }
            resp = self.app.post(endpoint, json=payload)
            l.log(self.dbg, "\tasserting that login worked correctly")
            self.assertIn("result",
                             resp.json,
                             "api response was incorrect")
            # TODO: implement replacement test
            # self.assertEqual(db.get_connection().execute("""SELECT * FROM users""").fetchall(),
            #                  [(derived_uuid, _type, username, password_hash, lconst.DEFAULT_USER_AVATAR, '[]', '[]')],
            #                  "database didn't update correctly")
            with self.app as c:
                with c.session_transaction() as sess:
                    self.assertEqual(sess["user_id"],
                                     derived_user_id,
                                     "user_id not saved in the session correctly during login")
                    self.assertEqual(sess["type"],
                                     _type,
                                     "type not saved in the session correctly during login")
            l.log(self.dbg, "\tending round {}\n".format(_))

    def test__login__valid__with_logout(self):
        l.log(self.dbg, "entering: test__login__valid__with_logout")
        for _ in range(10):  # NOTE: run 100 random iterations to for robustness
            l.log(self.dbg, "\tstarting round {}".format(_))
            l.log(self.dbg, "\tresetting the database")
            reset.auto_reset()  # NOTE: reset the database
            l.log(self.dbg, "\tresetting the application")
            self.setUp()  # NOTE: reset client to prevent carry over sessions
            l.log(self.dbg, "\tadding a user")
            _type = random.choice(lconst.USER_TYPES)
            username = "".join([
                random.choice(string.ascii_letters + string.digits) for _ in range(
                    random.randint(lconst.MIN_USERNAME_LEN, lconst.MAX_USERNAME_LEN)
                )
            ])
            password_hash = "".join([
                random.choice(string.ascii_letters + string.digits) for _ in range(
                    random.randint(lconst.MIN_PASSWORD_HASH_LEN, lconst.MAX_PASSWORD_HASH_LEN)
                )
            ])
            derived_user_id = ludeim.generate_user_user_id(username, password_hash)
            payload = {
                "jsonrpc": "2.0",
                "method": "add_user",
                "params": {
                    "type": _type,
                    "username": username,
                    "password_hash": password_hash
                },
                "id": 1
            }
            resp = self.app.post(endpoint, json=payload)
            expected_resp = {
                "jsonrpc": "2.0",
                "result": {
                    "type": _type,
                    "user_id": derived_user_id
                },
                "id": 1
            }
            l.log(self.dbg, "\tchecking that the user was created correctly")
            self.assertEqual(json.loads(resp.data.decode("utf-8")),
                             expected_resp,
                             "api response was incorrect")
            # TODO: implement replacement test
            # self.assertEqual(db.get_connection().execute("""SELECT * FROM users""").fetchall(),
            #                  [(derived_uuid, _type, username, password_hash, lconst.DEFAULT_USER_AVATAR, '[]', '[]')],
            #                  "database didn't update correctly")
            # NOTE: logging into the new user
            l.log(self.dbg, "\tlogging into the newly created user")
            payload = {
                "jsonrpc": "2.0",
                "method": "login",
                "params": {
                    "username": username,
                    "password_hash": password_hash
                },
                "id": 1
            }
            resp = self.app.post(endpoint, json=payload)
            l.log(self.dbg, "\tchecking that the login worked correctly")
            self.assertIn("result",
                          resp.json,
                          "api response was incorrect")
            # TODO: implement replacement test
            # self.assertEqual(db.get_connection().execute("""SELECT * FROM users""").fetchall(),
            #                  [(derived_uuid, _type, username, password_hash, lconst.DEFAULT_USER_AVATAR, '[]', '[]')],
            #                  "database didn't update correctly")
            with self.app as c:
                with c.session_transaction() as sess:
                    self.assertEqual(sess.get("user_id", None),
                                     derived_user_id,
                                     "user_id not saved in the session correctly during login")
                    self.assertEqual(sess.get("type", None),
                                     _type,
                                     "type not saved in the session correctly during login")
            l.log(self.dbg, "\tending round {}\n".format(_))

    def test__login__invalid__nonexistent_username(self):
        l.log(self.dbg, "entering: test__login__invalid__nonexistent_username")
        for _ in range(10):  # NOTE: run 100 random iterations to for robustness
            l.log(self.dbg, "\tstarting round {}".format(_))
            l.log(self.dbg, "\tresetting the database")
            reset.auto_reset()  # NOTE: reset the database
            l.log(self.dbg, "\tresetting the application")
            self.setUp()  # NOTE: reset client to prevent carry over sessions
            l.log(self.dbg, "\tadding a user")
            _type = random.choice(lconst.USER_TYPES)
            username = "".join([
                random.choice(string.ascii_letters + string.digits) for _ in range(
                    random.randint(lconst.MIN_USERNAME_LEN, lconst.MAX_USERNAME_LEN)
                )
            ])
            password_hash = "".join([
                random.choice(string.ascii_letters + string.digits) for _ in range(
                    random.randint(lconst.MIN_PASSWORD_HASH_LEN, lconst.MAX_PASSWORD_HASH_LEN)
                )
            ])
            derived_user_id = ludeim.generate_user_user_id(username, password_hash)
            payload = {
                "jsonrpc": "2.0",
                "method": "add_user",
                "params": {
                    "type": _type,
                    "username": username,
                    "password_hash": password_hash
                },
                "id": 1
            }
            resp = self.app.post(endpoint, json=payload)
            expected_resp = {
                "jsonrpc": "2.0",
                "result": {
                    "type": _type,
                    "user_id": derived_user_id
                },
                "id": 1
            }
            l.log(self.dbg, "\tchecking that the user was created correctly")
            self.assertEqual(json.loads(resp.data.decode("utf-8")),
                             expected_resp,
                             "api response was incorrect")
            # TODO: implement replacement test
            # self.assertEqual(db.get_connection().execute("""SELECT * FROM users""").fetchall(),
            #                  [(derived_uuid, _type, username, password_hash, lconst.DEFAULT_USER_AVATAR, '[]', '[]')],
            #                  "database didn't update correctly")
            with self.app as c:
                with c.session_transaction() as sess:
                    self.assertEqual(sess.get("user_id", None),
                                     None,
                                     "user_id not cleared from session correctly")
                    self.assertEqual(sess.get("type", None),
                                     None,
                                     "type not cleared from session correctly")
            l.log(self.dbg, "\ttrying an invalid login that should fail")
            payload = {
                "jsonrpc": "2.0",
                "method": "login",
                "params": {
                    "username": username + "_extra_letters",
                    "password_hash": password_hash
                },
                "id": 1
            }
            resp = self.app.post(endpoint, json=payload)
            l.log(self.dbg, "\tchecking that the login attempt failed")
            self.assertIn("error",
                          resp.json,
                          "api response was incorrect")
            # TODO: implement replacement test
            # self.assertEqual(db.get_connection().execute("""SELECT * FROM users""").fetchall(),
            #                  [(derived_uuid, _type, username, password_hash, lconst.DEFAULT_USER_AVATAR, '[]', '[]')],
            #                  "database updated inadvertently")
            with self.app as c:
                with c.session_transaction() as sess:
                    self.assertEqual(sess.get("user_id", None),
                                     None,
                                     "user_id saved in the session inadvertently during login")
                    self.assertEqual(sess.get("type", None),
                                     None,
                                     "type saved in the session inadvertently during login")
            l.log(self.dbg, "\tending round {}\n".format(_))

    def test__login__invalid__nonexistent_password_hash(self):
        l.log(self.dbg, "entering: test__login__invalid__nonexistent_password_hash")
        for _ in range(10):  # NOTE: run 100 random iterations to for robustness
            l.log(self.dbg, "\tstarting round {}".format(_))
            l.log(self.dbg, "\tresetting the database")
            reset.auto_reset()  # NOTE: reset the database
            l.log(self.dbg, "\tresetting the application")
            self.setUp()  # NOTE: reset client to prevent carry over sessions
            l.log(self.dbg, "\tadding a user")
            _type = random.choice(lconst.USER_TYPES)
            username = "".join([
                random.choice(string.ascii_letters + string.digits) for _ in range(
                    random.randint(lconst.MIN_USERNAME_LEN, lconst.MAX_USERNAME_LEN)
                )
            ])
            password_hash = "".join([
                random.choice(string.ascii_letters + string.digits) for _ in range(
                    random.randint(lconst.MIN_PASSWORD_HASH_LEN, lconst.MAX_PASSWORD_HASH_LEN)
                )
            ])
            derived_user_id = ludeim.generate_user_user_id(username, password_hash)
            payload = {
                "jsonrpc": "2.0",
                "method": "add_user",
                "params": {
                    "type": _type,
                    "username": username,
                    "password_hash": password_hash
                },
                "id": 1
            }
            resp = self.app.post(endpoint, json=payload)
            expected_resp = {
                "jsonrpc": "2.0",
                "result": {
                    "type": _type,
                    "user_id": derived_user_id
                },
                "id": 1
            }
            l.log(self.dbg, "\tchecking that the new user was added correctly")
            self.assertEqual(json.loads(resp.data.decode("utf-8")),
                             expected_resp,
                             "api response was incorrect")
            # TODO: implement replacement test
            # self.assertEqual(db.get_connection().execute("""SELECT * FROM users""").fetchall(),
            #                  [(derived_uuid, _type, username, password_hash, lconst.DEFAULT_USER_AVATAR, '[]', '[]')],
            #                  "database didn't update correctly")
            with self.app as c:
                with c.session_transaction() as sess:
                    self.assertEqual(sess.get("user_id", None),
                                     None,
                                     "user_id not cleared from session correctly")
                    self.assertEqual(sess.get("type", None),
                                     None,
                                     "type not cleared from session correctly")
            l.log(self.dbg, "\ttrying an invalid login attempt")
            payload = {
                "jsonrpc": "2.0",
                "method": "login",
                "params": {
                    "username": username,
                    "password_hash": password_hash + "_extra_letters"
                },
                "id": 1
            }
            resp = self.app.post(endpoint, json=payload)
            l.log(self.dbg, "\tasserting that the login failed")
            self.assertIn("error",
                          resp.json,
                          "api response was incorrect")
            # TODO: implement replacement test
            # self.assertEqual(db.get_connection().execute("""SELECT * FROM users""").fetchall(),
            #                  [(derived_uuid, _type, username, password_hash, lconst.DEFAULT_USER_AVATAR, '[]', '[]')],
            #                  "database updated inadvertently")
            with self.app as c:
                with c.session_transaction() as sess:
                    self.assertEqual(sess.get("user_id", None),
                                     None,
                                     "user_id saved in the session inadvertently during login")
                    self.assertEqual(sess.get("type", None),
                                     None,
                                     "type saved in the session inadvertently during login")
            l.log(self.dbg, "\tending round {}\n".format(_))
