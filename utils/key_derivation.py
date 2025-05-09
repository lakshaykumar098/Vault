import base64
import os
from hashlib import pbkdf2_hmac

def derive_key(master_password, salt, iterations=200000):
    key = pbkdf2_hmac('sha256', master_password.encode(), salt, iterations, dklen=32)
    return base64.urlsafe_b64encode(key)

def generate_salt():
    return os.urandom(16)