from old_classes.abstracts.Generics.ClassAbstrGenericType import AbstrGenericType


class AbstrAdmin(AbstrGenericType):
    def __init__(self,
                 username,
                 password_hash,
                 avatar=None,
                 users=()):
        AbstrGenericType.__init__(self,
                                  username=username,
                                  password_hash=password_hash,
                                  avatar=avatar)
        self.users = users

    def add_user(self, user_to_add):
        self.users += user_to_add

    def remove_user(self, user_to_remove):
        self.users = filter(lambda x: x != user_to_remove, self.users)
