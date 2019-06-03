from classes.ClassAbstrSerializable import AbstrSerializable


import json
import zlib


class Diamond(AbstrSerializable):

    def __init__(self, gem_id, dob, mine_name, dist_name, gia, tender_price, mine_pic, polisher_pic, cut, color,
                 clarity, carat, cutter_name, cutter_invoice: AbstrSerializable, polisher_name, polisher_invoice: AbstrSerializable):
        AbstrSerializable.__init__(self)
        self.gem_id = gem_id
        self.dob = dob
        self.mine_name = mine_name
        self.dist_name = dist_name
        self.gia = gia
        self.tender_price = tender_price
        self.mine_pic = mine_pic
        self.polisher_pic = polisher_pic
        self.cut = cut
        self.color = color
        self.clarity = clarity
        self.carat = carat
        self.cutter_name = cutter_name
        self.cutter_invoice = cutter_invoice
        self.polisher_name = polisher_name
        self.polisher_invoice = polisher_invoice

    # serialization

    def one_hot_encode(self):
        obj = {
            "gem_id": self.gem_id,
            "dob": self.dob,
            "mine_name": self.mine_name,
            "dist_name": self.dist_name,
            "gia": self.gia,
            "tender_price": self.tender_price,
            "mine_pic": self.mine_pic,
            "polisher_pic": self.polisher_pic,
            "cut": self.cut,
            "color": self.color,
            "clarity": self.clarity,
            "carat": self.carat,
            "cutter_name": self.cutter_name,
            "cutter_invoice": self.cutter_invoice.one_hot_encode(),
            "polisher_name": self.polisher_name,
            "polisher_invoice": self.polisher_invoice.one_hot_encode()
        }
        return json.dumps(obj)

    def compressed_encode(self):
        return zlib.compress(self.one_hot_encode().encode("utf-8"))

    def line_encode(self):
        return (
            self.gem_id,
            self.dob,
            self.mine_name,
            self.dist_name,
            self.gia,
            self.tender_price,
            self.mine_pic,
            self.polisher_pic,
            self.cut,
            self.color,
            self.clarity,
            self.carat,
            self.cutter_name,
            self.cutter_invoice.one_hot_encode(),
            self.polisher_name,
            self.polisher_invoice.one_hot_encode()
        )

    # deserialization

    @staticmethod
    def load_from_one_hot(obj):
        return Diamond(
            gem_id=obj["gem_id"],
            dob=obj["dob"],
            mine_name=obj["mine_name"],
            dist_name=obj["dist_name"],
            gia=obj["gia"],
            tender_price=obj["tender_price"],
            mine_pic=obj["mine_pic"],
            polisher_pic=obj["polisher_pic"],
            cut=obj["cut"],
            color=obj["color"],
            clarity=obj["clarity"],
            carat=obj["carat"],
            cutter_name=obj["cutter_name"],
            cutter_invoice=AbstrSerializable.load_from_one_hot(obj["cutter_invoice"]),
            polisher_name=obj["polisher_name"],
            polisher_invoice=AbstrSerializable.load_from_one_hot(obj["polisher_invoice"])
        )

    # TODO
    @staticmethod
    def load_from_compressed(obj):
        pass

    # TODO
    @staticmethod
    def load_from_line(obj):
        pass
