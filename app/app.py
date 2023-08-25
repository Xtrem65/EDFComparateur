from flask import Flask, request, render_template
app = Flask(__name__)
from AnalyseConso import *
from io import StringIO
import argparse
parser = argparse.ArgumentParser(description="Just an example",
	formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-d", "--debug", action="store_true", help="debug mode")
parser.add_argument("-v", "--verbose", action="store_true", help="increase verbosity")
args = parser.parse_args()

@app.route('/', methods=["GET", "POST"])
def homepage():
	if request.method == "POST":
		fileEnedis = request.files.get("fileENEDIS")
		fileEDF = request.files.get("fileEDF")
		puissance = request.form["puissance"]
		enedisData = fileEnedis.stream.read()
		edfData = fileEDF.stream.read()
		# check if file loaded successfully or not
		if enedisData:
			enedisFile = StringIO(enedisData.decode("UTF-8"), newline=None)
			results, earthWatcher = doStuff(puissance, enedisFile, "")
			return render_template("results.html",simulations=results, earthWatcher=earthWatcher)
		elif edfData:
			edfFile = StringIO(edfData.decode("ISO 8859-15"), newline=None)
			results, earthWatcher = doStuff(puissance, "", edfFile)
			return render_template("results.html",simulations=results, earthWatcher=earthWatcher)
		else:
			results, earthWatcher = doStuff(puissance)
			return render_template("results.html", simulations=results,earthWatcher=earthWatcher, test=True)

	return render_template("homepage.html") #Ici, on peut upload son fichier, cliquer sur un bouton pour processer et être redirigé vers la page de resultats

if __name__ == '__main__':
	if args.debug == True :
		app.run(host='0.0.0.0', port=8000, debug=True)
	else:
		app.run(host='0.0.0.0', port=8000, ssl_context='adhoc')
