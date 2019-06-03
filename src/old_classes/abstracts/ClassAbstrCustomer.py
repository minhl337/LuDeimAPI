from classes.ClassAbstrSerializable import AbstrSerializable


class AbstrCustomer(AbstrSerializable):
    def __init__(self,
                 title,
                 first_name,
                 last_name,
                 email=None,
                 address=None,
                 stores=()):
        self.title = title
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.address = address
        self.stores = stores
