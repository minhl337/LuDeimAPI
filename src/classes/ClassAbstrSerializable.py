import json
import zlib


class SetSafeJSON(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, set):
            return list(o)
        return json.JSONEncoder.default(self, o)


class AbstrSerializable:
    def one_hot_encode(self):
        return json.dumps(self.__dict__, cls=SetSafeJSON)

    def compressed_encode(self):
        return zlib.compress(self.one_hot_encode().encode("utf-8"))

    def line_encode(self):
        return tuple(self.__dict__.values())

    # TODO
    @staticmethod
    def load_from_one_hot(obj): pass

    # TODO
    @staticmethod
    def load_from_compressed(obj): pass

    # TODO
    @staticmethod
    def load_from_line(obj): pass
