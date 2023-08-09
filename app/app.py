from flask import Flask
app = Flask(__name__)
from AnalyseConso import *


def retrievePricingsfromEDF():
	#https://particulier.edf.fr/content/dam/2-Actifs/Documents/Offres/Grille_prix_Tarif_Bleu.pdf
	return ""


@app.route('/')
def hello():
	pricings = retrievePricingsfromEDF()

	data = doStuff()
	return "Hello World!"

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000, debug=True)
