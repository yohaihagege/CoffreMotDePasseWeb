import os

# Dossiers à créer
folders = [
    "app",
    "app/templates",
    "static"
]

# Fichiers à créer avec un contenu minimal
files = {
    "run.py": """from app import app

if __name__ == "__main__":
    app.run(debug=True)
""",
    "app/__init__.py": """from flask import Flask

app = Flask(__name__)
app.secret_key = "ta_clef_secrete"  # À personnaliser

from app import routes
""",
    "app/routes.py": """from flask import render_template, redirect, url_for, request, flash
from app import app

@app.route('/')
def accueil():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return render_template('login.html')
""",
    "app/utils.py": "# Ici tu mettras les fonctions : generer_cle_depuis_mdp, chiffrer, dechiffrer, etc.\n",
    "app/forms.py": "# Tu ajouteras ici les classes de formulaire (connexion, ajout, etc.) avec Flask-WTF\n",
    "app/templates/base.html": """<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}Gestionnaire MDP{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
<body>
    <div class="container">
        {% block content %}{% endblock %}
    </div>
</body>
</html>
""",
    "app/templates/login.html": """{% extends "base.html" %}
{% block title %}Connexion{% endblock %}
{% block content %}
<h2>Connexion</h2>
<form method="POST">
    <!-- Formulaire de mot de passe maître ici -->
</form>
{% endblock %}
""",
    "static/style.css": "body { font-family: Arial; background-color: #f5f5f5; padding: 20px; }\n",
    "donnees.json": "{}",
    "mdp_secondaire.key": ""
}

# Création des dossiers
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Création des fichiers
for filepath, content in files.items():
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

print("✅ Arborescence du projet Flask générée avec succès.")
