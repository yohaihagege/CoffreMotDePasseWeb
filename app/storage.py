import os
import json
from app.security import chiffrer, dechiffrer
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)  # créé au démarrage

PASSWORDS_FILE = os.path.join(DATA_DIR, "passwords.json")
SECONDARY_KEY_FILE = os.path.join(DATA_DIR, "mdp_secondaire.key")

DATA_FILE = "data/donnees.json"
SECONDARY_KEY_FILE = "data/mdp_secondaire.key"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)
def load_key():
    if not os.path.exists("data/key.key"):
        print("❌ Clé manquante : data/key.key")
        return None
    with open("data/key.key", "rb") as file:
        return file.read()


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)
def store_secondary_password(encrypted_pwd):
    with open(SECONDARY_KEY_FILE, "wb") as f:
        f.write(encrypted_pwd)

def load_secondary_password():
    if not os.path.exists(SECONDARY_KEY_FILE):
        return None
    with open(SECONDARY_KEY_FILE, "rb") as f:
        return f.read()
