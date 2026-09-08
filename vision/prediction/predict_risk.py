import pandas as pd
import joblib
import os

# Load the trained prediction model
model_path = os.path.join(
    os.path.dirname(__file__),
    "..",
    "prediction_model.pkl"
)

model = joblib.load(model_path)


def predict_risk(
    complaint_count,
    growth_rate,
    cluster_size,
    severity,
    duration,
    image_severity
):
    # Create input data
    data = pd.DataFrame([{
        "complaint_count": complaint_count,
        "growth_rate": growth_rate,
        "cluster_size": cluster_size,
        "severity": severity,
        "duration": duration,
        "image_severity": image_severity
    }])

    # Predict probability
    probability = model.predict_proba(data)[0][1]

    # Convert probability to percentage
    probability_percent = round(probability * 100, 2)

    # Determine risk level
    if probability_percent >= 70:
        risk = "High"
    elif probability_percent >= 40:
        risk = "Medium"
    else:
        risk = "Low"

    return {
        "risk": risk,
        "escalation_probability": probability_percent
    }


# Test the prediction function
if __name__ == "__main__":

    result = predict_risk(
        complaint_count=10,
        growth_rate=1.2,
        cluster_size=7,
        severity=3,
        duration=4,
        image_severity=3
    )

    print("\n--- City Early Warning Risk Prediction ---")
    print("Risk:", result["risk"])
    print(
        "Escalation Probability:",
        result["escalation_probability"],
        "%"
    )