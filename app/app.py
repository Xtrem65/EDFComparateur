from flask import Flask, request, render_template
app = Flask(__name__)
from AnalyseConso import *


def retrievePricingsfromEDF():
	#https://particulier.edf.fr/content/dam/2-Actifs/Documents/Offres/Grille_prix_Tarif_Bleu.pdf
	return ""


@app.route('/', methods=["GET", "POST"])
def homepage():
	if request.method == "POST":
		file = request.files.get("file")
		file_content = file.read()
		# check if file loaded successfully or not
		if file_content:
			results = doStuff(file_content)
			return render_template("results.html",results=results)
		else:
			results = doStuff()
			return render_template("results.html", results=results)

	return render_template("homepage.html") #Ici, on pourra upload son fichier, cliquer sur un bouton pour processer et être redirigé vers la page de resultats

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000, debug=True)
