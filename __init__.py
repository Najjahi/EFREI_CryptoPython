from cryptography.fernet import Fernet
from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from urllib.request import urlopen
import sqlite3, hashlib, base64
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html')

key = Fernet.generate_key()
f = Fernet(key)

@app.route('/encrypt/<string:valeur>') 
def encryptage(valeur):
    valeur_bytes = valeur.encode()  # Conversion str -> bytes
    token = f.encrypt(valeur_bytes)  # Encrypt la valeur
    return f"Valeur encryptée : {token.decode()}"   # Retourne le token en str

@app.route('/decrypt/<string:token>')
def decryptage(token):
    try:
        valeur_bytes = f.decrypt(token.encode())  # Déchiffrement
        return f"Valeur décryptée : {valeur_bytes.decode()}"  # Retourne la valeur déchiffrée
    except Exception as e:
        return f"Erreur lors du déchiffrement : {str(e)}"
      
@app.route('/encrypt2/<string:cle>/<string:valeur>')
def encryptage2(cle, valeur):
    try:
        hashed_key = hashlib.sha256(cle.encode()).digest()
        print(f"Hachage SHA-256 de la clé (32 octets) : {hashed_key}")
        base64_key = base64.urlsafe_b64encode(hashed_key)
        base64_key_str = base64_key.decode() 
        print(f"Clé Base64 URL-safe : {base64_key_str}")
        f = Fernet(cle.encode())  # Génération de l'instance Fernet avec la clé fournie
        valeur_bytes = valeur.encode()  # Conversion str -> bytes
        token = f.encrypt(valeur_bytes)  # Chiffrement
        return f"Valeur encryptée : {token.decode()}"  # Retourne le token
    except Exception as e:
        return f"Erreur lors du chiffrement : {str(e)}"

@app.route('/decrypt2/<string:cle>/<string:token>')
def decryptage2(cle, token):
    try:        
        print(f"Clé : {cle}")  # Vérification de la clé et du token
        print(f"Token : {token}")               
        f = Fernet(cle.encode())  # Générer l'instance Fernet avec la clé fournie : La clé doit être encodée en bytes         
        valeur_bytes = f.decrypt(token.encode())  # Déchiffrement du token : Le token doit aussi être encodé en bytes      
       
        return f"Valeur décryptée : {valeur_bytes.decode()}"  # Retourner la valeur déchiffrée : Convertir la valeur déchiffrée en chaîne
    except Exception as e:
        
        print(f"Erreur lors du déchiffrement : {str(e)}") # Afficher l'erreur détaillée pour le débogage
        return f"Erreur lors du déchiffrement : {str(e)}"
                                                                                                                                                     
if __name__ == "__main__":
  app.run(debug=True)
