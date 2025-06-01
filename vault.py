import sqlite3
from config import DB_NAME
from utils.encryption import encrypt_data, decrypt_data
from datetime import datetime

conn = sqlite3.connect(DB_NAME)
c = conn.cursor()

def initialize_vault():
    c.execute('''
        CREATE TABLE IF NOT EXISTS vault (
            id INTEGER PRIMARY KEY,
            site TEXT,
            username BLOB,
            password BLOB,
            created_at TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value BLOB
        )
    ''')
    conn.commit()


def verify_master_password(key):
    c.execute('SELECT value FROM settings WHERE key = ?', ('auth_token',))
    row = c.fetchone()
    if not row:
        return False
    encrypted_token = row[0]
    try:
        decrypted = decrypt_data(key, encrypted_token)
        return decrypted == "vault_verification"
    except Exception:
        return False


def store_password(site, username, password, key):
    encrypted_username = encrypt_data(key, username)
    encrypted_password = encrypt_data(key, password)
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute('INSERT INTO vault (site, username, password, created_at) VALUES (?, ?, ?, ?)', (site, encrypted_username, encrypted_password, created_at))
    conn.commit()

def fetch_all_passwords():
    c.execute('SELECT site, username, password, created_at FROM vault')
    return c.fetchall()

def update_password(site, username, new_password, key):
    """Update the password for a site and username in the vault."""
    # Encrypt the new password
    encrypted_password = encrypt_data(key, new_password)

    # Get the current datetime for the creation timestamp
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Update the password and creation timestamp in the database
    c.execute('''
        UPDATE vault
        SET password = ?, created_at = ?
        WHERE site = ? AND username = ?
    ''', (encrypted_password, created_at, site, username))
    
    conn.commit()
    print(f"Password for {site} ({username}) updated successfully.")
    return True

def delete_credential(site, username, key):
    """Delete a site and username entry from the vault."""
    # Fetch all credentials from the vault
    c.execute('SELECT site, username, password FROM vault')
    entries = c.fetchall()
    found = False
    for entry in entries:
        stored_site, stored_enc_username, stored_enc_password = entry
          
        # Decrypt the stored username before comparing
        decrypted_username = decrypt_data(key, stored_enc_username)
        # Normalize case and strip whitespace for comparison
        stored_site = stored_site.strip().lower()
        decrypted_username = decrypted_username.strip().lower()
        # Check if the site and username match
        if stored_site == site and decrypted_username == username:
            c.execute('DELETE FROM vault WHERE site = ? AND username = ?', (stored_site, stored_enc_username))
            conn.commit()  # Commit the changes to ensure deletion is saved
            found=True
            print(f"Deleted credentials for {site} / {username}")
            break

    if not found:
        print(f"Credentials for {site} / {username} not found")
        return False
    return True

def save_salt(salt):
    c.execute('INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)', ('salt', salt))
    conn.commit()

def load_salt():
    c.execute('SELECT value FROM settings WHERE key = ?', ('salt',))
    row = c.fetchone()
    return row[0] if row else None