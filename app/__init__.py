from flask import Flask

app = Flask(__name__)
app.secret_key = "ta_clef_secrete"  # À personnaliser

from app import routes
