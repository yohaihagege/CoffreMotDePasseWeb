from flask import Blueprint, render_template, redirect, url_for, session, request, flash
from app.forms import LoginForm, SecondaryPasswordForm, PasswordEntryForm
from app.security import generate_key, chiffrer, dechiffrer, encrypt_to_bytes
from app.storage import load_data, save_data, store_secondary_password, load_secondary_password

routes = Blueprint('routes', __name__)

@routes.route("/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        cle = generate_key(form.master_password.data)
        session["authenticated"] = True
        session["master_key"] = cle
        sec_pwd = load_secondary_password()
        if not sec_pwd:
            return redirect(url_for("routes.set_secondary"))
        else:
            return redirect(url_for("routes.secondary_login"))
    return render_template("login.html", form=form)

@routes.route("/set_secondary", methods=["GET", "POST"])
def set_secondary():
    form = SecondaryPasswordForm()
    if form.validate_on_submit():
        cle = session.get("master_key")
        if not cle:
            flash("Erreur : la clé de chiffrement est introuvable.", "danger")
            return redirect(url_for("routes.login"))
        enc = encrypt_to_bytes(cle, form.secondary_password.data)
        store_secondary_password(enc)
        session["authenticated"] = True
        return redirect(url_for("routes.secondary_login"))
    return render_template("secondary.html", form=form, title="Définir un mot de passe secondaire")

@routes.route("/secondary_login", methods=["GET", "POST"])
def secondary_login():
    if not session.get("authenticated"):
        return redirect(url_for("routes.login"))

    form = SecondaryPasswordForm()
    if form.validate_on_submit():
        encrypted = load_secondary_password()
        try:
            key = session.get("master_key")
            if not key:
                flash("Clé maître manquante.", "danger")
                return redirect(url_for("routes.login"))

            decrypted = dechiffrer(key, encrypted)
            if decrypted == form.secondary_password.data:
                session["secondary_verified"] = True
                return redirect(url_for("routes.dashboard"))
            else:
                flash("Mot de passe secondaire incorrect.", "danger")
        except Exception as e:
            flash("Erreur de déchiffrement.", "danger")

    return render_template("secondary_login.html", form=form, title="Déverrouiller les mots de passe")

@routes.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "master_key" not in session or not session.get("secondary_verified"):
        return redirect(url_for("routes.login"))

    cle = session["master_key"]
    form = PasswordEntryForm()
    donnees = load_data()

    if request.method == "POST" and form.validate_on_submit():
        site = form.site.data
        identifiant = form.username.data
        motdepasse = form.password.data

        motdepasse_chiffre = chiffrer(cle, motdepasse)

        donnees[site] = {
            "identifiant": identifiant,
            "motdepasse": motdepasse_chiffre
        }
        save_data(donnees)
        flash("Mot de passe ajouté avec succès.", "success")
        return redirect(url_for("routes.dashboard"))

    donnees_visibles = []
    for site, infos in donnees.items():
        try:
            motdepasse_dechiffre = dechiffrer(cle, infos["motdepasse"])
        except:
            motdepasse_dechiffre = "Erreur de déchiffrement"
        donnees_visibles.append((site, infos["identifiant"], motdepasse_dechiffre))

    return render_template("dashboard.html", form=form, passwords=donnees_visibles)
