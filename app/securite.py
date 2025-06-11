import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet

SEL = b'mon_sel_unique_et_constant'

def generate_key(password: str, salt=SEL) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))

def encrypt(key, plaintext):
    return Fernet(key).encrypt(plaintext.encode())

def decrypt(key, ciphertext):
    return Fernet(key).decrypt(ciphertext).decode()
