import hashlib


from classes.ClassAbstrSerializable import AbstrSerializable
from classes.ClassAbstrChangeTracked import AbstrChangeTracked


class Admin(AbstrSerializable, AbstrChangeTracked):
    def __init__(self, username, password_hash):
        AbstrChangeTracked.__init__(self)
        self.username = username
        self.password_hash = password_hash
        self.uuid = hashlib.sha256((username + password_hash).encode("utf-8")).hexdigest()
