from flask import Flask
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.secret_key = "ta_clef_secrete"  # À personnaliser
csrf = CSRFProtect(app)


from app.routes import routes # ⬅️ important : doit être après la création de l'app

app.register_blueprint(routes)  # ⬅️ enregistre les routes du blueprint