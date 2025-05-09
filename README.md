
# 🔐 Vault: Password Manager (Secure CLI Tool)

A fully encrypted, interactive password manager built for security and usability.  
Now featuring a streamlined menu-only interface, strong password enforcement, encrypted storage, breach detection, and one-time authentication.

---

## 🚀 Features

- 🔐 **Master Password Authentication**  
  Uses PBKDF2 to derive a cryptographic key from your master password.

- 🧠 **Interactive Menu Interface**  
  No command-line arguments — everything is handled through a clean, user-friendly menu.

- 💪 **Password Strength Enforcement**  
  Automatically scores passwords, shows a visual strength bar, and prevents weak passwords unless overridden.

- 🛡️ **Offline Breach Detection**  
  Detects common breached passwords without sending data online.

- 🔁 **Password Reuse Prevention**  
  Warns if the password has already been used for another site.

- ⏰ **Password Expiry Tracking**  
  Notifies you if any credential is older than 90 days.

- ❌ **Credential Deletion with Confirmation**  
  Remove credentials for specific site/user combinations.

- 🔒 **End-to-End Encryption**  
  All stored data is encrypted using keys derived from your master password.

---

## 📦 Installation

1. Install required packages:

```bash
pip install -r requirements.txt
```

2. Initialize the vault (run **once**):

```bash
python init_vault.py
```

3. Launch the password manager:

```bash
python main.py
```

---

## 🧭 Usage Guide

After launching:

```bash
python main.py
```

You'll be prompted for your master password (one-time per session). Then:

```
=================================
     VAULT PASSWORD MANAGER
=================================
[1] Add New Credentials
[2] View Saved Passwords
[3] Delete Credentials
[4] Exit
=================================
```

### Menu Actions:

| Option | Description |
|--------|-------------|
| 1 | Add a new credential (site, username, password) |
| 2 | View all saved credentials (decrypted) |
| 3 | Delete a credential with confirmation |
| 4 | Exit the manager |

---

## 🔍 Password Safety Checks

When adding a password, the tool checks for:

- ❌ Weak strength
- 🔁 Reuse within vault
- 🔓 Known breached passwords (offline check)

If issues are found, you can:
- Accept a randomly generated strong password, or
- Keep trying until your custom password is strong enough

---

## 🔐 Security Design

- Master password never stored
- All credentials encrypted using Fernet (AES-based)
- Salt and auth token stored securely in SQLite
- Vault key derived with PBKDF2 (SHA256)

---

## 🧑‍💻 Project Structure

```
vault/
├── main.py               # Menu-driven CLI interface
├── init_vault.py         # Vault initialization script
├── vault.py              # DB logic & encryption interface
├── utils/                # Key derivation & crypto tools
├── password_analyzer.py  # Password scoring & strength bar
├── password_generator.py # Random password generator
├── breach_checker.py     # Local password breach check
```

---

## ✅ Good to Know

- No internet access is needed to use the manager
- If you delete your vault or salt, data cannot be recovered
- You can customize breach databases for offline checks

---

## 💡 Future Ideas

- Desktop GUI with the same backend
- Biometric or hardware key support
- Secure cloud sync (end-to-end encrypted)

---

## 🤝 Contribute

Suggestions and pull requests are welcome.  
Let’s build a better password manager, together.
