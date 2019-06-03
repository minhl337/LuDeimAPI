from old_classes.abstracts.ClassAbstrUser import AbstrUser


class Distributor(AbstrUser):
    def __init__(self,
                 password_hash,
                 name,
                 avatar=None,
                 group_name=None,
                 supply_chain_members=()):
        AbstrUser.__init__(self,
                           password_hash=password_hash,
                           name=name,
                           avatar=avatar,
                           group_name=group_name,
                           supply_chain_members=supply_chain_members)
