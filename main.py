from vault import store_password, fetch_all_passwords, update_password, delete_credential, load_salt
from password_generator import generate_password
from password_analyzer import analyze_password , print_strength_bar
from breach_checker import is_password_breached
from utils.key_derivation import derive_key
from utils.encryption import decrypt_data
from config import PASSWORD_EXPIRY_DAYS
from datetime import datetime, timedelta
from getpass import getpass
from vault import verify_master_password
import sys

def password_reuse_check(password, key):
    for site, enc_username, enc_password, created_at in fetch_all_passwords():
        stored_password = decrypt_data(key, enc_password)
        if stored_password == password:
            return True
    return False

def view_passwords(key):
    credentials = fetch_all_passwords()
    expired_entries = check_password_expiry(credentials)

    if not credentials:
        print("No Saved Credentials.")
    else:
        print("+-----------------------------------------------------------------------------------------------+")
        for site, enc_username, enc_password, created_at in credentials:
            username = decrypt_data(key, enc_username)
            password = decrypt_data(key, enc_password)
            print(f"Site: {site} | Username: {username} | Password: {password} | Created: {created_at}")
        print("+-----------------------------------------------------------------------------------------------+")
    if expired_entries:
        print("\nThe following entries are expired and should be updated:")
        for site, username in expired_entries:
            choice = input(f"Do you want to update the password for {site} ({username})? (yes/no): ").strip().lower()
            if choice == 'yes':
                new_password = input(f"Enter a new password for {site} ({username}): ").strip()
                if update_password(site, username, new_password, key):
                    print(f"Password updated for {site} / {username}.")
                else:
                    print("Failed to update password.")

def check_password_expiry(credentials):
    expired = []
    for entry in credentials:
        site, username, password, created_at = entry
        created_at_dt = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
        if datetime.now() - created_at_dt > timedelta(days=PASSWORD_EXPIRY_DAYS):
            print(f"⚠️ Password for site '{site}' (username: {username}) is older than 90 days.")
            expired.append((site, username))
    return expired

def cool_banner():
    print("\033[96m")
    print("=================================")
    print("     VAULT PASSWORD MANAGER     ")
    print("=================================")
    print("[1] Add New Credentials")
    print("[2] View Saved Passwords")
    print("[3] Delete Credentials")
    print("[4] Exit")
    print("=================================")

def main():
    salt = load_salt()
    if not salt:
        print("❌ Vault not initialized. Please run the initializer script.")
        return

    # Authenticate once per session
    while True:
        master_password = getpass("Enter Master Password: ")
        key = derive_key(master_password, salt)
        if verify_master_password(key):
            print("✅ Master password verified. Welcome!")
            break
        else:
            print("❌ Incorrect Master Password.")

    while True:
        cool_banner()
        choice = input("Enter your choice (1/2/3/4): ").strip()

        if choice == '4':
            print("Exiting VAULT Password Manager. Goodbye!")
            print("\033[0m")
            sys.exit(0)

        elif choice == '1':
            site = input("Enter Site Name: ").strip()
            username = input("Enter Username: ").strip()
            password = getpass("Enter Password: ").strip()

            result = analyze_password(password)
            print_strength_bar(result["score"])

            reused = password_reuse_check(password, key)
            breached = is_password_breached(password)

            issues = []
            if result["label"] == "Weak":
                issues.append("Weak")
            if reused:
                issues.append("Reused")
            if breached:
                issues.append("Breached")

            if issues:
                print(f"\n⚠️ Issues detected: {', '.join(issues)}")
                while True:
                    suggested_password = generate_password()
                    print(f"\nSuggested secure password: {suggested_password}")
                    print("Choose an option:")
                    print("[1] Use suggested secure password")
                    print("[2] Enter your own password")

                    choice = input("Your choice (1/2): ").strip()

                    if choice == "1":
                        result = analyze_password(suggested_password)
                        print_strength_bar(result["score"])
                        store_password(site, username, suggested_password, key)
                        print("✅ Secure password stored.")
                        break


                    elif choice == "2":
                        user_password = getpass("Enter your custom password: ").strip()
                        result = analyze_password(user_password)
                        print_strength_bar(result["score"])
                        reused = password_reuse_check(user_password, key)
                        breached = is_password_breached(user_password)

                        issues = []
                        if result["label"] == "Weak":
                            issues.append("Weak")
                        if reused:
                            issues.append("Reused")
                        if breached:
                            issues.append("Breached")

                        if issues:
                            print(f"\n⚠️ Issues detected: {', '.join(issues)}. Please try again.")
                        else:
                            store_password(site, username, user_password, key)
                            print("✅ Strong password stored.")
                            break
                    else:
                        print("❌ Invalid choice. Please select 1 or 2.")

            else:
                store_password(site, username, password, key)
                print("Password is strong and stored securely.✅")

        elif choice == '2':
            view_passwords(key)

        elif choice == '3':
            site = input("Enter Site Name to delete: ").strip()
            username = input("Enter Username to delete: ").strip()
            confirm = input(f"Are you sure you want to delete credentials for {site} / {username}? (yes/no): ").strip().lower()
            if confirm == 'yes':
                deleted = delete_credential(site.strip().lower(), username.strip().lower(), key)
                if deleted:
                    print("Credential deleted successfully.✅")
                else:
                    print("Credential not found.")
            else:
                print("Deletion cancelled.")

if __name__ == '__main__':
    main()
