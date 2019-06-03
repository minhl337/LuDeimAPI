from old_classes.abstracts.Generics.ClassAbstrGenericType import AbstrGenericType
from old_classes.abstracts.Generics.ClassAbstrGenericEntity import AbstrGenericEntity
from old_classes.abstracts.ClassAbstrSupplyChainMember import AbstrSupplyChainMember


class AbstrUser(AbstrGenericType, AbstrGenericEntity):
    def __init__(self,
                 password_hash,
                 name,
                 avatar=None,
                 group_name=None,
                 supply_chain_members=()):
        AbstrGenericType.__init__(self,
                                  username=name,
                                  password_hash=password_hash,
                                  avatar=avatar)
        AbstrGenericEntity.__init__(self,
                                    name=name)
        self.group_name = group_name
        self.supply_chain_members = supply_chain_members

    def add_supply_chain_member(self, supply_chain_member_to_add: AbstrSupplyChainMember):
        self.supply_chain_members += supply_chain_member_to_add

    def remove_supply_chain_member(self, supply_chain_member_to_remove):
        self.supply_chain_members = filter(lambda x: x != supply_chain_member_to_remove, self.supply_chain_members)

