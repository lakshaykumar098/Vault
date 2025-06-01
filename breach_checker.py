import hashlib
import requests

def is_password_breached(password: str) -> bool:
    """
    Checks if the given password has been breached using the HIBP API.
    Returns True if password is found in breaches, else False.
    """
    sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix, suffix = sha1_password[:5], sha1_password[5:]

    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    headers = {"User-Agent": "VaultAI-PwnedChecker"}
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise RuntimeError(f"Error fetching data from HIBP API: {response.status_code}")

        hashes = (line.split(':') for line in response.text.splitlines())
        return any(suffix == hash_suffix for hash_suffix, _ in hashes)
    
    except Exception as e:
        print(f"[ERROR] Failed to check password breach: {e}")
        return False
