from vault import initialize_vault, save_salt, c, conn
from utils.key_derivation import derive_key, generate_salt
from utils.encryption import encrypt_data
from getpass import getpass

def init_vault():
    print("🔐 Initializing Vault...")

    # Set up the DB tables
    initialize_vault()

    # Prompt for master password
    master_password = getpass("Create Master Password: ")
    if not master_password.strip():
        print("❌ Master password cannot be empty.")
        return

    # Generate salt and derive encryption key
    salt = generate_salt()
    save_salt(salt)
    key = derive_key(master_password, salt)

    # Store encrypted verification token
    verification_token = "vault_verification"
    encrypted_token = encrypt_data(key, verification_token)
    c.execute('INSERT OR REPLACE INTO settings (key, value) VALUES (?, ?)', ('auth_token', encrypted_token))
    conn.commit()

    print("✅ Vault successfully initialized and master password set.")

if __name__ == "__main__":
    init_vault()
