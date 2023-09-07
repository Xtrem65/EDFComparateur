from flask import Flask, request, render_template
app = Flask(__name__)
from AnalyseConso import *
from appContext import AppContext
from io import StringIO
import argparse
parser = argparse.ArgumentParser(description="Just an example",
	formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("-d", "--debug", action="store_true", help="debug mode")
parser.add_argument("-v", "--verbose", action="store_true", help="increase verbosity")
args = parser.parse_args()


appContext = AppContext()

@app.route('/data', methods=["GET"])
def showData():
	return render_template("data.html", data=appContext)

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
			results, earthWatcher = doStuff(appContext, puissance, enedisFile, "")
			return render_template("results.html",simulations=results, earthWatcher=earthWatcher, tempo=TempoCalGetter())
		elif edfData:
			edfFile = StringIO(edfData.decode("ISO 8859-15"), newline=None)
			results, earthWatcher = doStuff(appContext, puissance, "", edfFile)
			return render_template("results.html",simulations=results, earthWatcher=earthWatcher, tempo=TempoCalGetter())
		else:
			results, earthWatcher = doStuff(appContext, puissance)
			return render_template("results.html", simulations=results,earthWatcher=earthWatcher, tempo=TempoCalGetter(), test=True)

	totalAvailablePuissances = []
	for nomAbo, abonnementConnu in appContext.getPricings().items():
		puissancesPossiblePourCetAbo = abonnementConnu.keys()
		for puissancePossiblePourCetAbo in puissancesPossiblePourCetAbo:
			if puissancePossiblePourCetAbo not in totalAvailablePuissances:
				totalAvailablePuissances.append(puissancePossiblePourCetAbo)

	return render_template("homepage.html", puissances=totalAvailablePuissances) #Ici, on peut upload son fichier, cliquer sur un bouton pour processer et être redirigé vers la page de resultats

@app.route('/config', methods=["GET"])
def getConfig():
	totalAvailablePuissances = []
	for nomAbo, abonnementConnu in appContext.getPricings().items():
		puissancesPossiblePourCetAbo = abonnementConnu.keys()
		for puissancePossiblePourCetAbo in puissancesPossiblePourCetAbo:
			if puissancePossiblePourCetAbo not in totalAvailablePuissances:
				totalAvailablePuissances.append(puissancePossiblePourCetAbo)
	return {"puissances": totalAvailablePuissances }

@app.route('/simulations', methods=["GET", "POST"])
def postSimulation():
	fileEnedis = request.files.get("fileENEDIS")
	fileEDF = request.files.get("fileEDF")
	#puissance = request.form["puissance"]
	#enedisData = fileEnedis.stream.read()
	#edfData = fileEDF.stream.read()
	# check if file loaded successfully or not
	#if enedisData:
		#enedisFile = StringIO(enedisData.decode("UTF-8"), newline=None)
		#results, earthWatcher = doStuff(appContext, puissance, enedisFile, "")
		#return render_template("results.html",simulations=results, earthWatcher=earthWatcher, tempo=TempoCalGetter())
	#elif edfData:
		#edfFile = StringIO(edfData.decode("ISO 8859-15"), newline=None)
		#results, earthWatcher = doStuff(appContext, puissance, "", edfFile)
		#return render_template("results.html",simulations=results, earthWatcher=earthWatcher, tempo=TempoCalGetter())
	
	results, earthWatcher = doStuff(appContext, "9")
	return {
		"simulations":"merci",
		"earthWatcher":"lu",
		"tempo":"cas"
		}


if __name__ == '__main__':
	if args.debug == True :
		app.run(host='0.0.0.0', port=8000, debug=True)
	else:
		app.run(host='0.0.0.0', port=8000, ssl_context='adhoc')
