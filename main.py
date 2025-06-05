import os

structure = {
    "gestionnaire_web": {
        "templates": ["login.html", "dashboard.html", "ajouter.html"],
        "static": ["style.css"],
        "utils": ["securite.py"],
        "app.py": None,
        "requirements.txt": None,
        "donnees.json": None,
        "mdp_secondaire.key": None
    }
}

def creer_structure(d, racine=""):
    for nom, contenu in d.items():
        chemin = os.path.join(racine, nom)
        if contenu is None:
            # fichier vide
            with open(chemin, "w", encoding="utf-8") as f:
                pass
        elif isinstance(contenu, list):
            # dossier avec fichiers
            os.makedirs(chemin, exist_ok=True)
            for fichier in contenu:
                chemin_fichier = os.path.join(chemin, fichier)
                with open(chemin_fichier, "w", encoding="utf-8") as f:
                    pass
        elif isinstance(contenu, dict):
            os.makedirs(chemin, exist_ok=True)
            creer_structure(contenu, chemin)

creer_structure(structure)
print("Structure créée avec succès !")
