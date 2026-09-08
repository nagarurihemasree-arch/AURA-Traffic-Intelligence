def calculate_urgency(text):

    # Convert text to lowercase
    text = text.lower()

    # High urgency words
    high_keywords = [
        "dangerous",
        "huge",
        "major",
        "emergency",
        "severe",
        "accident",
        "overflowing",
        "flooding",
        "collapsed",
        "burst",
        "damaging vehicles",
        "risk to people"
    ]

    # Medium urgency words
    medium_keywords = [
        "large",
        "broken",
        "blocked",
        "leaking",
        "damaged",
        "damaging",
        "deep",
        "cracked",
        "overflow",
        "not working"
    ]

    high_count = 0
    medium_count = 0

    # Check for high urgency words
    for word in high_keywords:
        if word in text:
            high_count += 1

    # Check for medium urgency words
    for word in medium_keywords:
        if word in text:
            medium_count += 1

    # Calculate urgency score
    score = (high_count * 30) + (medium_count * 15)

    # Limit score to 100
    score = min(score, 100)

    # Decide urgency level
    if score >= 60:
        level = "HIGH"
    elif score >= 30:
        level = "MEDIUM"
    else:
        level = "LOW"

    return score, level


# =====================================
# TEST SECTION
# Keep this at the BOTTOM of the file
# =====================================

if __name__ == "__main__":

    complaint = "There is a huge dangerous pothole on the road"

    score, level = calculate_urgency(complaint)

    print("\n--- URGENCY ANALYSIS ---")

    print("\nComplaint:")
    print(complaint)

    print("\nUrgency Score:")
    print(score)

    print("\nUrgency Level:")
    print(level)