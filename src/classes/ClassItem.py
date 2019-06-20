from uuid import uuid4


from classes.ClassAbstrSerializable import AbstrSerializable
from classes.ClassAbstrChangeTracked import AbstrChangeTracked
import utils.ludeim_constants as lconst


class Item(AbstrSerializable, AbstrChangeTracked):
    def __init__(self,
                 uuid=None,
                 _type=None,
                 location_uuids=None,
                 user_uuids=None,
                 status=lconst.STATIONARY,
                 sister_items=None,
                 details=None):
        AbstrChangeTracked.__init__(self)
        if uuid is None:
            uuid = uuid4().hex + uuid4().hex + uuid4().hex + uuid4().hex
        self.uuid = uuid
        if _type is None:
            raise Exception("`type` can't be None.")
        self.type = _type
        if location_uuids is None:
            location_uuids = list()
        self.location_uuids = location_uuids
        if user_uuids is None:
            user_uuids = list()
        self.user_uuids = user_uuids
        self.status = status
        if sister_items is None:
            sister_items = list()
        self.sister_items = sister_items
        if details is None:
            details = dict()
        self.details = details
