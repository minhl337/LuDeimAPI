from classes.ClassAbstrSerializable import AbstrSerializable
from classes.ClassAbstrChangeTracked import AbstrChangeTracked


import hashlib


class AbstrGenericType(AbstrSerializable, AbstrChangeTracked):
    def __init__(self,
                 username=None,
                 password_hash=None,
                 avatar=None):
        AbstrChangeTracked.__init__(self)
        self.username = username
        self.password_hash = password_hash
        self.user_id = self.generate_user_id(self.username, self.password_hash)
        self.avatar = avatar

    @staticmethod
    def generate_user_id(username, password_hash):
        return hashlib.sha256((username + password_hash).encode("utf-8")).hexdigest()