import pandas as pd
import re
import nltk
from nltk.corpus import stopwords

# Download English stopwords
nltk.download("stopwords", quiet=True)


# =====================================
# TEXT CLEANING FUNCTION
# =====================================

def clean_text(text):

    # Convert to lowercase
    text = text.lower()

    # Remove punctuation and numbers
    text = re.sub(r"[^a-z\s]", "", text)

    # Get English stopwords
    stop_words = set(stopwords.words("english"))

    # Split into words
    words = text.split()

    # Remove stopwords
    cleaned_words = [
        word for word in words
        if word not in stop_words
    ]

    # Join words
    return " ".join(cleaned_words)


# =====================================
# LOAD ORIGINAL DATASET
# =====================================

data = pd.read_csv("data/complaints.csv")


# =====================================
# CLEAN ALL COMPLAINTS
# =====================================

data["cleaned_text"] = data["text"].apply(clean_text)


# =====================================
# SAVE CLEANED DATASET
# =====================================

data.to_csv(
    "data/cleaned_complaints.csv",
    index=False
)


print("✅ Dataset cleaned successfully!")

print("\nTotal complaints:", len(data))

print("\nFirst 5 rows:")

print(
    data[["text", "category", "cleaned_text"]].head()
)