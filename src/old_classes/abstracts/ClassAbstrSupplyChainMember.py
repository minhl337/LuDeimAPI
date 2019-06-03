from old_classes.abstracts.Generics.ClassAbstrGenericPlace import AbstrGenericPlace


class AbstrSupplyChainMember(AbstrGenericPlace):
    def __init__(self,
                 name,
                 address=None,
                 uuid=None,
                 picture=None,
                 incoming=(),
                 outgoing=(),
                 inventory=(),
                 users=()):
        AbstrGenericPlace.__init__(self,
                                   name=name,
                                   address=address,
                                   uuid=uuid,
                                   picture=picture)
        self.incoming = incoming
        self.outgoing = outgoing
        self.inventory = inventory
        self.users = users
