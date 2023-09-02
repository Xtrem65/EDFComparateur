from priceGetter import PriceGetter
import json

class AppContext:

    def __init__(self):
        self.pricings = self.regeneratePricing()

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
    
    def regeneratePricing(self):
        priceGetter = PriceGetter()
        # This should retrieve price for TEMPO / BASE AND HCHP
        pricing = priceGetter.getPrice()
        
        #Zen is still hardcoded 
        ZenHPEco = 0.2228
        ZenHCEco = 0.1295
        ZenHPSobriete = 0.6712
        ZenHCSobriete = 0.2228
        
        pricing["ZEN"] =  {
                        "6": {
                            "Abonnement":12.62,
                            "Consommation": {"HP":{"BLEU":ZenHPEco,"BLANC":ZenHPEco,"ROUGE":ZenHPSobriete},"HC":{"BLEU":ZenHCEco,"BLANC":ZenHCEco,"ROUGE":ZenHCSobriete}}
                        },
                        "9": {
                            "Abonnement":15.99,
                            "Consommation": {"HP":{"BLEU":ZenHPEco,"BLANC":ZenHPEco,"ROUGE":ZenHPSobriete},"HC":{"BLEU":ZenHCEco,"BLANC":ZenHCEco,"ROUGE":ZenHCSobriete}}
                            },
                        "12": {
                            "Abonnement":19.27,
                            "Consommation": {"HP":{"BLEU":ZenHPEco,"BLANC":ZenHPEco,"ROUGE":ZenHPSobriete},"HC":{"BLEU":ZenHCEco,"BLANC":ZenHCEco,"ROUGE":ZenHCSobriete}}
                        }
                    }
        return pricing
    
    def getPricings(self):
        return self.pricings