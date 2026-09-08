def calculate_risk(ai_confidence, urgency_score, complaint_count):

    # -------------------------
    # AI CONFIDENCE SCORE
    # Maximum contribution: 20
    # -------------------------
    confidence_points = (ai_confidence / 100) * 20


    # -------------------------
    # URGENCY SCORE
    # Maximum contribution: 40
    # -------------------------
    urgency_points = (urgency_score / 100) * 40


    # -------------------------
    # COMPLAINT COUNT SCORE
    # Maximum contribution: 40
    # -------------------------

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


    # -------------------------
    # FINAL RISK SCORE
    # -------------------------

    risk_score = (
        confidence_points
        + urgency_points
        + complaint_points
    )

    risk_score = round(risk_score, 2)


    # -------------------------
    # RISK LEVEL
    # -------------------------

    if risk_score >= 70:
        risk_level = "HIGH"

    elif risk_score >= 40:
        risk_level = "MEDIUM"

    else:
        risk_level = "LOW"


    return risk_score, risk_level


# -------------------------
# TEST THE SYSTEM
# -------------------------

ai_confidence = 70
urgency_score = 60
complaint_count = 8


risk_score, risk_level = calculate_risk(
    ai_confidence,
    urgency_score,
    complaint_count
)


print("\n--- CITY EARLY-WARNING RISK ANALYSIS ---")

print("\nAI Confidence:", ai_confidence, "%")

print("Urgency Score:", urgency_score)

print("Similar Complaints:", complaint_count)

print("\nFINAL RISK SCORE:", risk_score, "/ 100")

print("RISK LEVEL:", risk_level)