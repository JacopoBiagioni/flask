# 1. Avere l’elenco delle linee tranviarie e di bus che hanno un percorso la cui lunghezza è compresa tra due valori inseriti dall’utente. Ordinare le linee in ordine crescente 
# sul numero della linea.
# 2. Avere un elenco di tutte le linee (tram e bus) che passano in un certo quartiere. L’utente inserisce il nome del quartiere (anche solo una parte del nome) e il sito 
# risponde con l’elenco ordinato in ordine crescente delle linee che passano in quel quartiere.
# 3. Avere la mappa della città con il percorso di una linea scelta dall’utente. L’utente sceglie il numero della linea da un menù a tendina (le linee devono essere ordinati 
# in ordine crescente), clicca su un bottone e ottiene la mappa di Milano con il percorso della linea prescelta.

from flask import Flask, render_template, request, Response, redirect, url_for
app = Flask(__name__)

import io
import geopandas as gpd
import pandas as pd
import contextily as ctx
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

linee = gpd.read_file('/workspace/flask/Verifica Flask C/templates/tpl_percorsi.geojson')
quartieri = gpd.read_file('/workspace/flask/Verifica Flask C/templates/ds964_nil_wm (1).zip')


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/selezione', methods=['GET'])
def selezione():
  scelta = request.args['scelta']
  if scelta == 'es1':
    return redirect(url_for('lunghezza'))
  elif scelta == 'es2':
    return redirect(url_for('nome'))
  else:
    return redirect(url_for('tendina'))

@app.route('/lunghezza', methods=['GET'])
def lunghezza():
  return render_template('lunghezza.html')

@app.route("/elenco", methods=["GET"])
def elenco():
    Min = min(request.args["lunghezza_minima"], request.args["lunghezza_massima"])
    Max = max(request.args["lunghezza_minima"], request.args["lunghezza_massima"])
    linee_distanza = linee[(linee["lung_km"] > Min) & (linee["lung_km"] < Max)].sort_values("linea")
    return render_template("elenco.html", tabella = linee_distanza.to_html())

@app.route('/nome', methods=['GET'])
def nome():
  return render_template('nome.html')

@app.route('/elencolinee', methods=['GET'])
def elenconlinee():
  quartiere = request.args['quartieri']
  quartiereUtente = quartieri[quartieri['NIL'].str.contains(quartiere)]
  linee_quartiere = linee[linee.intersects(quartiereUtente.geometry.squeeze())].sort_values('linea')
  return render_template('elenco.html', risultato = linee_quartiere.to_html())

@app.route('/tendina', methods=['GET'])
def tendina():
  return render_template('tendina.html', linee = linee["linea"].drop_duplicates().sort_values(ascending=True))

@app.route('/sceltalinee', methods=['GET'])
def sceltalinee(): 
  global lineeUtente
  linea = int(request.args["linea"])
  lineeUtente = linee[linee["linea"] == linea]
  return render_template("vistalinee.html", linea = linea)

@app.route('/mappa', methods=['GET'])
def mappa():
  fig, ax = plt.subplots(figsize = (12,8))
  lineeUtente.to_crs(epsg=3857).plot(ax=ax, color='r')
  quartieri.to_crs(epsg=3857).plot(ax=ax, alpha=0.5, edgecolor='k')
  ctx.add_basemap(ax=ax)
  output = io.BytesIO()
  FigureCanvas(fig).print_png(output)
  return Response(output.getvalue(), mimetype='image/png')


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)