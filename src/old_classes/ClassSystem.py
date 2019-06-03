import time


from classes.ClassAbstrSerializable import AbstrSerializable
from classes.ClassAbstrChangeTracked import AbstrChangeTracked
from old_classes.abstracts.ClassAbstrUser import AbstrUser
from old_classes.abstracts.ClassAbstrSupplyChainMember import AbstrSupplyChainMember
from old_classes.ClassMiningCompany import MiningCompany
from old_classes.ClassMine import Mine
from old_classes.ClassDistributor import Distributor
from old_classes.ClassWarehouse import Warehouse
from old_classes.ClassJeweler import Jeweler
from old_classes.ClassStore import Store
from old_classes.ClassManagerAdmin import ManagerAdmin


class System(AbstrSerializable, AbstrChangeTracked):
    def __init__(self,
                 admins=(),
                 users=(),
                 customers=(),
                 supply_chain_members=(),
                 cutters=(),
                 items=(),
                 places=()):
        AbstrChangeTracked.__init__(self)
        self.admins = admins
        self.users = users
        self.customers = customers
        self.supply_chain_members = supply_chain_members
        self.cutters = cutters
        self.items = items
        self.places = places

    # ------------

    def __add_user(self, new_user: AbstrUser):
        self.users += new_user

    def add_mining_company(self, username, password_hash, avatar=None):
        new_mining_co = MiningCompany(name=username,
                                      password_hash=password_hash,
                                      avatar=avatar,
                                      group_name="mining_company")
        self.__add_user(new_mining_co)

    def add_distributor(self, username, password_hash, avatar=None):
        new_distributor = Distributor(name=username,
                                      password_hash=password_hash,
                                      avatar=avatar,
                                      group_name="distributor")
        self.__add_user(new_distributor)

    def add_jeweler(self, username, password_hash, avatar=None):
        new_jeweler = Jeweler(name=username,
                              password_hash=password_hash,
                              avatar=avatar,
                              group_name="jeweler")
        self.__add_user(new_jeweler)

    # ------------

    def __add_admin(self, new_admin):
        self.admins += new_admin

    def add_manager_admin(self,
                          username,
                          password_hash,
                          avatar=None,
                          users=()):
        new_manager = ManagerAdmin(username=username,
                                   password_hash=password_hash,
                                   avatar=avatar,
                                   users=users)
        self.__add_admin(new_manager)

    # ------------

    # TODO
    def add_customer(self):
        pass

    # ------------

    def __add_supply_chain_member(self, new_supply_chain_member: AbstrSupplyChainMember):
        self.supply_chain_members += new_supply_chain_member

    def add_mine(self,
                 owner: MiningCompany,
                 mine_name,
                 mine_address,
                 picture=None,
                 incoming=(),
                 outgoing=(),
                 inventory=()):
        new_mine = Mine(name=mine_name,
                        address=mine_address,
                        uuid=int(time.time()),
                        picture=picture,
                        incoming=incoming,
                        outgoing=outgoing,
                        inventory=inventory,
                        users=(owner,))
        self.__add_supply_chain_member(new_mine)
        owner.add_supply_chain_member(new_mine)

    def add_warehouse(self,
                      owner: Distributor,
                      warehouse_name,
                      warehouse_address,
                      picture=None,
                      incoming=(),
                      outgoing=(),
                      inventory=()):
        new_warehouse = Warehouse(name=warehouse_name,
                                  address=warehouse_address,
                                  uuid=int(time.time()),
                                  picture=picture,
                                  incoming=incoming,
                                  outgoing=outgoing,
                                  inventory=inventory,
                                  users=(owner,))
        self.__add_supply_chain_member(new_warehouse)
        owner.add_supply_chain_member(new_warehouse)

    def add_store(self,
                  owner: Jeweler,
                  store_name,
                  store_address,
                  picture=None,
                  incoming=(),
                  outgoing=(),
                  inventory=()):
        new_store = Store(name=store_name,
                          address=store_address,
                          uuid=int(time.time()),
                          picture=picture,
                          incoming=incoming,
                          outgoing=outgoing,
                          inventory=inventory,
                          users=(owner,))
        self.__add_supply_chain_member(new_store)
        owner.add_supply_chain_member(new_store)
