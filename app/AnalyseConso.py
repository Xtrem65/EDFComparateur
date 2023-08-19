#################################################################################################
#
# Ce programme sert à analyser la consommation d'électricité d'un abonnement EDF, il permet de
# de comparer les différents forfaits EDF sur cette consommation passée, et de déterminer lequel
# est le plus avantageux.
# Il tient compte des jours Tempo (bleu, blanc, rouge) et des heures creuses.
#
# Auteur : Koicoubeh
# Contributeur du fichier CSV d'exemple et aide au débug : @MathieuMf (Twitter)
#
# Ce programme est sous licence CC BY-NC-SA 4.0
# https://creativecommons.org/licenses/by-nc-sa/4.0/
#
#################################################################################################

#################################################################################################
#
# v1.0 : 2023-08-03
# - Première version fonctionnelle
# v1.1 : 2023-08-04
# - Ajout de l'abonnement ZenFlex
#
#################################################################################################

import csv
from datetime import datetime, timedelta
from aboCounter import AboCounter
from rteCommunicator import RteCommunicator
from earthWatcher import EarthWatcher
from tempoCalGetter import TempoCalGetter

def processFile(csvFile, priceCounters):
    lecteur = csv.reader(csvFile, delimiter=';')
    i = 0
    earthWatcher = EarthWatcher()
    
    for ligne in lecteur:
        # Gestion simpliste de l'entête du CSV : si le 5e caractère de la ligne n'est pas un tiret (donc une date), ignorer la ligne
        if ligne[0][4] == "-":
            i += 1
            date_heure = ligne[0]
            consommation = int(ligne[1]) if ligne[1].strip() else 0        
            consommation = consommation / 2000  # Convertir les W sur 30 minutes en kW.h
            date_heure = date_heure[:-6]  # Enlever le décalage horaire (ex: +01:00)            

            # Récupération du 1er mois, pour compter le nombre de mois que recouvre le CSV
            if i == 1:
                PremiereDate = datetime.fromisoformat(date_heure.replace("Z", "+00:00"))

            # Extraire la date (ex: "2023-01-05")
            jour = date_heure[:10]
            # Extraire l'heure (ex: "23:59")
            heure = date_heure[11:]
            for counter in priceCounters:
                counter.addConsummatedHour(consommation,heure,jour)
            earthWatcher.addConsummatedHour(consommation,heure,jour)
    
    # Calcul du nombre de mois que recouvre le fichier CSV
    DerniereDate = datetime.fromisoformat(date_heure.replace("Z", "+00:00"))

    # Durée en mois couverte par le CSV 
    nbMois = int((DerniereDate - PremiereDate).days / 30)
    DernierMois = int(date_heure[5:7])
    print(f"Nombre de lignes traitées : {i}")
    # nbMois = DernierMois - PremierMois + 1
    print(f"Nombre de mois dans le CSV : {nbMois}")
    for counter in priceCounters:
        counter.setNbMoisAbo(nbMois)

    return priceCounters, earthWatcher


def getZenCalendar():
    data={}
    with open("../data/calZen.csv", newline='') as csvfile:
        # Créer un objet lecteur CSV
        lecteur_csv = csv.reader(csvfile, delimiter=';')
        
        # Parcourir chaque ligne du CSV
        for ligne in lecteur_csv:
            # Convertir la date au format "01/09/2019" en objet datetime
            date_str = ligne[0]
            date_obj = datetime.strptime(date_str, "%d/%m/%Y").date()
            
            # Utiliser la date au format "YYYY-MM-DD" comme clé dans le dictionnaire
            # et la couleur comme valeur associée
            data[date_obj.strftime("%Y-%m-%d")] = ligne[1]
    return data

def doStuff(puissance, enedisFileStream=""):
    #################################################################################################
    #
    # Variables amenées à être modifiées par les utilisateurs
    #
    #################################################################################################

    # Tableaux contenant les heures creuses. Si c'est pas creux... c'est plein !
    # exemple : 0,1,2,3,4,5,22,23 : HC de 0h à 6h et de 22h à 24h
    HC = [0,1,2,3,4,5,22,23]

    # Horaires HC/HP pour l'abonnement ZenFlex
    HCZenFlex = [0,1,2,3,4,5,6,7,14,15,16,17,20,21,22,23]

    # Chemin vers le fichier CSV. Ce fichier est à récupérer sur le site d'Enedis, en ayant activé 
    # l'option "Historique de consommation" avec le pas demi-horaire dans l'espace client.
    # Il faut que le fichier soit sur 1 an (pas de contrôle sur ce point, mais le résultat ne serait pas significatif)
    chemin_csv = "../data/consoexemple.csv"

    #################################################################################################
    #
    # Variables peu susceptibles d'être modifiées par les utilisateurs
    #
    #################################################################################################

    # Prix des différents W.h. Faire un XML/YAML/Json ?
    # Attention, les données d'origine sont pour des kW.h mais les données du CSV son des W.h
    # Données d'origine  https://particulier.edf.fr/content/dam/2-Actifs/Documents/Offres/Grille_prix_Tarif_Bleu.pdf
    # Tarifs au 01/08/2023

    TempoBleuHC = 0.1056
    TempoBleuHP = 0.1369
    TempoBlancHC = 0.1246
    TempoBlancHP = 0.1654
    TempoRougeHC = 0.1328
    TempoRougeHP = 0.7324
    BleuHC = 0.1828
    BleuHP = 0.246
    ZenHPEco = 0.2228
    ZenHCEco = 0.1295
    ZenHPSobriete = 0.6712
    ZenHCSobriete = 0.2228
    BleuBase = 0.2276

    Abonnement = {
                "Base": {
                    "3":9.47,
                    "6":12.44,
                    "9":15.63,
                    "12":18.89,
                    "15":21.92,
                    "18":24.92,
                    "24":31.60,
                    "30":37.29,
                    "36":44.66
                },
                "HCHP": {
                    "6":12.85,
                    "9":16.55,
                    "12":19.97,
                    "15":23.24,
                    "18":26.48,
                    "24":33.28,
                    "30":39.46,
                    "36":44.64
                },
                "TEMPO": {
                    "6":12.80,
                    "9":16.00,
                    "12":19.29,
                    "15":22.30,
                    "18":25.29,
                    "30":38.13,
                    "36":44.28
                },
                "ZEN": {
                    "6":12.62,
                    "9":15.99,
                    "12":19.27,
                }
            }
    # Dictionnaire des jours bleu blanc rouge. Chaque élément est un tuple (date, couleur)
    RTE = RteCommunicator()
    #tempoCalendar = RTE.getTempo()

    # Dictionnaire des jours eco/sobriété de l'offre ZenFlex
    CalZen = getZenCalendar()

    baseCounter = AboCounter("Base")
    baseCounter.configureConsoPricingPlans({"HP":BleuBase})
    baseCounter.configureAboPricingPlans(Abonnement["Base"])

    tempoCounter = AboCounter("Tempo")
    tempoCounter.setCalendrierJours(TempoCalGetter())
    tempoCounter.configureHeuresCreuses(HC)
    tempoCounter.configureConsoPricingPlans({"HP":{"BLUE":TempoBleuHP,"WHITE":TempoBlancHP,"RED":TempoRougeHP},"HC":{"BLUE":TempoBleuHC,"WHITE":TempoBlancHC,"RED":TempoRougeHC}})
    tempoCounter.configureAboPricingPlans(Abonnement["TEMPO"])
    
    HCHPCounter = AboCounter("HCHP")
    HCHPCounter.configureConsoPricingPlans({"HP":BleuHP, "HC":BleuHC})
    HCHPCounter.configureHeuresCreuses(HC)
    HCHPCounter.configureAboPricingPlans(Abonnement["HCHP"])

    ZenCounter = AboCounter("Zen")
    ZenCounter.setCalendrierJours(CalZen)
    ZenCounter.configureHeuresCreuses(HCZenFlex)
    ZenCounter.configureConsoPricingPlans({"HP":{"BLEU":ZenHPEco,"BLANC":ZenHPEco,"ROUGE":ZenHPSobriete},"HC":{"BLEU":ZenHCEco,"BLANC":ZenHCEco,"ROUGE":ZenHCSobriete}})
    ZenCounter.configureAboPricingPlans(Abonnement["ZEN"])

    priceCounters = [baseCounter, tempoCounter, HCHPCounter, ZenCounter]
    for counter in priceCounters:
        counter.setPuissance(puissance)

    if enedisFileStream == "":
        print("Using Example Dataset")
        with open(chemin_csv, newline='', encoding='utf-8-sig') as csvfile:
            priceCounters, earthWatcher = processFile(csvfile,priceCounters)
    else: 
        print("Using shared dataset")
        #Checker le format
        #Appeller processFile avec le fichier importé (attention csv_reader attends un vrai fichier)
        priceCounters, earthWatcher = processFile(enedisFileStream,priceCounters)

    return priceCounters, earthWatcher


if __name__ == '__main__':
    doStuff()