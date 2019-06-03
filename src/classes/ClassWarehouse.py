from uuid import uuid4


from classes.ClassAbstrSerializable import AbstrSerializable
from classes.ClassAbstrChangeTracked import AbstrChangeTracked
from classes.ClassAbstrLocation import AbstrLocation


class Warehouse(AbstrSerializable, AbstrChangeTracked, AbstrLocation):
    def __init__(self,
                 user_uuids=(),
                 name=None,
                 address=None,
                 coordinates=None,
                 details=None,
                 photo=None,
                 representative=None):  # (title, first_name, last_name, contact_info)
        AbstrChangeTracked.__init__(self)
        AbstrLocation.__init__(self,
                               name=name,
                               address=address,
                               coordinates=coordinates,
                               details=details,
                               photo=photo,
                               representative=representative)
        self.uuid = uuid4().hex
        self.user_uuids = user_uuids

    def add_user(self, user_to_add):
        if isinstance(user_to_add, str):
            self.user_uuids += user_to_add
        else:
            self.user_uuids += user_to_add.uuid

    def remove_user(self, user_to_remove):
        if isinstance(user_to_remove, str):
            self.user_uuids = filter(lambda e: e != user_to_remove, self.user_uuids)
        else:
            self.user_uuids = filter(lambda e: e != user_to_remove.uuid, self.user_uuids)
