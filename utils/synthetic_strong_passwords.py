import random
import string

def strong_pattern_generator():
    styles = []

    # Category 1: Symbol-heavy passwords (high entropy)
    for _ in range(200):
        pwd = ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=18))
        styles.append(pwd)

    # Word banks for variety
    nouns = ["Bridge", "Rocket", "Falcon", "Matrix", "Engine", "River", "Laptop", "Shield", "Server", "Switch"]
    verbs = ["Jump", "Drive", "Hack", "Build", "Run", "Type", "Launch", "Scan", "Save", "Push"]
    adjectives = ["Strong", "Quick", "Bright", "Sharp", "Deep", "Silent", "Fast", "Secure", "Fresh", "Stable"]
    user_words = ["Lakshay", "Naman", "Admin", "Dev", "Root", "Master", "Shadow", "Tiger", "Dragon", "Buddy"]

    # Category 2: Word combos + digits + symbols
    for _ in range(150):
        word_combo = random.choice(adjectives) + random.choice(nouns)
        pwd = f"{word_combo}{random.randint(10, 999)}{random.choice('!@#$%^&*')}"
        styles.append(pwd)

    # Category 3: Passphrase-style (real words + symbols + numbers)
    for _ in range(150):
        phrase = random.choice(user_words) + random.choice('!@#') + \
                 random.choice(verbs) + str(random.randint(10, 99))
        styles.append(phrase)

    # Category 4: Custom structured + entropy mix
    for _ in range(100):
        base = ''.join(random.choices('lakshaynamanthisisaboysecurepass', k=8))
        symbols = ''.join(random.choices('!@#$%^&*', k=3))
        digits = ''.join(random.choices(string.digits, k=4))
        styles.append(base + symbols + digits)

    return styles
