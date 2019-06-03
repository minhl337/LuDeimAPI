from old_classes.abstracts.ClassAbstrSupplyChainMember import AbstrSupplyChainMember
from old_classes.ClassMiningCompany import MiningCompany


class Mine(AbstrSupplyChainMember):
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

    def add_mining_company(self, user_to_add: MiningCompany):
        self.users += user_to_add

    def remove_mining_company(self, user_to_remove: MiningCompany):
        self.users = filter(lambda x: x != user_to_remove, self.users)
