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
# encrypt_to_bytes pour stocker (pas de .decode())
def encrypt_to_bytes(cle, texte):
    f = Fernet(cle)
    return f.encrypt(texte.encode())

# encrypt_to_str pour afficher
def encrypt_to_str(cle, texte):
    return encrypt_to_bytes(cle, texte).decode()


def dechiffrer(cle, texte_chiffre):
    f = Fernet(cle)
    return f.decrypt(texte_chiffre.encode()).decode()
