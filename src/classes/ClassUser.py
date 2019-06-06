import hashlib
import utils.ludeim_constants as lconst


from classes.ClassAbstrSerializable import AbstrSerializable
from classes.ClassAbstrChangeTracked import AbstrChangeTracked


class User(AbstrSerializable, AbstrChangeTracked):
    def __init__(self,
                 uuid=None,
                 _type=None,
                 username=None,
                 password_hash=None,
                 avatar=None,
                 location_uuids=(),
                 item_uuids=()):
        AbstrChangeTracked.__init__(self)
        if _type is None:
            raise Exception("`type` can't be None.")
        self.type = _type
        if username is None:
            raise Exception("`username` can't be None.")
        self.username = username
        if password_hash is None:
            raise Exception("`password_hash` can't be None.")
        if uuid is None:
            uuid = hashlib.sha256((username + password_hash).encode("utf-8")).hexdigest()
        else:
            assert uuid == hashlib.sha256((username + password_hash).encode("utf-8")).hexdigest()
        self.uuid = uuid

        self.password_hash = password_hash
        if avatar is None:
            avatar = lconst.DEFAULT_USER_AVATAR
        self.avatar = avatar
        self.location_uuids = location_uuids
        self.item_uuids = item_uuids
