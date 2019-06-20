import hashlib
import utils.ludeim_constants as lconst


from classes.ClassAbstrSerializable import AbstrSerializable
from classes.ClassAbstrChangeTracked import AbstrChangeTracked
import utils.ludeim_generic_helpers as ludeim


class Admin(AbstrSerializable, AbstrChangeTracked):
    def __init__(self,
                 user_id=None,
                 username=None,
                 password_hash=None,
                 avatar=None):
        AbstrChangeTracked.__init__(self)
        if username is None:
            raise Exception("`username` can't be None.")
        self.username = username
        if password_hash is None:
            raise Exception("`password_hash` can't be None.")
        self.password_hash = password_hash
        if user_id is None:
            user_id = ludeim.generate_user_user_id(self.username, self.password_hash)
        else:
            assert user_id == hashlib.sha256((username + password_hash).encode("utf-8")).hexdigest()
        self.user_id = user_id
        if avatar is None:
            avatar = lconst.DEFAULT_USER_AVATAR
        self.avatar = avatar

    def recalculate_user_id(self):
        self.user_id = ludeim.generate_user_user_id(self.username, self.password_hash)