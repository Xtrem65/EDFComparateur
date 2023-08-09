from collections import defaultdict

from datetime import datetime, timedelta


class AboCounter:
    
    def __init__(self, name):
        self.name = name
        self.total = 0
        self.details = defaultdict(lambda: 0.0)
        self.pricing = {}

        self.calendrierJours = {}
        self.heuresCreuses = []

    def setPricing(self, pricing):
        self.pricing = pricing

    def setCalendrierJours(self, calJour):
        self.calendrierJours = calJour

    def setHeuresCreuses(self, heuresCreuses):
        self.heuresCreuses = heuresCreuses

    def getCouleurFromJour(self, jour):
        if jour in self.calendrierJours:
            return self.calendrierJours[jour]
        else:
            return ""
    
    def getTarificationFromHeure(self, heure):
        heure = datetime.strptime(heure,"%H:%M:%S").hour
        if heure in self.heuresCreuses:
            return "HC"
        else:
            return "HP"

    def getInstantTarification(self, couleur, tarification):
        tarifHoraire = self.pricing[tarification]
        if isinstance(tarifHoraire, float):
            return tarifHoraire
        else:
            return tarifHoraire[couleur]
    
    def addConsummatedHour(self, conso, heure, jour):
        if heure < "06:00":
            jour = (datetime.strptime(jour,"%Y-%m-%d").date() - timedelta(days=1)).strftime("%Y-%m-%d")

        couleur = self.getCouleurFromJour(jour)
        tarification = self.getTarificationFromHeure(heure)
        instantTarif = self.getInstantTarification(couleur, tarification)

        hourCost = instantTarif * conso

        self.total = self.total + hourCost
        self.details[couleur] = self.details[couleur] + hourCost
        self.details[tarification] = self.details[tarification] + hourCost
        #self.details[couleur][tarification] = self.details[couleur][tarification] + hourCost

    def getTotal(self):
        return self.total


