from cryptography.fernet import Fernet
import base64
import hashlib

def generate_key(master_password):
    digest = hashlib.sha256(master_password.encode()).digest()
    return base64.urlsafe_b64encode(digest)

def encrypt(key, message):
    return Fernet(key).encrypt(message.encode())

def decrypt(key, token):
    return Fernet(key).decrypt(token).decode()
