# 1. Avere il numero di stazioni per ogni municipio (in ordine crescente sul numero del municipio) e il grafico corrispondente;
# 2. Avere un elenco di tutte le stazioni radio che si trovano in un certo quartiere. L’utente inserisce il nome del quartiere (anche solo una parte del nome) e il sito risponde
# con l’elenco ordinato in ordine alfabetico delle stazioni radio presenti in quel quartiere;
# 3. Avere la posizione in città di una stazione radio. L’utente sceglie il nome della stazione da un menù a tendina (i nomi delle stazioni devono essere ordinati in ordine 
# alfabetico), clicca su un bottone e ottiene la mappa del quartiere che contiene la stazione radio, con un pallino nero sulla posizione della stazione radio.
from flask import Flask, render_template, request, Response
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

stazioni = pd.read_csv('/workspace/flask/Verifica Flask A/templates/coordfix_ripetitori_radiofonici_milano_160120_loc_final.csv', sep=';')

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/numero', methods=['GET'])
def num():
  risultato = stazioni.groupby('MUNICIPIO')['OPERATORE'].count().reset_index().sort_values(by='MUNICIPIO',ascending=True)
  return render_template('link1.html', risultato = risultato.to_html())

@app.route('/input', methods=['GET'])
def input1():
  return render_template

@app.route('/dropdown', methods=['GET'])
def dropd():
  return render_template

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)