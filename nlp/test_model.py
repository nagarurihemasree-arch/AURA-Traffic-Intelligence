import joblib


# =====================================
# LOAD AI MODEL
# =====================================

model = joblib.load("models/complaint_model.pkl")

vectorizer = joblib.load(
    "models/tfidf_vectorizer.pkl"
)


# =====================================
# TEST DATA
# =====================================


test_data = [

    # Pothole
    ("A massive hole in the road is causing problems for cars", "Pothole"),
    ("There is a deep crater on the street", "Pothole"),
    ("Vehicles may get damaged because the road has a big hole", "Pothole"),

    # Water Leakage
    ("Water is leaking heavily from an underground pipe", "Water Leakage"),
    ("A broken pipeline is flooding the road", "Water Leakage"),
    ("Water is continuously flowing from the damaged pipe", "Water Leakage"),

    # Garbage
    ("Trash is piling up near the market", "Garbage"),
    ("Waste has been lying on the street for several days", "Garbage"),
    ("The garbage bin is full and overflowing", "Garbage"),

    # Streetlight
    ("The road is completely dark because the lights are not working", "Streetlight"),
    ("Several street lamps are broken", "Streetlight"),
    ("The street light pole is not functioning properly", "Streetlight"),

    # Drainage
    ("Sewage water is overflowing from the drain", "Drainage"),
    ("The drainage system is blocked and causing flooding", "Drainage"),
    ("Water cannot flow because the sewer drain is blocked", "Drainage")

]




# =====================================
# AI MODEL TEST
# =====================================

correct_predictions = 0
total_tests = len(test_data)


print("\n================================")
print("       🤖 AI MODEL TEST")
print("================================")


for complaint, expected_category in test_data:

    # Convert text into numbers
    complaint_vector = vectorizer.transform([complaint])

    # AI prediction
    prediction = model.predict(complaint_vector)[0]

    # AI confidence
    probabilities = model.predict_proba(
        complaint_vector
    )

    confidence = probabilities.max() * 100


    # Check if prediction is correct
    if prediction == expected_category:

        result = "✅ CORRECT"
        correct_predictions += 1

    else:

        result = "❌ INCORRECT"


    # Display result
    print("\n📝 Complaint:")
    print(complaint)

    print("\n🎯 Expected Category:")
    print(expected_category)

    print("\n🤖 AI Prediction:")
    print(prediction)

    print(f"\n📊 Confidence: {confidence:.2f}%")

    print("\nResult:")
    print(result)

    print("--------------------------------")


# =====================================
# FINAL ACCURACY
# =====================================

accuracy = (
    correct_predictions / total_tests
) * 100


print("\n================================")
print("       📊 FINAL RESULTS")
print("================================")

print(f"\nTotal Tests: {total_tests}")

print(f"Correct Predictions: {correct_predictions}")

print(f"Accuracy: {accuracy:.2f}%")

print("\n================================")
print("       TEST COMPLETED ✅")
print("================================")