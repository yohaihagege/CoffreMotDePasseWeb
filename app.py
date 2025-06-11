from flask import Flask, render_template, request, redirect, session
import os, json, base64
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

app = Flask(__name__)
app.secret_key = 'vraiment_tres_secret'

sel = b'mon_sel_unique_et_constant'

def generer_cle(mdp):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=sel,
        iterations=100000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(mdp.encode()))

@app.route('/', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        mdp = request.form['mdp_maitre']
        try:
            cle = generer_cle(mdp)
            session['cle'] = cle.decode()
            return redirect('/dashboard')
        except:
            return "Erreur dans la génération de la clé."
    return render_template("login.html")

@app.route('/dashboard')
def dashboard():
    if 'cle' not in session:
        return redirect('/')
    return render_template("dashboard.html")

if __name__ == "__main__":
    app.run(debug=True)
