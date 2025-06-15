from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from app.forms import LoginForm, SecondaryPasswordForm, PasswordEntryForm
from app.security import generate_key, encrypt, decrypt
from app.storage import load_data, save_data, load_secondary_password, store_secondary_password
import os

routes = Blueprint('routes', __name__)
key = None
decrypted = False

@routes.route("/", methods=["GET", "POST"])
def login():
    global key
    form = LoginForm()
    if form.validate_on_submit():
        key = generate_key(form.master_password.data)
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
        enc = encrypt(key, form.secondary_password.data)
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
            dec = decrypt(key, enc)
            if dec == form.secondary_password.data:
                decrypted = True
                return redirect(url_for("routes.dashboard"))
            else:
                flash("Mot de passe incorrect.")
        except:
            flash("Erreur de déchiffrement.")
    return render_template("secondary.html", form=form, title="Déverrouiller les mots de passe")

@routes.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if not decrypted:
        return redirect(url_for("routes.unlock"))

    form = PasswordEntryForm()
    data = load_data()
    passwords = []

    for site, value in data.items():
        try:
            decoded = decrypt(key, value.encode())
            identifiant, motdepasse = decoded.split(":")
            passwords.append((site, identifiant, motdepasse))
        except:
            continue

    if form.validate_on_submit():
        if len(form.password.data) < 12 or not any(c.isdigit() for c in form.password.data) or not any(c in "!@#$%^&*()-_=+[{]}\\|;:'\",<.>/?`~" for c in form.password.data):
            flash("Mot de passe trop faible.")
            return redirect(url_for("routes.dashboard"))

        entry = f"{form.username.data}:{form.password.data}"
        encrypted = encrypt(key, entry).decode()
        data[form.site.data] = encrypted
        save_data(data)
        return redirect(url_for("routes.dashboard"))

    return render_template("dashboard.html", form=form, passwords=passwords)
