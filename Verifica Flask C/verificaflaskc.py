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

linee = pd.read_csv('/workspace/flask/Verifica Flask C/templates/tpl_percorsi.geojson')
quartieri = gpd.read_file('/workspace/flask/Verifica Flask C/templates/ds964_nil_wm (1).zip')


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/selezione', methods=['GET'])
def selezione():
  scelta = request.args['scelta']
  if scelta == 'es1':
    return redirect(url_for('numero'))
  elif scelta == 'es2':
    return redirect(url_for('input'))
  else:
    return redirect(url_for('dropdown'))

@app.route('/lunghezza', methods=['GET'])
def lunghezza():
    return render_template('lunghezza.html')




if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)