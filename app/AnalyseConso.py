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
from datetime import datetime, timedelta, time
from aboCounter import AboCounter
from earthWatcher import EarthWatcher
from tempoCalGetter import TempoCalGetter
from priceGetter import PriceGetter

def processENEDISFile(csvFile, priceCounters):
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
    for counter in priceCounters:
        counter.setNbMoisAbo(nbMois)

    return priceCounters, earthWatcher


def processEDFFile(csvFile, priceCounters):
    lecteur = csv.reader(csvFile, delimiter=';')
    i = 0
    earthWatcher = EarthWatcher()
    firstDate = None
    lastDate = None
    parsedDate = None
    
    for ligne in lecteur:
        if len(ligne) == 0: #Ligne vide
            continue
        if len(ligne) == 1: #Ligne PreEntete
            if ligne[0] != "Récapitulatif de ma consommation" :
                raise Exception("Format Inconnu, merci de chosir le fichier EDF 'Récupitulatif de ma consommation'")
        elif "kWh" in ligne[1]:
            print("Lecture de la ligne d'entete")
        else:
            parsedDate = ligne[0] #format JJ/MM/AAAA
            conso = ligne[1] #en kwh
            print("Parsing "+parsedDate+" ("+conso+"kwh)")
            conso = float(conso)
            if firstDate is None:
                firstDate = datetime.strptime(parsedDate,"%d/%m/%Y")
        
            formattedDate = datetime.strptime(parsedDate,"%d/%m/%Y").strftime("%Y-%m-%d")
            consoHoraire = float(conso / 24)
            for heure in range(0,23):
                parsedTime = time(heure,0,0).strftime("%H:%M:%S")
                print(parsedTime)
                for counter in priceCounters:
                    counter.addConsummatedHour(consoHoraire,parsedTime,formattedDate)
                earthWatcher.addConsummatedHour(consoHoraire,parsedTime,formattedDate)

    # Calcul du nombre de mois que recouvre le fichier CSV
    lastDate = datetime.strptime(parsedDate,"%d/%m/%Y")
        
    # Durée en mois couverte par le CSV 
    nbMois = int((lastDate - firstDate).days / 30)
    for counter in priceCounters:
        counter.setNbMoisAbo(nbMois)

    return priceCounters, earthWatcher


def getZenCalendar():
    data={}
    with open("data/calZen.csv", newline='') as csvfile:
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

def doStuff(puissance, enedisFileStream="", edfFileStream=""):
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
    chemin_csv = "data/consoexemple.csv"

    # Prix des différents W.h. Faire un XML/YAML/Json ?
    # Attention, les données d'origine sont pour des kW.h mais les données du CSV son des W.h
    # Données d'origine  https://particulier.edf.fr/content/dam/2-Actifs/Documents/Offres/Grille_prix_Tarif_Bleu.pdf
    # Tarifs au 01/08/2023
    
    ZenHPEco = 0.2228
    ZenHCEco = 0.1295
    ZenHPSobriete = 0.6712
    ZenHCSobriete = 0.2228
    
    fallbackAbonnement = {
                "ZEN": {
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
            }

    priceGetter = PriceGetter()
    dynamicPricing = priceGetter.getPrice()

    # Dictionnaire des jours eco/sobriété de l'offre ZenFlex
    CalZen = getZenCalendar()

    baseCounter = AboCounter("Base")
    baseCounter.configurePricingPlans(dynamicPricing["Base"])

    tempoCounter = AboCounter("Tempo")
    tempoCounter.setCalendrierJours(TempoCalGetter())
    tempoCounter.configureHeuresCreuses(HC)
    tempoCounter.configurePricingPlans(dynamicPricing["TEMPO"])
    
    HCHPCounter = AboCounter("HCHP")
    HCHPCounter.configureHeuresCreuses(HC)
    HCHPCounter.configurePricingPlans(dynamicPricing["HCHP"])

    ZenCounter = AboCounter("Zen")
    ZenCounter.setCalendrierJours(CalZen)
    ZenCounter.configureHeuresCreuses(HCZenFlex)
    ZenCounter.configurePricingPlans(fallbackAbonnement["ZEN"])

    priceCounters = [baseCounter, tempoCounter, HCHPCounter, ZenCounter]
    for counter in priceCounters:
        counter.setPuissance(puissance)

    if enedisFileStream != "":
        print("Using ENEDIS Imported dataset")
        priceCounters, earthWatcher = processENEDISFile(enedisFileStream,priceCounters)
    elif edfFileStream != "":
        print("Using EDF Imported dataset")
        priceCounters, earthWatcher = processEDFFile(edfFileStream,priceCounters)
    else: 
        print("Using Example Dataset")
        with open(chemin_csv, newline='', encoding='utf-8-sig') as csvfile:
            priceCounters, earthWatcher = processENEDISFile(csvfile,priceCounters)


    return priceCounters, earthWatcher


if __name__ == '__main__':
    doStuff()