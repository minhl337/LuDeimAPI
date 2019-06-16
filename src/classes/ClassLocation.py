from uuid import uuid4


from classes.ClassAbstrSerializable import AbstrSerializable
from classes.ClassAbstrChangeTracked import AbstrChangeTracked
import utils.ludeim_constants as lconst


class Location(AbstrSerializable, AbstrChangeTracked):
    def __init__(self,
                 uuid=None,
                 _type=None,
                 user_uuids=(),
                 item_uuids=(),
                 name=None,
                 address=None,
                 latitude=None,
                 longitude=None,
                 details=None,
                 photo=None,
                 representative=None):
        AbstrChangeTracked.__init__(self)
        if uuid is None:
            uuid = uuid4().hex + uuid4().hex + uuid4().hex + uuid4().hex
        self.uuid = uuid
        if _type is None:
            raise Exception("`type` can't be None.")
        self.type = _type
        self.user_uuids = user_uuids
        self.item_uuids = item_uuids
        if name is None:
            raise Exception("`name` can't be None.")
        self.name = name
        if address is None:
            raise Exception("`address` can't be None.")
        self.address = address
        if latitude is None:
            raise Exception("`latitude` can't be None.")
        self.latitude = latitude
        if longitude is None:
            raise Exception("`longitude` can't be None.")
        self.longitude = longitude
        if details is None:
            details = ""
        self.details = details
        if photo is None:
            photo = lconst.DEFAULT_LOCATION_AVATAR
        self.photo = photo
        if representative is None:
            raise Exception("`representative` can't be None.")
        self.representative = representative


