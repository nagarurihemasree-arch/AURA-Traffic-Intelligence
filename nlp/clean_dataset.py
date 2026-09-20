import pandas as pd
import re
import nltk
from nltk.corpus import stopwords

# Download stopwords
nltk.download("stopwords")

# Load our dataset
data = pd.read_csv("data/complaints.csv")


def clean_text(text):

    # Convert text to lowercase
    text = text.lower()

    # Remove punctuation and numbers
    text = re.sub(r"[^a-z\s]", "", text)

    # Get English stopwords
    stop_words = set(stopwords.words("english"))

    # Split text into individual words
    words = text.split()

    # Remove stopwords
    cleaned_words = [
        word for word in words
        if word not in stop_words
    ]

    # Join words back together
    return " ".join(cleaned_words)


# Apply cleaning to every complaint
data["cleaned_text"] = data["text"].apply(clean_text)


# Show original and cleaned text
print(data[["text", "cleaned_text", "category"]])
# Save the cleaned dataset
data.to_csv("data/cleaned_complaints.csv", index=False)

print("\nCleaned dataset saved successfully!")