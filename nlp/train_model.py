import pandas as pd
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression


# Load cleaned dataset
data = pd.read_csv("data/cleaned_complaints.csv")


# X = Complaint text
X_text = data["cleaned_text"]


# y = Correct category
y = data["category"]


# Convert text into numbers
vectorizer = TfidfVectorizer()

X = vectorizer.fit_transform(X_text)


# Create the AI model
model = LogisticRegression(max_iter=1000)


# Train the AI model
model.fit(X, y)
# Save the trained AI model
joblib.dump(model, "models/complaint_model.pkl")

# Save the TF-IDF vectorizer
joblib.dump(vectorizer, "models/tfidf_vectorizer.pkl")

print("AI model and TF-IDF vectorizer saved successfully! 💾")



print("AI Model trained successfully! 🤖")

print("\nThe AI learned these categories:")

for category in model.classes_:
    print("-", category)
    # Test the AI with multiple new complaints

test_complaints = [
    "There is a large hole in the road",
    "Water is leaking from a broken pipe",
    "Garbage is overflowing on the street",
    "The street lamp is broken and the road is dark",
    "The drain is blocked and sewage is overflowing"
]

print("\n--- AI TEST RESULTS ---")

for complaint in test_complaints:

    # Convert complaint into numbers
    complaint_vector = vectorizer.transform([complaint])

    # Ask AI for prediction
    prediction = model.predict(complaint_vector)

# Get confidence probabilities
probabilities = model.predict_proba(complaint_vector)

# Find the highest probability
confidence = probabilities.max() * 100

print("\nComplaint:", complaint)
print("Prediction:", prediction[0])
print(f"Confidence: {confidence:.2f}%")