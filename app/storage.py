import os
import json
from app.security import encrypt, decrypt

DATA_FILE = "data/donnees.json"
SECONDARY_KEY_FILE = "data/mdp_secondaire.key"

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

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
