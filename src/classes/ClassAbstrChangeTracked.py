import time


class AbstrChangeTracked:
    def __init__(self):
        self.edits = tuple()  # using tuples because they're immutable

    def __setattr__(self, key, value):
        if key != "edits" or self.__dict__.get("edits", None) is None:
            self.__dict__[key] = value
        if key != "edits":
            self.__dict__["edits"] += ((key, value, int(time.time())),)