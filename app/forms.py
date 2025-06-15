# Tu ajouteras ici les classes de formulaire (connexion, ajout, etc.) avec Flask-WTF
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    master_password = PasswordField("Mot de passe maître", validators=[DataRequired()])
    submit = SubmitField("Se connecter")

class SecondaryPasswordForm(FlaskForm):
    secondary_password = PasswordField("Mot de passe secondaire", validators=[DataRequired()])
    submit = SubmitField("Déverrouiller")

class PasswordEntryForm(FlaskForm):
    site = StringField("Site", validators=[DataRequired()])
    username = StringField("Identifiant", validators=[DataRequired()])
    password = PasswordField("Mot de passe", validators=[DataRequired(), Length(min=12)])
    submit = SubmitField("Enregistrer")
