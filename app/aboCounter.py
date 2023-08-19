from collections import defaultdict

from datetime import datetime, timedelta
import traceback


class AboCounter:
    
    def __init__(self, name):
        self.name = name
        self.totalConso = 0
        self.details = defaultdict(lambda: 0.0)
        self.pricing = {}
        self.aboPricingPlan = {}
        self.errors = defaultdict(None)

        self.aboMensuel = 0
        self.nbMoisAbo = 1
        self.totalConsommatedWatts = 0

        self.calendrierJours = None
        self.heuresCreuses = []



    def configureAboPricingPlans(self, pricingPlan):
        self.aboPricingPlan = pricingPlan


    def setPuissance(self, puissance):
        try:
            self.aboMensuel=self.aboPricingPlan[puissance]
        except BaseException as e:
            self.aboMensuel = 0
            self.errors["Cet abonnement n'est pas disponible avec cette puissance"] = "Aucune tarification d'abonnement trouvée pour la puissance " + puissance

    def setNbMoisAbo(self, nbMois):
        self.nbMoisAbo = nbMois

    def getAboMensuel(self):
        return self.aboMensuel
    
    def configureConsoPricingPlans(self, pricing):
        self.pricing = pricing

    def setCalendrierJours(self, calJour):
        self.calendrierJours = calJour

    def configureHeuresCreuses(self, heuresCreuses):
        self.heuresCreuses = heuresCreuses

    def getCouleurFromJour(self, jour):
        if self.calendrierJours is None:
            return ""
        else:
            return self.calendrierJours.get(jour)
    
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
        
    def getTotalConsommatedWatts(self):
        return round(self.totalConsommatedWatts)
    
    def addConsummatedHour(self, conso, heure, jour):
        if heure < "06:00":
            jour = (datetime.strptime(jour,"%Y-%m-%d").date() - timedelta(days=1)).strftime("%Y-%m-%d")

        try:
            couleur = self.getCouleurFromJour(jour)
            tarification = self.getTarificationFromHeure(heure)
            instantTarif = self.getInstantTarification(couleur, tarification)
        except BaseException as e:
            self.errors[jour]="Could not find tarification"
            return
        self.totalConsommatedWatts = self.totalConsommatedWatts + conso
        hourCost = instantTarif * conso

        self.totalConso = self.totalConso + hourCost
        self.details[couleur] = self.details[couleur] + hourCost
        self.details[tarification] = self.details[tarification] + hourCost

    def getTotalConso(self):
        return round(self.totalConso)
    
    def getTotalAbo(self):
        return round(self.aboMensuel * self.nbMoisAbo)
    
    def getTotal(self):
        return round(self.getTotalConso() + self.getTotalAbo())
    
    def getDetails(self):
        return self.details


