# Realizzare un sito web che restituisca la mappa dei quartieri di Milano.
# Ci deve essere una home page con un link quartieri di Milano: cliccando su questo link si deve visualizzare la mappa dei quartieri di Milano.

from flask import Flask, request, render_template, send_file, make_response, url_for, Response
app = Flask(__name__)

import io
import geopandas as gpd
import contextily as ctx
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

quartieri = gpd.read_file('/workspace/flask/ds964_nil_wm (1).zip')

@app.route('/', methods=['GET'])
def home():
    return render_template('homepage.html')

@app.route('/quartieri', methods=['GET'])
def quartieri1():
    fig, ax = plt.subplots(figsize = (12,8))
    imgUtente.to_crs(epsg=3857).plot(ax=ax, alpha=0.5, edgecolor='k')
    ctx.add_basemap(ax=ax)
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')

@app.route('/plot', methods=['GET'])
def plot():
    global imgUtente
    quartieriUtente = request.args['Quartiere']
    imgUtente = quartieri[quartieri['NIL'] == quartieriUtente]
    return render_template('quartieri.html')

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)