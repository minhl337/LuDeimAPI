from uuid import uuid4


from classes.ClassAbstrSerializable import AbstrSerializable
from classes.ClassAbstrChangeTracked import AbstrChangeTracked


class Item(AbstrSerializable, AbstrChangeTracked):
    def __init__(self,
                 uuid=None,
                 _type=None,
                 location_uuids=(),
                 user_uuids=()):
        AbstrChangeTracked.__init__(self)
        if uuid is None:
            uuid = uuid4().hex
        self.uuid = uuid
        if _type is None:
            raise Exception("`type` can't be None.")
        self.type = _type
        self.location_uuids = location_uuids
        self.user_uuids = user_uuids
