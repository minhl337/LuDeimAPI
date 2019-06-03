import json
import zlib


class AbstrSerializable:
    def one_hot_encode(self):
        return json.dumps(self.__dict__)

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
