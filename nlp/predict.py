import joblib
import re
import nltk
from nltk.corpus import stopwords


# Download stopwords if needed
nltk.download("stopwords", quiet=True)


# -----------------------------
# TEXT CLEANING FUNCTION
# -----------------------------
def clean_text(text):

    # Convert to lowercase
    text = text.lower()

    # Remove punctuation and numbers
    text = re.sub(r"[^a-z\s]", "", text)

    # Get English stopwords
    stop_words = set(stopwords.words("english"))

    # Split text into words
    words = text.split()

    # Remove stopwords
    cleaned_words = [
        word for word in words
        if word not in stop_words
    ]

    # Join words again
    return " ".join(cleaned_words)


# -----------------------------
# LOAD SAVED AI
# -----------------------------

model = joblib.load("models/complaint_model.pkl")

vectorizer = joblib.load("models/tfidf_vectorizer.pkl")


# -----------------------------
# NEW COMPLAINT
# -----------------------------

complaint = "The Drainage system is blocked and water is overflowing"


# Clean the complaint
cleaned_complaint = clean_text(complaint)


# Convert text into numbers
complaint_vector = vectorizer.transform([cleaned_complaint])


# AI prediction
prediction = model.predict(complaint_vector)[0]


# AI confidence
probabilities = model.predict_proba(complaint_vector)

confidence = probabilities.max() * 100


# -----------------------------
# SHOW RESULTS
# -----------------------------

print("\n--- CITY COMPLAINT ANALYSIS ---")

print("\nOriginal Complaint:")
print(complaint)

print("\nCleaned Complaint:")
print(cleaned_complaint)

print("\nPredicted Category:")
print(prediction)

print(f"\nAI Confidence: {confidence:.2f}%")