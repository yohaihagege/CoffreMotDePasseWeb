# Ici tu mettras les fonctions : generer_cle_depuis_mdp, chiffrer, dechiffrer, etc.
import base64, json, os
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

sel = b'mon_sel_unique_et_constant'

def generer_cle_depuis_mdp(mot_de_passe: str, sel: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=sel,
        iterations=100_000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(mot_de_passe.encode()))

def chiffrer(cle, texte): return Fernet(cle).encrypt(texte.encode())
def dechiffrer(cle, texte_chiffre): return Fernet(cle).decrypt(texte_chiffre).decode()

fichier_donnees = "donnees.json"
fichier_mdp_secondaire = "mdp_secondaire.key"

def charger_donnees():
    if os.path.exists(fichier_donnees):
        with open(fichier_donnees, "r") as f:
            return json.load(f)
    return {}

def sauvegarder_donnees(data):
    with open(fichier_donnees, "w") as f:
        json.dump(data, f)

def sauvegarder_mdp_secondaire(cle, mdp):
    with open(fichier_mdp_secondaire, "wb") as f:
        f.write(chiffrer(cle, mdp))

def charger_mdp_secondaire(cle):
    if os.path.exists(fichier_mdp_secondaire):
        try:
            with open(fichier_mdp_secondaire, "rb") as f:
                donnees = f.read()
                return dechiffrer(cle, donnees)
        except InvalidToken:
            return None
    return None
