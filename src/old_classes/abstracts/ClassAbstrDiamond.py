from old_classes.abstracts.Generics.ClassAbstrGenericJemstone import AbstrGenericJemstone
from old_classes.abstracts.Features.ClassAbstr5Cs import Abstr5C


class AbstrDiamond(AbstrGenericJemstone, Abstr5C):
    def __init__(self,
                 uuid,
                 dob,
                 mine,
                 gem_id,
                 raw_id,
                 mining_company,
                 location,
                 in_transit_to=None,
                 usd_value=None,
                 zar_value=None,
                 distributor=None,
                 cutter=None,
                 jeweler=None,
                 store=None,
                 tender_house=None,
                 tender_date=None,
                 customer=None,
                 carat=None,
                 color=None,
                 cut=None,
                 clarity=None,
                 chronicle=None):
        AbstrGenericJemstone.__init__(self,
                                      uuid=uuid,
                                      dob=dob,
                                      mine=mine,
                                      gem_id=gem_id,
                                      raw_id=raw_id,
                                      mining_company=mining_company,
                                      usd_value=usd_value,
                                      zar_value=zar_value,
                                      distributor=distributor,
                                      cutter=cutter,
                                      jeweler=jeweler,
                                      store=store,
                                      tender_house=tender_house,
                                      tender_date=tender_date,
                                      customer=customer,
                                      location=location,
                                      in_transit_to=in_transit_to)
        Abstr5C.__init__(self,
                         carat=carat,
                         color=color,
                         cut=cut,
                         clarity=clarity,
                         chronicle=chronicle)

    def log_cutting(self, cutter, cutter_invoice, cut):
        self.cutter = cutter
        self.cutter_invoice = cutter_invoice
        self.cut = cut
