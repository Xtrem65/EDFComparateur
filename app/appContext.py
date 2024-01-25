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
        

        pricing["BaseManual2023"] =  {
                        "3": {
                            "Abonnement":9.47,
                            "Consommation": {"HP":0.2276}
                        },
                        "6": {
                            "Abonnement":12.44,
                            "Consommation": {"HP":0.2276}
                        },
                        "9": {
                            "Abonnement":15.63,
                            "Consommation": {"HP":0.2276}
                        },
                        "12": {
                            "Abonnement":18.89,
                            "Consommation": {"HP":0.2276}
                        },
                        "15": {
                            "Abonnement":21.92,
                            "Consommation": {"HP":0.2276}
                        },
                        "18": {
                            "Abonnement":24.92,
                            "Consommation": {"HP":0.2276}
                        },
                        "24": {
                            "Abonnement":31.6,
                            "Consommation": {"HP":0.2276}
                        },
                        "30": {
                            "Abonnement":37.29,
                            "Consommation": {"HP":0.2276}
                        },
                        "36": {
                            "Abonnement":44.66,
                            "Consommation": {"HP":0.2276}
                        }
        }
        pricing["BaseManual2024"] =  {
                        "3": {
                            "Abonnement":9.47,
                            "Consommation": {"HP":0.2516}
                        },
                        "6": {
                            "Abonnement":12.44,
                            "Consommation": {"HP":0.2516}
                        },
                        "9": {
                            "Abonnement":15.63,
                            "Consommation": {"HP":0.2516}
                        },
                        "12": {
                            "Abonnement":18.89,
                            "Consommation": {"HP":0.2516}
                        },
                        "15": {
                            "Abonnement":21.92,
                            "Consommation": {"HP":0.2516}
                        },
                        "18": {
                            "Abonnement":24.92,
                            "Consommation": {"HP":0.2516}
                        },
                        "24": {
                            "Abonnement":31.6,
                            "Consommation": {"HP":0.2516}
                        },
                        "30": {
                            "Abonnement":37.29,
                            "Consommation": {"HP":0.2516}
                        },
                        "36": {
                            "Abonnement":44.66,
                            "Consommation": {"HP":0.2516}
                        }
        }

        pricing["HCHPManual2023"] =  {
                        "6": {
                            "Abonnement":12.85,
                            "Consommation": {"HP":0.2460, "HC":0.1828}
                        },
                        "9": {
                            "Abonnement":16.55,
                            "Consommation": {"HP":0.2460, "HC":0.1828}
                        },
                        "12": {
                            "Abonnement":19.97,
                            "Consommation": {"HP":0.2460, "HC":0.1828}
                        },
                        "15": {
                            "Abonnement":23.24,
                            "Consommation": {"HP":0.2460, "HC":0.1828}
                        },
                        "18": {
                            "Abonnement":26.48,
                            "Consommation": {"HP":0.2460, "HC":0.1828}
                        },
                        "24": {
                            "Abonnement":33.28,
                            "Consommation": {"HP":0.2460, "HC":0.1828}
                        },
                        "30": {
                            "Abonnement":39.46,
                            "Consommation": {"HP":0.2460, "HC":0.1828}
                        },
                        "36": {
                            "Abonnement":44.66,
                            "Consommation": {"HP":0.2460, "HC":0.1828}
                        }
        }
        pricing["HCHPManual2024"] =  {
                        "6": {
                            "Abonnement":12.85,
                            "Consommation": {"HP":0.27, "HC":0.2068}
                        },
                        "9": {
                            "Abonnement":16.55,
                            "Consommation": {"HP":0.27, "HC":0.2068}
                        },
                        "12": {
                            "Abonnement":19.97,
                            "Consommation": {"HP":0.27, "HC":0.2068}
                        },
                        "15": {
                            "Abonnement":23.24,
                            "Consommation": {"HP":0.27, "HC":0.2068}
                        },
                        "18": {
                            "Abonnement":26.48,
                            "Consommation": {"HP":0.27, "HC":0.2068}
                        },
                        "24": {
                            "Abonnement":33.28,
                            "Consommation": {"HP":0.27, "HC":0.2068}
                        },
                        "30": {
                            "Abonnement":39.46,
                            "Consommation": {"HP":0.27, "HC":0.2068}
                        },
                        "36": {
                            "Abonnement":44.66,
                            "Consommation": {"HP":0.27, "HC":0.2068}
                        }
        }
        pricing["TEMPOManual2023"] =  {
                        "6": {
                            "Abonnement":12.8,
                            "Consommation": {'HC': {'BLUE': 0.1056, 'WHITE': 0.1246, 'RED': 0.1328}, 'HP': {'BLUE': 0.1369, 'WHITE': 0.1654, 'RED': 0.7324}}
                        },
                        "9": {
                            "Abonnement":16,
                            "Consommation": {'HC': {'BLUE': 0.1056, 'WHITE': 0.1246, 'RED': 0.1328}, 'HP': {'BLUE': 0.1369, 'WHITE': 0.1654, 'RED': 0.7324}}
                        },
                        "12": {
                            "Abonnement":19.29,
                            "Consommation": {'HC': {'BLUE': 0.1056, 'WHITE': 0.1246, 'RED': 0.1328}, 'HP': {'BLUE': 0.1369, 'WHITE': 0.1654, 'RED': 0.7324}}
                        },
                        "15": {
                            "Abonnement":22.3,
                            "Consommation": {'HC': {'BLUE': 0.1056, 'WHITE': 0.1246, 'RED': 0.1328}, 'HP': {'BLUE': 0.1369, 'WHITE': 0.1654, 'RED': 0.7324}}
                        },
                        "18": {
                            "Abonnement":25.29,
                            "Consommation": {'HC': {'BLUE': 0.1056, 'WHITE': 0.1246, 'RED': 0.1328}, 'HP': {'BLUE': 0.1369, 'WHITE': 0.1654, 'RED': 0.7324}}
                        },
                        "30": {
                            "Abonnement":38.13,
                            "Consommation": {'HC': {'BLUE': 0.1056, 'WHITE': 0.1246, 'RED': 0.1328}, 'HP': {'BLUE': 0.1369, 'WHITE': 0.1654, 'RED': 0.7324}}
                        },
                        "36": {
                            "Abonnement":44.28,
                            "Consommation": {'HC': {'BLUE': 0.1056, 'WHITE': 0.1246, 'RED': 0.1328}, 'HP': {'BLUE': 0.1369, 'WHITE': 0.1654, 'RED': 0.7324}}
                        }
        }
        pricing["TEMPOManual2024"] =  {
                        "6": {
                            "Abonnement":12.8,
                            "Consommation": {'HC': {'BLUE': 0.1296, 'WHITE': 0.1486, 'RED': 0.1568}, 'HP': {'BLUE': 0.1609, 'WHITE': 0.1894, 'RED': 0.7564}}
                        },
                        "9": {
                            "Abonnement":16,
                            "Consommation": {'HC': {'BLUE': 0.1296, 'WHITE': 0.1486, 'RED': 0.1568}, 'HP': {'BLUE': 0.1609, 'WHITE': 0.1894, 'RED': 0.7564}}
                        },
                        "12": {
                            "Abonnement":19.29,
                            "Consommation": {'HC': {'BLUE': 0.1296, 'WHITE': 0.1486, 'RED': 0.1568}, 'HP': {'BLUE': 0.1609, 'WHITE': 0.1894, 'RED': 0.7564}}
                        },
                        "15": {
                            "Abonnement":22.3,
                            "Consommation": {'HC': {'BLUE': 0.1296, 'WHITE': 0.1486, 'RED': 0.1568}, 'HP': {'BLUE': 0.1609, 'WHITE': 0.1894, 'RED': 0.7564}}
                        },
                        "18": {
                            "Abonnement":25.29,
                            "Consommation": {'HC': {'BLUE': 0.1296, 'WHITE': 0.1486, 'RED': 0.1568}, 'HP': {'BLUE': 0.1609, 'WHITE': 0.1894, 'RED': 0.7564}}
                        },
                        "30": {
                            "Abonnement":38.13,
                            "Consommation": {'HC': {'BLUE': 0.1296, 'WHITE': 0.1486, 'RED': 0.1568}, 'HP': {'BLUE': 0.1609, 'WHITE': 0.1894, 'RED': 0.7564}}
                        },
                        "36": {
                            "Abonnement":44.28,
                            "Consommation": {'HC': {'BLUE': 0.1296, 'WHITE': 0.1486, 'RED': 0.1568}, 'HP': {'BLUE': 0.1609, 'WHITE': 0.1894, 'RED': 0.7564}}
                        }
        }

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