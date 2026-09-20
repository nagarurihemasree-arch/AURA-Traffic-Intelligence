import pandas as pd


def detect_spike(category, location):

    # Read the complaint dataset
    df = pd.read_csv("data/city_complaints.csv")

    # Convert date column to datetime format
    df["date"] = pd.to_datetime(df["date"])

    # Find complaints with the same category and location
    matching_complaints = df[
        (df["category"] == category)
        & (df["location"] == location)
    ].copy()

    # Check if there are matching complaints
    if matching_complaints.empty:
        return 0, 0, "NO SPIKE"

    # Find the latest date in the dataset
    latest_date = df["date"].max()

    # Recent period = last 3 days
    recent_start = latest_date - pd.Timedelta(days=2)

    # Count recent complaints
    recent_complaints = matching_complaints[
        matching_complaints["date"] >= recent_start
    ]

    recent_count = len(recent_complaints)

    # Count older complaints
    older_complaints = matching_complaints[
        matching_complaints["date"] < recent_start
    ]

    older_count = len(older_complaints)

    # Detect spike
    if recent_count >= 5:
        warning = "HIGH SPIKE"

    elif recent_count >= 3:
        warning = "MODERATE SPIKE"

    else:
        warning = "NO SPIKE"

    return recent_count, older_count, warning


# =====================================
# TEST SECTION
# =====================================

if __name__ == "__main__":

    category = "Water Leakage"
    location = "Area A"

    recent_count, older_count, warning = detect_spike(
        category,
        location
    )

    print("\n--- TIME-BASED SPIKE ANALYSIS ---")

    print(f"\nCategory: {category}")
    print(f"Location: {location}")

    print(f"\nRecent Complaints (Last 3 Days): {recent_count}")

    print(f"Older Complaints: {older_count}")

    print(f"\nWarning Status: {warning}")