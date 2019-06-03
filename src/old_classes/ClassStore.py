from old_classes.abstracts.ClassAbstrSupplyChainMember import AbstrSupplyChainMember


class Store(AbstrSupplyChainMember):
    def __init__(self,
                 name,
                 address=None,
                 uuid=None,
                 picture=None,
                 incoming=(),
                 outgoing=(),
                 inventory=(),
                 users=()):
        AbstrSupplyChainMember.__init__(self,
                                        name=name,
                                        address=address,
                                        uuid=uuid,
                                        picture=picture,
                                        incoming=incoming,
                                        outgoing=outgoing,
                                        inventory=inventory,
                                        users=users)
