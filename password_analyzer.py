import joblib
from utils.password_features import advanced_password_features
from termcolor import colored
from config import MODEL_PATH
model = joblib.load(MODEL_PATH)

def analyze_password_strength(password):
    features = advanced_password_features(password)
    prediction = model.predict([features])[0]
    return "Weak" if prediction == 0 else "Strong"


def show_strength_bar(score):
    bar_length = 50  # Bar length for visual representation
    filled_length = int(score / 2)  # Calculate filled length of the bar (since score is between 0-100)
    bar = '█' * filled_length + '-' * (bar_length - filled_length)  # Bar visualization

    # Determine the color based on the score
    if score < 40:
        color = 'red'
        strength_label = 'Weak'
    elif 40 <= score < 70:
        color = 'yellow'
        strength_label = 'Moderate'
    else:
        color = 'green'
        strength_label = 'Strong'

    # Display the colored bar and strength label
    print(colored(f"\nStrength: [{bar}] {score}% - {strength_label}", color))

def score_password(password):
    # Extract features
    features = advanced_password_features(password)
    
    # Basic scoring components
    length_score = min(len(password) * 5, 30)
    digit_score = 10 if features[1] > 0 else 0
    special_score = 20 if features[2] > 0 else 0
    upper_lower_score = 20 if features[3] and features[4] else 0
    dictionary_penalty = -30 if features[5] else 0
    common_password_penalty = -40 if features[6] else 0
    sequence_penalty = -20 if features[7] else 0
    repeating_penalty = -20 if features[9] else 0
    palindrome_penalty = -20 if features[10] else 0
    entropy_score = min(int(features[8]), 20)
    variety_score = features[11] * 5
    ratio_score = int(features[12] * 10)

    # Total score
    total_score = (length_score + digit_score + special_score + upper_lower_score +
                   dictionary_penalty + common_password_penalty + sequence_penalty +
                   repeating_penalty + palindrome_penalty + entropy_score + variety_score + ratio_score)

    # Clamp the score to 0-100 range
    total_score = max(0, min(100, total_score))

    return total_score
