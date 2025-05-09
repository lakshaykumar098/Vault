import hashlib
from config import BREACHED_PASSWORD_FILE

def hash_password(password):
    """Hash the password to SHA1 for comparison."""
    return hashlib.sha1(password.encode()).hexdigest().upper()

def check_breach(password):
    """Check if the hashed password is in the breached password dataset."""
    hashed = hash_password(password)
    prefix = hashed[:5]  # First 5 characters of the hash
    suffix = hashed[5:]  # Remaining characters of the hash
    
    # Open the breached password file
    try:
        with open(BREACHED_PASSWORD_FILE, 'r') as file:
            for line in file:
                if line.startswith(prefix):  # Check if hash prefix matches
                    if suffix in line:  # Check if suffix matches
                        return True
        return False
    except FileNotFoundError:
        print(f"Error: The file {BREACHED_PASSWORD_FILE} is missing.")
        return False
