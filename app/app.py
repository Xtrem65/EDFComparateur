from flask import Flask
app = Flask(__name__)


def retrievePricingsfromEDF():
	#https://particulier.edf.fr/content/dam/2-Actifs/Documents/Offres/Grille_prix_Tarif_Bleu.pdf
	return ""


@app.route('/')
def hello():
	#pricings = retrievePricingsfromEDF()

	return "Hello World!" + pricings

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000, debug=True)
