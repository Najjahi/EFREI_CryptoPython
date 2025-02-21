from cryptography.fernet import Fernet
from flask import Flask, render_template_string, render_template, jsonify, request, json
from urllib.request import urlopen
import sqlite3
import hashlib
import base64
                                                                                                                                   
app = Flask(__name__)
# je transforme la saisir de l'utilisateur en clé fermet valide ( je la hash puis je la convertir en base64)

def transformercle(custom_key: str) -> bytes: #prend une chaîne (str) en entrée, nommée custom_key.Elle renvoie un objet de type bytes

    hash_obj = hashlib.sha256(custom_key.encode()) #convertit la chaîne en 1séquence de bytes (hashlib.sha256(...) génère 1objet de hachage SHA-256 à partir de cette clé.
    digest = hash_obj.digest() #retourne le résultat du hachage sous forme de bytes (une séquence de 32 octets).
    fernet_key = base64.urlsafe_b64encode(digest) #encode le hash SHA-256 en Base64 URL-safe (1version qui évite les caractères spéciaux comme + et /).
    return fernet_key #La clé transformée est retournée sous forme de bytes, prête à être utilisée avec Fernet pour le chiffrement/déchiffrement.

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/encrypt', methods=['POST'])
def encryptage():
    data = request.get_json() #extrait le corps de la requête sous forme de dictionnaire Python.( "cle": "MaSuperCleSecrete",  "token": "gAAAAABl...")
    cle = data.get('cle') #récupère la clé secrète envoyée.
    valeur = data.get('valeur') 
    fernet_key = transformercle(cle) #appelle la fonction transformercle()  pour convertir la clé utilisateur en une clé utilisable avec Fernet.
    f = Fernet(fernet_key) #Un objet Fernet est créé avec la clé transformée. Cet objet permet de déchiffrer les données
    token = f.encrypt(valeur.encode()) #valeur.encode() : Convertit la chaîne de texte en byte et f.encrypt(...) : Utilise l’objet Fernet (f) pour chiffrer la valeur.
    return jsonify({"result": token.decode()}) #token.decode() : Convertit le résultat (bytes) en une chaîne de texte UTF-8 lisible, jsonify({...}) : Retourne le token chiffré au format JSON.

@app.route('/decrypt', methods=['POST'])
def decryptage():
    data = request.get_json()
    cle = data.get('cle')
    token = data.get('token') #récupère le message chiffré (appelé token).
    fernet_key = transformercle(cle)
    f = Fernet(fernet_key) #(Fernet ne fonctionne qu’avec des données binaires).
    valeur = f.decrypt(token.encode()).decode() #token.encode():Convertit le token en bytes,f.decrypt(...): Déchiffre le message en bytes, .decode():Convertit le résultat en 1chaîne lisible (UTF-8).
    return jsonify({"result": valeur}) #jsonify(...) convertit la valeur déchiffrée en une réponse JSON :

if __name__ == "__main__":
    app.run(debug=True)
