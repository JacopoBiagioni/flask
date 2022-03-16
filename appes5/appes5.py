# Si vuole realizzare un sito web per memorizzare le squadre di uno sport a scelta.
# L'utente deve poter inserire il nome della squadra, la data di fondazione e la città.
# Deve inoltre poter effetuare delle ricerche inserendo uno dei valori delle colonne e ottenendo i dati presenti.

from flask import Flask, render_template, request 
import pandas as pd 

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return render_template("formes5.html")

@app.route("/data", methods=["GET"])
def data():
    squadra = request.args["Nome"]
    anno = request.args["Anno"]
    citta = request.args["Citta"]
    df = pd.read_csv("/workspace/Flask/appEs5/templates/dati.csv")
    dUtente = {"Squadra" : squadra, "Anno_Fondazione" : anno, "Città" : citta}
    df = df.append(dUtente, ignore_index = True)
    df.to_csv("/workspace/Flask/appEs5/templates/datisquadre.csv", index=False)
    return df.to_html()


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)