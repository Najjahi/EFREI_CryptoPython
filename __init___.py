from cryptography.fernet import Fernet
from flask import Flask, render_template_string, render_template, jsonify, request, json
from urllib.request import urlopen
import sqlite3
import hashlib
import base64
                                                                                                                                   
app = Flask(__name__)
# je transforme la saisir de l'utilisateur en clé fermet valide ( je la hash puis je la convertir en base64)

def transformercle(custom_key: str) -> bytes:

    hash_obj = hashlib.sha256(custom_key.encode())
    digest = hash_obj.digest()
    fernet_key = base64.urlsafe_b64encode(digest)
    return fernet_key

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/encrypt3', methods=['POST'])
def encryptage():
    data = request.get_json()
    cle = data.get('cle')
    valeur = data.get('valeur')
    fernet_key = transformercle(cle)
    f = Fernet(fernet_key)
    token = f.encrypt(valeur.encode())
    return jsonify({"result": token.decode()})

@app.route('/decrypt3', methods=['POST'])
def decryptage():
    data = request.get_json()
    cle = data.get('cle')
    token = data.get('token')
    fernet_key = transformercle(cle)
    f = Fernet(fernet_key)
    valeur = f.decrypt(token.encode()).decode()
    return jsonify({"result": valeur})

if __name__ == "__main__":
    app.run(debug=True)
