import os
# Define the paths to the common words file and the breached passwords file
COMMON_WORDS_FILE = 'Training_data/rockyou.txt'
# Function to load common words from the file
def load_common_words():
    common_words = set()
    
    if os.path.exists(COMMON_WORDS_FILE):
        with open(COMMON_WORDS_FILE, 'r', encoding='utf-8', errors='ignore') as file:
            for line in file:
                # Strip any extra whitespace and newlines from the word
                common_words.add(line.strip().lower())  # Convert to lowercase for uniformity
    else:
        print(f"Error: The file {COMMON_WORDS_FILE} does not exist.")
    
    return common_words
# Load common words and breached passwords from the files
common_words = load_common_words()