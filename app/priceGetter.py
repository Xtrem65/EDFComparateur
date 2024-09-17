from collections import defaultdict
#import requests

import re
from PyPDF2 import PdfReader


import urllib.request
import io

class PriceGetter:
    
    def __init__(self):
        self.dataSource = 'https://particulier.edf.fr/content/dam/2-Actifs/Documents/Offres/Grille_prix_Tarif_Bleu.pdf'
        self.dataSourceZenFlex = "https://particulier.edf.fr/content/dam/2-Actifs/Documents/Offres/Grille-prix-zen-flex.pdf"
        self.pricing = self.loadPrice()

    def getPrice(self):
        return self.pricing

    def loadPrice(self,):
        # calling urllib to create a reader of the pdf url
        File = urllib.request.urlopen(self.dataSource)
        reader = PdfReader(io.BytesIO(File.read()))

        parsing = None
        pattern = None
        pricing = {}
        for page in reader.pages:
            content = page.extract_text()
            for line in content.splitlines():
                if "Option Base" in line:
                    print("Retrieving prices from OptionBase")
                    regex="^(\d+).([{\d,}]+)[\s]+([{\d,}]+)"
                    pattern = re.compile(regex)
                    parsing="Base"
                if "Option Heures C" in line:
                    print("Retrieving prices from Option Heures Creuses")
                    regex="^(\d+).([{\d,}]+)[\s]+([{\d,}]+)[\s]+([{\d,}]+)"
                    pattern = re.compile(regex)
                    parsing="HCHP"
                if "Option Tempo" in line:
                    print("Retrieving prices from Option Tempo")
                    regex="^(\d+).([{\d,}]+)[\s]+([{\d,}]+)[\s]+([{\d,}]+)[\s]+([{\d,}]+)[\s]+([{\d,}]+)[\s]+([{\d,}]+)[\s]+([{\d,}]+)"
                    pattern = re.compile(regex)
                    parsing="TEMPO"
                if parsing is not None:
                    if pattern.match(line):
                        m = pattern.search(line)
                        if parsing not in pricing :
                            pricing[parsing] = {}
                        if parsing == "Base":
                            pricing[parsing][m.group(1)] = {
                                "Abonnement" : float(m.group(2).replace(',','.')),
                                "Consommation" : {
                                    "HP": float(m.group(3).replace(',','.'))/100
                                }
                            }
                        if parsing == "HCHP":
                            pricing[parsing][m.group(1)] = {
                                "Abonnement" : float(m.group(2).replace(',','.')),
                                "Consommation" : {
                                    "HP": float(m.group(3).replace(',','.'))/100,
                                    "HC": float(m.group(4).replace(',','.'))/100
                                }
                            }
                        if parsing == "TEMPO":
                            pricing[parsing][m.group(1)] = {
                                "Abonnement" : float(m.group(2).replace(',','.')),
                                "Consommation" : {
                                    "HC": {
                                        "BLUE" : float(m.group(3).replace(',','.'))/100,
                                        "WHITE" : float(m.group(5).replace(',','.'))/100,
                                        "RED" : float(m.group(7).replace(',','.'))/100,
                                    },
                                    "HP": {
                                        "BLUE" : float(m.group(4).replace(',','.'))/100,
                                        "WHITE" : float(m.group(6).replace(',','.'))/100,
                                        "RED" : float(m.group(8).replace(',','.'))/100,
                                    },
                                }
                            }
        # calling urllib to create a reader of the pdf url
        File = urllib.request.urlopen(self.dataSourceZenFlex)
        reader = PdfReader(io.BytesIO(File.read()))

        parsing = None
        pattern = None
        pricing["zen-flex"] = {}
        for page in reader.pages:
            content = page.extract_text()
            for line in content.splitlines():
                regex="^(\d+).([{\d,}]+)[\s]+([{\d,}]+)[\s]+([{\d,}]+)[\s]+([{\d,}]+)[\s]+([{\d,}]+)[\s]+"
                pattern = re.compile(regex)
                if pattern.match(line):
                    m = pattern.search(line)
                    pricing["zen-flex"][m.group(1)] = {
                                "Abonnement" : float(m.group(2).replace(',','.')),
                                "Consommation" : {
                                    "HC": {
                                        "ECO" : float(m.group(3).replace(',','.'))/100,
                                        "SOBRIETE" : float(m.group(5).replace(',','.'))/100,
                                    },
                                    "HP": {
                                        "ECO" : float(m.group(4).replace(',','.'))/100,
                                        "SOBRIETE" : float(m.group(6).replace(',','.'))/100,
                                    },
                                }
                            }
        return pricing
