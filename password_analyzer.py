import joblib
from utils.password_features import advanced_password_features
from config import MODEL_PATH

model = joblib.load(MODEL_PATH)

def get_password_strength_score(password: str) -> float:
    features = advanced_password_features(password)
    proba = model.predict_proba([features])[0][1]
    return round(proba, 2)

def get_password_strength_label(score: float) -> str:
    if score < 0.3:
        return "Weak"
    elif score < 0.7:
        return "Moderate"
    else:
        return "Strong"

def analyze_password(password: str) -> dict:
    score = get_password_strength_score(password)
    label = get_password_strength_label(score)
    return {"score": score, "label": label}

def print_strength_bar(score):
    """
    Print a visually enhanced strength bar using Unicode and color based on AI score.
    """
    import math

    # Configuration
    total_blocks = 20
    filled_blocks = int(score * total_blocks)
    empty_blocks = total_blocks - filled_blocks
    percent = int(score * 100)

    # Bar characters
    filled_char = "█"
    empty_char = "░"

    # Emoji and color by strength
    if score < 0.3:
        color = "\033[91m"  # Red
        emoji = "🛑"
        label = "Weak"
    elif score < 0.7:
        color = "\033[93m"  # Yellow
        emoji = "⚠️"
        label = "Moderate"
    else:
        color = "\033[92m"  # Green
        emoji = "✅"
        label = "Strong"

    bar = filled_char * filled_blocks + empty_char * empty_blocks
    print(f"{color}Strength: [{bar}] {percent}% {emoji} ({label})\033[0m")

