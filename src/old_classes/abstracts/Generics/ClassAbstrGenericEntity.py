from classes.ClassAbstrSerializable import AbstrSerializable
from classes.ClassAbstrChangeTracked import AbstrChangeTracked


class AbstrGenericEntity(AbstrSerializable, AbstrChangeTracked):
    def __init__(self, name):
        AbstrChangeTracked.__init__(self)
        self.name = name

    def rename(self, new_name):
        self.name = new_name
