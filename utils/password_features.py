import string
import math
from utils.passwords_data import common_words

def is_sequential(password):
    sequential_patterns = ['abcdefghijklmnopqrstuvwxyz', 'qwertyuiop', 'asdfghjkl', 'zxcvbnm', '1234567890']
    password_lower = password.lower()
    for pattern in sequential_patterns:
        for i in range(len(pattern) - 2):
            if pattern[i:i+3] in password_lower:
                return True
    return False

# Enhanced function to calculate password entropy
def calculate_entropy(password):
    # Calculate the number of unique characters in the password
    unique_chars = set(password)
    # Use the formula for entropy: H = log2(N^L), where N is the number of unique characters, and L is the length of the password
    return math.log2(len(unique_chars) ** len(password))

# Check if the password has repeating characters (e.g., "aaaa", "1111")
def has_repeating_characters(password):
    for i in range(len(password) - 1):
        if password[i] == password[i + 1]:  # Check consecutive characters
            return True
    return False

# Check if the password is a palindrome (same forwards and backwards)
def is_palindrome(password):
    return password == password[::-1]

# Check the variety of characters in the password (lowercase, uppercase, digits, special)
def character_variety(password):
    variety = 0
    if any(c.islower() for c in password): variety += 1
    if any(c.isupper() for c in password): variety += 1
    if any(c.isdigit() for c in password): variety += 1
    if any(c in string.punctuation for c in password): variety += 1
    return variety

# Enhanced feature extractor
def advanced_password_features(password):
    features = {
        "length": len(password),
        "num_digits": sum(c.isdigit() for c in password),
        "num_special": sum(c in string.punctuation for c in password),
        "has_upper": any(c.isupper() for c in password),
        "has_lower": any(c.islower() for c in password),
        "has_dictionary_word": int(any(word in password.lower() for word in common_words)),
        "has_sequence": int(is_sequential(password)),
        "entropy": calculate_entropy(password),
        "has_repeating_characters": int(has_repeating_characters(password)),
        "is_palindrome": int(is_palindrome(password)),
        "character_variety": character_variety(password),
        "length_to_complexity_ratio": len(password) / (1 + calculate_entropy(password)),
    }
    return list(features.values())