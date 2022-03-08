# Realizzare un sito web che permetta la registrazione degli utenti
# L'utente inserisce il nome, uno username, una password
# La conferma della password e il sesso.
# Se le informazioni sono corrette il sito salva le informazioni in una struttura dati opportuna (lista di dizionari)

# Prevedere la possibilità di fare il login 
# Se sono corrette fornire un messaggio di benvenuto diverso a seconda del sesso

from flask import Flask, render_template, request
app = Flask(__name__)

lista = []

@app.route('/', methods=['GET'])
def home():
    return render_template('formes3.html')

@app.route('/data', methods=['GET'])
def data():
  password = request.args['Password']
  conferma_password = request.args['Conferma password']
  sesso = request.args['Sex']
  username = request.args['Username']
  nome = request.args['Name']
  if password == conferma_password:
      utente = {'Nome': nome, 'Username': username, 'Sex': sesso, 'Password': password}
      lista.append(utente)
      print(lista)
      if sesso == 'M':
          saluto = 'Benvenuto!'
      elif sesso == 'F':
          saluto = 'Benvenuta!'
      else:
          saluto = 'Benvenut*!'
      return render_template('welcome.html', benvenuto = saluto)
  else:
      return '<h1>Errore</h1>'

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')


if __name__ == '__main__':
  app.run(host='0.0.0.0', port=3245, debug=True)