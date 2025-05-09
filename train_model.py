import pandas as pd
import random
import os
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from utils.password_features import advanced_password_features
from password_generator import generate_password
from config import MODEL_PATH
from utils.passwords_data import breached_passwords, common_words

def main():
    data = []
    labels = []

    # Breached passwords (weak passwords)
    for pwd in breached_passwords:
        data.append(advanced_password_features(pwd))
        labels.append(0)

    # Common words with numbers (weak passwords)
    for word in common_words:
        pwd = word + str(random.randint(1, 999))
        data.append(advanced_password_features(pwd))
        labels.append(0)

    # Random weak passwords (5 characters + '123')
    for _ in range(200):
        pwd = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(5)) + '123'
        data.append(advanced_password_features(pwd))
        labels.append(0)

    # Strong passwords (randomly generated strong passwords)
    for _ in range(1000):
        pwd = generate_password()
        data.append(advanced_password_features(pwd))
        labels.append(1)

    # Convert the data into a DataFrame and labels into a list
    X = pd.DataFrame(data)
    y = labels

    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Create and train the RandomForest model
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)

    # Save the trained model
    if not os.path.exists(os.path.dirname(MODEL_PATH)):
        os.makedirs(os.path.dirname(MODEL_PATH))

    joblib.dump(model, MODEL_PATH)
    print("✅ Smarter AI Model trained and saved successfully!")

if __name__ == "__main__":
    main()