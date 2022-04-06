# 1. Avere un elenco di tutte le stazioni radio che si trovano in un certo quartiere. L’utente sceglie il nome del quartiere da un elenco di radiobutton 
# (ordinato in ordine alfabetico) e clicca su un bottone. Il sito risponde con l’elenco ordinato in ordine alfabetico delle stazioni radio presenti in quel quartiere.
# 2. Avere le stazioni radio presenti in un quartiere. L’utente inserisce il nome del quartiere (anche solo una parte di esso), clicca su un bottone e ottiene la mappa del 
# quartiere con un pallino nero sulla posizione delle stazioni radio.
# 3. Avere il numero di stazioni per ogni municipio (in ordine crescente sul numero del municipio) e il grafico corrispondente.

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

stazioni = pd.read_csv('/workspace/flask/Verifica Flask B/templates/coordfix_ripetitori_radiofonici_milano_160120_loc_final.csv', sep=';')
stazionigeo = gpd.read_file('/workspace/flask/Verifica Flask B/templates/ds710_coordfix_ripetitori_radiofonici_milano_160120_loc_final.geojson')
quartieri = gpd.read_file('/workspace/flask/Verifica Flask B/templates/ds964_nil_wm (1).zip')

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/scelta', methods=['GET'])
def scelta():
    quartieri_ordine = quartieri.NIL.to_list()
    quartieri_ordine = list(set(quartieri_ordine))
    quartieri_ordine.sort()
    return render_template('scelta.html', quartieri = quartieri_ordine)

@app.route('/stazioniradio', methods=['GET'])
def stazioniradio():
    quartieriRadio = request.args['quartiere']
    quartiereUtente = quartieri[quartieri['NIL'] == quartieriRadio]
    stazioniQuartieri = stazionigeo[stazionigeo.within(quartiereUtente.geometry.squeeze())]
    return render_template('elenco.html', risultato = stazioniQuartieri.to_html())



if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)