from cryptography.fernet import Fernet
from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/hello')
def hello_world():
    return render_template('hello.html')

key = Fernet.generate_key()
f = Fernet(key)

@app.route('/encrypt/<string:valeur>') 
def encryptage(valeur):
    valeur_bytes = valeur.encode()  # Conversion str -> bytes
    token = f.encrypt(valeur_bytes)  # Encrypt la valeur
    return f"Valeur encryptée : {token.decode()}"   # Retourne le token en str

@app.route('/decrypt', methods=['POST'])
def decryptage():
    valeur = request.form['valeur']  # Récupère la valeur envoyée via le formulaire
    try:       
        valeur_bytes = valeur.encode()  # Décryptage de la valeur reçue (il faut qu'elle soit en bytes, donc on encode)
        decrypted_value = f.decrypt(valeur_bytes)  # Décrypte la valeur
        return f"Valeur décryptée : {decrypted_value.decode()}"  # Retourne la valeur décryptée
    except Exception as e:
        return f"Erreur lors du décryptage: {str(e)}"n str
                                                                                                                                                     
if __name__ == "__main__":
  app.run(debug=True)
