from cryptography.fernet import Fernet

def encrypt_data(key, data):
    cipher = Fernet(key)
    return cipher.encrypt(data.encode())

def decrypt_data(key, token):
    cipher = Fernet(key)
    return cipher.decrypt(token).decode()