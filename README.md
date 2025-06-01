# 🔐 Vault: AI-Powered Password Manager (Secure CLI Tool)

An advanced, encrypted password manager that uses artificial intelligence to analyze and score password strength — with built-in breach detection, reuse checks, expiry alerts, and strong password generation.  
Now powered by AI + HaveIBeenPwned API.

---

## 🚀 Features

- 🔐 **Master Password Authentication**  
  PBKDF2-derived cryptographic key from your master password secures the vault.

- 🧠 **AI-Based Password Strength Detection**  
  Passwords are evaluated using a trained ML model, detecting strength based on real-world patterns and entropy.

- 📊 **Visual Strength Meter**  
  Stylish strength bar displays score percentage and confidence level (Weak, Moderate, Strong).

- 🔎 **Live Breach Detection (HIBP API)**  
  Checks if a password has been found in real-world leaks using the HaveIBeenPwned API.

- 🔁 **Password Reuse Check**  
  Warns if you've reused the same password across multiple entries.

- ⏰ **Password Expiry Alerts**  
  Flags passwords older than `PASSWORD_EXPIRY_DAYS` (default: 90 days).

- 🔐 **End-to-End Encryption**  
  Username and password fields are encrypted with Fernet AES.

- 🧪 **Realistic Model Training**  
  Custom AI model trained on weak vs. strong password patterns including breached samples and synthetic secure variants.

---

## 📦 Installation

```bash
pip install -r requirements.txt
```

---

## 🛠️ Initialization (First-Time Setup)

```bash
python init_vault.py
```

This creates your encrypted vault and stores a secure salt and verification token.

---

## ▶️ Run the Application

```bash
python main.py
```

You'll be prompted to authenticate with your master password.

---

## 🧭 Usage Menu

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

---

## 🧠 AI-Driven Password Evaluation

When adding a new password:
- It is analyzed by the AI model (trained via `train_model.py`)
- It is scored from 0–1 and color-coded with a visual bar
- Feedback is shown (e.g. `Weak`, `Strong`, `Breached`, `Reused`)
- If weak, the tool suggests a randomly generated strong password

---

## 🔍 Security Overview

- **No passwords stored in plaintext**
- **All data encrypted** using AES (via Fernet)
- **Master password not stored** anywhere — only derived key is used
- Passwords are stored with timestamps to track expiry
- Uses HaveIBeenPwned API with k-anonymity (only hash prefixes sent)

---

## 📁 Project Structure

```
vault/
├── main.py                 # Interactive CLI logic
├── vault.py                # Database & encryption logic
├── init_vault.py           # Vault/salt setup script
├── train_model.py          # Model training logic
├── password_analyzer.py    # AI scoring + strength bar
├── password_generator.py   # Random password generator
├── password_features.py    # Feature engineering for AI
├── breach_checker.py       # HIBP API password check
├── utils/                  # Key derivation & encryption tools
```

---

## ✅ Best Practices

- Use strong, AI-approved passwords
- Update passwords flagged as expired (older than 90 days)
- Never delete your salt or encrypted vault — it's irreversible
- Periodically retrain `train_model.py` with newer samples

---

## 🔧 Future Enhancements (Planned)

- Desktop GUI version (Tkinter or PyQt)
- Cloud backup with E2E encryption
- Hardware token (YubiKey) integration

---

## 🤝 Contributions

Pull requests and feedback are welcome!  
Let's keep improving this secure password manager together.
