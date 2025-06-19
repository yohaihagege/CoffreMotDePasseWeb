import base64
import hashlib
from cryptography.fernet import Fernet

def generate_key(mot_de_passe_maitre):
    digest = hashlib.sha256(mot_de_passe_maitre.encode()).digest()
    return base64.urlsafe_b64encode(digest)
def load_key():
    try:
        with open("key.key", "rb") as f:
            return f.read()
    except FileNotFoundError:
        return None
def chiffrer(cle, texte):
    f = Fernet(cle)
    return f.encrypt(texte.encode()).decode()

def dechiffrer(cle, texte_chiffre):
    f = Fernet(cle)
    return f.decrypt(texte_chiffre.encode()).decode()
