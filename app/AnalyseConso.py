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

def doStuff():
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

    # Abonnement en kVA : 6, 9 ou 12
    abonnement = 9

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
    AboTempo6kva = 12.8
    AboTempo9kva = 16.0
    AboTempo12kva = 19.29

    BleuBase = 0.2276
    AboBleu3kva = 9.47
    AboBleu6kva = 12.44
    AboBleu9kva = 15.63
    AboBleu12kva = 18.89

    BleuHC = 0.1828
    BleuHP = 0.246
    AboHC6kva = 12.85
    AboHP9kva = 16.55
    AboHP12kva = 19.97

    ZenHPEco = 0.2228
    ZenHCEco = 0.1295
    ZenHPSobriete = 0.6712
    ZenHCSobriete = 0.2228
    ZenAbo6kva = 12.62
    ZenAbo9kva = 15.99
    ZenAbo12kva = 19.27

    # Dictionnaire des jours bleu blanc rouge. Chaque élément est un tuple (date, couleur)
    CalBar = {}

    # Dictionnaire des jours eco/sobriété de l'offre ZenFlex
    CalZen = {}

    # Tableau des données de consommation. Chaque élément est un tuple (date_heure, consommation HC, consommation HP)
    CalConso = []

    # Nombre de mois dans le fichier CSV de consommation de l'utilisateur. Par défaut 12
    nbMois = 12
    PremierMois = 0
    DernierMois = 0

    # Initialisation des sommes pour chacun des forfaits testés
    simulTempo, simulBase, simulHCHP, simulZen = 0.0, 0.0, 0.0, 0.0

    # Consommation en HP et HC
    ConsoHP, ConsoHC = 0.0, 0.0

    # Importe un fichier avec les dates des jours bleu blanc rouge, et les stocke dans une liste
    # Fichier CSV avec 2 colonnes : date et couleur
    # Généré à la main depuis les fichiers "Calendrier TEMPO" dispos sur le site de RTE :
    # https://www.rte-france.com/eco2mix/telecharger-les-indicateurs
    # Ouvrir le fichier CSV en mode lecture
    with open("../data/calBAR.csv", newline='') as csvfile:
        # Créer un objet lecteur CSV
        lecteur_csv = csv.reader(csvfile, delimiter=';')
        
        # Parcourir chaque ligne du CSV
        for ligne in lecteur_csv:
            # Convertir la date au format "01/09/2019" en objet datetime
            date_str = ligne[0]
            date_obj = datetime.strptime(date_str, "%d/%m/%Y").date()
            
            # Utiliser la date au format "YYYY-MM-DD" comme clé dans le dictionnaire
            # et la couleur comme valeur associée
            CalBar[date_obj.strftime("%Y-%m-%d")] = ligne[1]


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
            CalZen[date_obj.strftime("%Y-%m-%d")] = ligne[1]


    baseCounter = AboCounter("Base")
    baseCounter.setPricing({"HP":BleuBase})

    tempoCounter = AboCounter("Tempo")
    tempoCounter.setCalendrierJours(CalBar)
    tempoCounter.setHeuresCreuses(HC)
    tempoCounter.setPricing({"HP":{"BLEU":TempoBleuHP,"BLANC":TempoBlancHP,"ROUGE":TempoRougeHP},"HC":{"BLEU":TempoBleuHC,"BLANC":TempoBlancHC,"ROUGE":TempoRougeHC}})
    
    HCHPCounter = AboCounter("HCHP")
    HCHPCounter.setPricing({"HP":BleuHP, "HC":BleuHC})
    HCHPCounter.setHeuresCreuses(HC)

    ZenCounter = AboCounter("Zen")
    ZenCounter.setCalendrierJours(CalZen)
    ZenCounter.setHeuresCreuses(HCZenFlex)
    ZenCounter.setPricing({"HP":{"BLEU":ZenHPEco,"BLANC":ZenHPEco,"ROUGE":ZenHPSobriete},"HC":{"BLEU":ZenHCEco,"BLANC":ZenHCEco,"ROUGE":ZenHCSobriete}})

    # Ouvrir le fichier CSV de consommation en mode lecture
    with open(chemin_csv, newline='', encoding='utf-8-sig') as csvfile:
        lecteur = csv.reader(csvfile, delimiter=';')
        i = 0
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

                baseCounter.addConsummatedHour(consommation,heure,jour)
                HCHPCounter.addConsummatedHour(consommation,heure,jour)
                tempoCounter.addConsummatedHour(consommation,heure,jour)
                ZenCounter.addConsummatedHour(consommation,heure,jour)


        simulBase = baseCounter.getTotal()
        simulHCHP = HCHPCounter.getTotal()
        simulTempo = tempoCounter.getTotal()
        simulZen = ZenCounter.getTotal()

        # Calcul du nombre de mois que recouvre le fichier CSV
        DerniereDate = datetime.fromisoformat(date_heure.replace("Z", "+00:00"))

        # Durée en mois couverte par le CSV 
        nbMois = int((DerniereDate - PremiereDate).days / 30)
        DernierMois = int(date_heure[5:7])
        print(f"Nombre de lignes traitées : {i}")
        # nbMois = DernierMois - PremierMois + 1
        print(f"Nombre de mois dans le CSV : {nbMois}")

    # Ajout du coût annuel de l'abonnement
    if abonnement == 6:
        simulTempo += AboTempo6kva*nbMois
        simulBase += AboBleu6kva*nbMois
        simulHCHP += AboHC6kva*nbMois
        simulZen += ZenAbo6kva*nbMois    
    elif abonnement == 9:
        simulTempo += AboTempo9kva*nbMois
        simulBase += AboBleu9kva*nbMois
        simulHCHP += AboHP9kva*nbMois
        simulZen += ZenAbo9kva*nbMois
    elif abonnement == 12:
        simulTempo += AboTempo12kva*nbMois
        simulBase += AboBleu12kva*nbMois
        simulHCHP += AboHP12kva*nbMois
        simulZen += ZenAbo12kva*nbMois

    #Arrondir à 2 décimales
    simulTempo = round(simulTempo, 2)
    simulBase = round(simulBase, 2)
    simulHCHP = round(simulHCHP, 2)
    simulZen = round(simulZen, 2)
    ConsoHC = round(ConsoHC, 2)
    ConsoHP = round(ConsoHP, 2)

    print()
    print(f"Consommation HP : {ConsoHP} kW.h")
    print(f"Consommation HC : {ConsoHC} kW.h")
    print(f"Consommation totale : {round(ConsoHP + ConsoHC, 2)} kW.h")
    print()
    print(f"Simulation des coûts sur {nbMois} mois, selon les 3 forfaits :")
    print(f"  Tempo = {simulTempo} €")
    print(f"  Base = {simulBase} €")
    print(f"  HCHP = {simulHCHP} €")
    print(f"  ZenFlex = {simulZen} €")
    print()


if __name__ == '__main__':
    doStuff()