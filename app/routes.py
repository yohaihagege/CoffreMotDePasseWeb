from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from app.forms import LoginForm, SecondaryPasswordForm, PasswordEntryForm
from app.security import generate_key, encrypt, decrypt
from app.storage import load_data, save_data, load_secondary_password, store_secondary_password
import os
from flask import render_template, request, redirect, url_for, session, flash
from app import app
from app.forms import PasswordEntryForm
from app.storage import charger_donnees, sauvegarder_donnees, generer_cle_depuis_mdp, chiffrer, dechiffrer
routes = Blueprint('routes', __name__)


@routes.route("/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    cle = generate_key(form.master_password.data)
    session["master_key"] = cle
    if form.validate_on_submit():
        sec_pwd = load_secondary_password()
        if not sec_pwd:
            # Première utilisation : demande un mot de passe secondaire
            return redirect(url_for("routes.set_secondary"))
        else:
            session["authenticated"] = True
            return redirect(url_for("routes.unlock"))
    return render_template("login.html", form=form)

@routes.route("/set_secondary", methods=["GET", "POST"])
def set_secondary():
    form = SecondaryPasswordForm()
    if form.validate_on_submit():
        cle = session.get("master_key")
        enc = encrypt(cle, form.secondary_password.data)
        store_secondary_password(enc)
        session["authenticated"] = True
        return redirect(url_for("routes.unlock"))
    return render_template("secondary.html", form=form, title="Définir un mot de passe secondaire")

@routes.route("/unlock", methods=["GET", "POST"])
def unlock():
    global decrypted
    if not session.get("authenticated"):
        return redirect(url_for("routes.login"))

    form = SecondaryPasswordForm()
    if form.validate_on_submit():
        enc = load_secondary_password()
        try:
            cle = session.get("master_key")
            dec = decrypt(cle, enc)
            if dec == form.secondary_password.data:
                session["secondary_verified"] = True
                return redirect(url_for("routes.dashboard"))
            else:
                flash("Mot de passe incorrect.")
        except:
            flash("Erreur de déchiffrement.")
    return render_template("secondary.html", form=form, title="Déverrouiller les mots de passe")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "master_key" not in session or not session.get("secondary_verified"):
        return redirect(url_for("routes.login"))

    cle = session["master_key"]
    form = PasswordEntryForm()
    donnees = charger_donnees()

    if request.method == "POST" and form.validate_on_submit():
        site = form.site.data
        identifiant = form.username.data
        motdepasse = form.password.data

        # Chiffrement du mot de passe
        motdepasse_chiffre = chiffrer(cle, motdepasse)

        # Sauvegarde
        donnees[site] = {
            "identifiant": identifiant,
            "motdepasse": motdepasse_chiffre.decode()
        }
        sauvegarder_donnees(donnees)
        flash("Mot de passe ajouté avec succès.", "success")
        return redirect(url_for("dashboard"))

    # Déchiffrement pour affichage
    donnees_visibles = []
    for site, infos in donnees.items():
        try:
            motdepasse_dechiffre = dechiffrer(cle, infos["motdepasse"].encode())
        except:
            motdepasse_dechiffre = "Erreur de déchiffrement"
        donnees_visibles.append((site, infos["identifiant"], motdepasse_dechiffre))

    return render_template("dashboard.html", form=form, passwords=donnees_visibles)