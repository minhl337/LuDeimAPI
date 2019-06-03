from old_classes.abstracts.ClassAbstrAdmin import AbstrAdmin


class ManagerAdmin(AbstrAdmin):
    def __init__(self,
                 username,
                 password_hash,
                 avatar=None,
                 users=()):
        AbstrAdmin.__init__(self,
                            username=username,
                            password_hash=password_hash,
                            avatar=avatar,
                            users=users)
