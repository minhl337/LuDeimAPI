from classes.ClassAbstrSerializable import AbstrSerializable
from classes.ClassAbstrChangeTracked import AbstrChangeTracked
from old_classes.abstracts.ClassAbstrSupplyChainMember import AbstrSupplyChainMember


class AbstrGenericItem(AbstrSerializable, AbstrChangeTracked):
    def __init__(self,
                 uuid,
                 dob,
                 location: AbstrSupplyChainMember,
                 in_transit_to=None,
                 usd_value=None,
                 zar_value=None):
        AbstrChangeTracked.__init__(self)
        self.location = location
        self.in_transit_to = in_transit_to
        self.uuid = uuid
        self.dob = dob
        self.usd_value = usd_value
        self.zar_value = zar_value

    def revalue_in_usd(self, new_usd_value, zar_per_usd=None):
        self.usd_value = new_usd_value
        if zar_per_usd is not None:
            self.zar_value = new_usd_value * zar_per_usd

    def revalue_in_zar(self, new_zar_value, usd_per_zar=None):
        self.zar_value = new_zar_value
        if usd_per_zar is not None:
            self.usd_value = new_zar_value * usd_per_zar

    def start_transfer(self, destination: AbstrSupplyChainMember):
        assert self.location is not None
        self.location.inventory = filter(lambda x: x != self, self.location.inventory)
        self.location.outgoing = self
        destination.incoming = self
        self.in_transit_to = destination

    def receive_transfer(self):
        assert self.in_transit_to is not None
        self.location.outgoing = filter(lambda x: x != self, self.location.outgoing)
        self.location = self.in_transit_to
        self.location.inventory += self
        self.location.incoming = filter(lambda x: x != self, self.location.incoming)
        self.in_transit_to = None
