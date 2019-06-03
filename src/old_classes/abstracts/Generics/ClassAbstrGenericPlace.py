from old_classes.abstracts.Generics.ClassAbstrGenericEntity import AbstrGenericEntity


class AbstrGenericPlace(AbstrGenericEntity):
    def __init__(self,
                 name,
                 address=None,
                 uuid=None,
                 picture=None):
        AbstrGenericEntity.__init__(self, name=name)
        self.address = address
        self.uuid = uuid
        self.picture = picture
