# inserire il nome di una provincia, cliccare su un bottone ed ottenere le seguenti informazioni:
# a. mappa geografica con i confini della provincia (confini neri) con l’indicazione al suo interno dei comuni che la compongono (confini rossi)
# b. area della provincia (espressa in km 2 )
# 2. scegliere il nome della provincia da una serie di menù a tendina ed avere le stesse informazioni dell’esercizioprecedente. Per scegliere la provincia, l’utente sceglie 
# prima la regione (in cui si trova la provincia) da un menù a tendina, la seleziona, clicca su un bottone e ottiene l’elenco delle province di quella regione, sempre in un menù
# a tendina. A questo punto sceglie la provincia dal menù a tendina, clicca su un bottone e ottiene le informazioni.
# Tutti gli elenchi devono essere ordinati in ordine alfabetico. Ottimizzare il lavoro in modo da poter riutilizzare il codice dell’esercizio 1
# 3. come l’esercizio precedente ma l’utente sceglie a partire dalla ripartizione geografica (che contiene la regione
# che contiene a sua volta la provincia). Usare sempre menù a tendina e ordinare sempre gli elenchi in ordine alfabetico. Ottimizzare il lavoro in modo da poter riutilizzare 
# il codice dell’esercizio 2.

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

regioni = gpd.read_file('/workspace/flask/CorrezioneVerficaFlaskA21/templates/Regioni.zip')
comuni = gpd.read_file('/workspace/flask/CorrezioneVerficaFlaskA21/templates/Comuni.zip')
province = gpd.read_file('/workspace/flask/CorrezioneVerficaFlaskA21/templates/Province.zip')
ripartizioni = gpd.read_file('/workspace/flask/CorrezioneVerficaFlaskA21/templates/RipGeo01012021_g_WGS84.zip')

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/provincia', methods=['GET'])
def provincia():
    return render_template('provincia.html')

@app.route('/infoprov', methods=['GET'])
def infoprov():
    global provUtente, comuniProv
    provincia = request.args['provincia']
    provUtente = province[province['DEN_UTS'] == provincia]
    comuniProv = comuni[comuni.within(provUtente.geometry.squeeze())]
    return render_template('infoprov.html')

@app.route('/mappa', methods=['GET'])
def mappa():
    fig, ax = plt.subplots(figsize = (12,8))
    provUtente.to_crs(epsg=3857).plot(ax=ax, alpha=0.5, edgecolor='k')
    comuniProv.to_crs(epsg=3857).plot(ax=ax, alpha=0.5, edgecolor='r')
    ctx.add_basemap(ax=ax)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/sceltaregione', methods=['GET'])
def sceltaregione():
    return render_template('sceltaregione.html', regioni = regioni['DEN_REG'].sort_values(ascending=True))

@app.route('/sceltaprov', methods=['GET'])
def sceltaprov():
    global regUtente, provReg
    regione = request.args['regione']
    regUtente = regioni[regioni['DEN_REG'] == regione]
    provReg = province[province.within(regUtente.geometry.squeeze())]
    return render_template('sceltaprov.html', province = provReg['DEN_UTS'].sort_values(ascending=False))

@app.route('/infoprov2', methods=['GET'])
def infoprov2():
    global prov_utente, com_prov
    provincia = request.args['provincia']
    prov_utente = province[province['DEN_UTS'] == provincia]
    com_prov = comuni[comuni.within(prov_utente.geometry.squeeze())]
    return render_template('infoprov2.html')

@app.route('/mappa2', methods=['GET'])
def mappa2():
    fig, ax = plt.subplots(figsize = (12,8))
    prov_utente.to_crs(epsg=3857).plot(ax=ax, alpha=0.5, edgecolor='k')
    com_prov.to_crs(epsg=3857).plot(ax=ax, alpha=0.5, edgecolor='r')
    ctx.add_basemap(ax=ax)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/ripartizione', methods=['GET'])
def ripartizione():
    return render_template('ripartizione.html', ripartizioni = ripartizioni['DEN_RIP'].sort_values(ascending=False))

@app.route('/dropreg', methods=['GET'])
def dropreg():
    ripartizione = request.args['ripartizione']
    ripartizioneUtente = ripartizioni[ripartizioni['DEN_RIP'] == ripartizione]
    regRip = ripartizioneUtente[ripartizioneUtente.contains(regioni.geometry.squeeze())]
    return render_template('dropreg.html', regioni = regioni['DEN_REG'].sort_values(ascending=False))

@app.route('/droprov', methods=['GET'])
def droprov():
    regione = request.args['regione']
    reg_utente = regioni[regioni['DEN_REG'] == regione]
    prov_reg = province[province.within(reg_utente.geometry.squeeze())]
    return render_template('droprov.html', province = prov_reg['DEN_UTS'].sort_values(ascending=False))

@app.route('/infoprov3', methods=['GET'])
def infoprov3():
    global provinUtente, comuProv
    provincia = request.args['provincia']
    provinUtente = province[province['DEN_UTS'] == provincia]
    comuProv = comuni[comuni.within(provinUtente.geometry.squeeze())]
    return render_template('infoprov3.html')

@app.route('/mappa3', methods=['GET'])
def mappa3():
    fig, ax = plt.subplots(figsize = (12,8))
    provinUtente.to_crs(epsg=3857).plot(ax=ax, alpha=0.5, edgecolor='k')
    comuProv.to_crs(epsg=3857).plot(ax=ax, alpha=0.5, edgecolor='r')
    ctx.add_basemap(ax=ax)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')



if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)