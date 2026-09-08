import joblib
import re
import nltk
from nltk.corpus import stopwords
from similar_complaints import count_similar_complaints
from urgency import calculate_urgency
from spike_detection import detect_spike


# =====================================
# TEXT CLEANING
# =====================================

nltk.download("stopwords", quiet=True)


def clean_text(text):

    text = text.lower()

    text = re.sub(r"[^a-z\s]", "", text)

    stop_words = set(stopwords.words("english"))

    words = text.split()

    cleaned_words = [
        word for word in words
        if word not in stop_words
    ]

    return " ".join(cleaned_words)
# =====================================
# RISK SCORE
# =====================================

def calculate_risk(ai_confidence, urgency_score, complaint_count,spike_warning):

    confidence_points = (ai_confidence / 100) * 20

    urgency_points = (urgency_score / 100) * 40


    if complaint_count >= 10:
        complaint_points = 40

    elif complaint_count >= 7:
        complaint_points = 30

    elif complaint_count >= 4:
        complaint_points = 20

    elif complaint_count >= 2:
        complaint_points = 10

    else:
        complaint_points = 5
    # Points based on complaint spike
    if spike_warning == "HIGH SPIKE":
        spike_points = 20

    elif spike_warning == "MODERATE SPIKE":
        spike_points = 10

    else:
        spike_points = 0


    risk_score = (
        confidence_points
        + urgency_points
        + complaint_points
        +spike_points
    )

    risk_score = round(risk_score, 2)


    if risk_score >= 70:
        risk_level = "HIGH"

    elif risk_score >= 40:
        risk_level = "MEDIUM"

    else:
        risk_level = "LOW"


    return risk_score, risk_level





# =====================================
# LOAD SAVED AI MODEL
# =====================================

model = joblib.load("models/complaint_model.pkl")

vectorizer = joblib.load(
    "models/tfidf_vectorizer.pkl"
)


# =====================================
# CITIZEN COMPLAINT
# =====================================

print("\n📝 ENTER CITY COMPLAINT")

complaint = input("Describe the problem: ")

location = input("Enter the location: ").strip()


# Number of similar complaints



# =====================================
# STEP 1: CLEAN TEXT
# =====================================

cleaned_complaint = clean_text(complaint)


# =====================================
# STEP 2: AI CATEGORY
# =====================================

complaint_vector = vectorizer.transform(
    [cleaned_complaint]
)

prediction = model.predict(
    complaint_vector
)[0]

probabilities = model.predict_proba(
    complaint_vector
)

confidence = probabilities.max() * 100


# =====================================
# UNKNOWN ISSUE DETECTION
# =====================================

CONFIDENCE_THRESHOLD = 40

if confidence < CONFIDENCE_THRESHOLD:
    prediction = "Unknown Issue"
    issue_status = "NEEDS MUNICIPAL REVIEW"
else:
    issue_status = "RECOGNIZED ISSUE"


# =====================================
# STEP 3: AUTOMATIC SIMILAR COMPLAINTS
# =====================================

if prediction == "Unknown Issue":
    complaint_count = 0
else:
    complaint_count = count_similar_complaints(
        prediction,
        location
    )
# =====================================
# STEP 3.5: SPIKE DETECTION
# =====================================

recent_count, older_count, spike_warning = detect_spike(
    prediction,
    location
)



# =====================================
# STEP 4: URGENCY
# =====================================

urgency_score, urgency_level = calculate_urgency(
    complaint
)




# =====================================
# STEP 5: FINAL RISK
# =====================================

if prediction == "Unknown Issue":
    risk_score = "UNDER REVIEW"
    risk_level = "NEEDS ASSESSMENT"

else:
    risk_score, risk_level = calculate_risk(
        confidence,
        urgency_score,
        complaint_count
    )

# =====================================
# FINAL CITY EARLY-WARNING REPORT
# =====================================

print("   🌆 CITY EARLY-WARNING SYSTEM \n")

print("\n📝 Citizen Complaint:")
print(complaint)
print(f"\n📍 Location: {location}")


print("\n🧹 Cleaned Complaint:")
print(cleaned_complaint)

print("\n🤖 AI Detected Issue:")
print(prediction)
print("\n📋 Issue Status:")
print(issue_status)
if prediction == "Unknown Issue":
    print("\n⚠️ MUNICIPAL REVIEW REQUIRED")
    print("This complaint could not be confidently categorized.")
    print("Please send it for manual review by the municipal authority.")

print(f"\n📊 AI Confidence: {confidence:.2f}%")


print(f"\n🚨 Urgency Score: {urgency_score}/100")

print("🚨 Urgency Level:", urgency_level)

print(f"\n👥 Similar Complaints: {complaint_count}")
print(f"\n📈 Recent Complaints (Last 3 Days): {recent_count}")

print(f"📅 Older Complaints: {older_count}")

print(f"🚨 Spike Warning: {spike_warning}")

if prediction == "Unknown Issue":
    print(f"\n🔥 FINAL RISK SCORE: {risk_score}")
else:
    print(f"\n🔥 FINAL RISK SCORE: {risk_score}/100")

print("🚨 RISK LEVEL:", risk_level)



print("\n______________________________________")