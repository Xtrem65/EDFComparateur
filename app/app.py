from flask import Flask, request, render_template
app = Flask(__name__)
from AnalyseConso import *
from io import StringIO

@app.route('/', methods=["GET", "POST"])
def homepage():
	if request.method == "POST":
		file = request.files.get("file")
		puissance = request.form["puissance"]
		data = file.stream.read()
		# check if file loaded successfully or not
		if data:
			enedisFile = StringIO(data.decode("UTF8"), newline=None)
			results = doStuff(puissance, enedisFile)
			return render_template("results.html",simulations=results)
		else:
			results = doStuff(puissance)
			return render_template("results.html", simulations=results,test=True)

	return render_template("homepage.html") #Ici, on peut upload son fichier, cliquer sur un bouton pour processer et être redirigé vers la page de resultats

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000, debug=True)
