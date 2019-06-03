from old_classes.abstracts.Generics.ClassAbstrGenericItem import AbstrGenericItem


class AbstrGenericJemstone(AbstrGenericItem):
    def __init__(self,
                 uuid,
                 dob,
                 mine,
                 gem_id,
                 raw_id,
                 mining_company,
                 location,
                 in_transit_to=None,  # TODO : should jem stones be forced to originate from a mine?
                 usd_value=None,
                 zar_value=None,
                 distributor=None,
                 cutter=None,
                 cutter_invoice=None,
                 jeweler=None,
                 store=None,
                 tender_house=None,
                 tender_date=None,
                 customer=None):
        AbstrGenericItem.__init__(self,
                                  uuid=uuid,
                                  dob=dob,
                                  usd_value=usd_value,
                                  zar_value=zar_value,
                                  location=location,
                                  in_transit_to=in_transit_to)
        self.gem_id = gem_id
        self.raw_id = raw_id
        self.mine = mine
        self.mining_company = mining_company
        self.distributor = distributor
        self.cutter = cutter
        self.cutter_invoice = cutter_invoice
        self.jeweler = jeweler
        self.store = store
        self.tender_house = tender_house
        self.tender_date = tender_date
        self.customer = customer

    def log_cutting(self, cutter, cutter_invoice):
        self.cutter = cutter
        self.cutter_invoice = cutter_invoice
