import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Load the prediction dataset
data = pd.read_csv("prediction/prediction_data.csv")

# Input features
X = data[
    [
        "complaint_count",
        "growth_rate",
        "cluster_size",
        "severity",
        "duration",
        "image_severity"
    ]
]

# Target
y = data["became_serious"]

# Split data into training and testing
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# Create Random Forest model
model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

# Train the model
model.fit(X_train, y_train)

# Test the model
y_pred = model.predict(X_test)

# Calculate accuracy
accuracy = accuracy_score(y_test, y_pred)

print("\n--- City Early Warning Prediction Model ---")
print("Model trained successfully!")
print("Accuracy:", round(accuracy * 100, 2), "%")

# Save the trained model
joblib.dump(model, "prediction_model.pkl")

print("Model saved as prediction_model.pkl")