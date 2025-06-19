from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length

class LoginForm(FlaskForm):
    master_password = PasswordField("Mot de passe maître", validators=[DataRequired(), Length(min=8)])
    submit = SubmitField("Se connecter")

class SecondaryPasswordForm(FlaskForm):
    secondary_password = PasswordField("Mot de passe secondaire", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("Valider")

class PasswordEntryForm(FlaskForm):
    site = StringField("Site", validators=[DataRequired()])
    username = StringField("Identifiant", validators=[DataRequired()])
    password = PasswordField("Mot de passe", validators=[DataRequired(), Length(min=8)])
    submit = SubmitField("Ajouter")
