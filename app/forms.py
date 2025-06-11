# Tu ajouteras ici les classes de formulaire (connexion, ajout, etc.) avec Flask-WTF
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length

class LoginForm(FlaskForm):
    master_password = PasswordField("Mot de passe maître", validators=[InputRequired()])
    submit = SubmitField("Se connecter")

class SecondaryPasswordForm(FlaskForm):
    secondary_password = PasswordField("Mot de passe secondaire", validators=[InputRequired()])
    submit = SubmitField("Déverrouiller")

class PasswordEntryForm(FlaskForm):
    site = StringField("Site", validators=[InputRequired()])
    username = StringField("Identifiant", validators=[InputRequired()])
    password = PasswordField("Mot de passe", validators=[InputRequired(), Length(min=12)])
    submit = SubmitField("Enregistrer")
